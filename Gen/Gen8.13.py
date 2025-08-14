import cadquery as cq
import numpy as np
from scipy.spatial.transform import Rotation as R
import re


#TODO:       目前在扫掠路径的处理上只能完成线性的
#            圆弧的目前没有选择好合适的方法
#            threepointarc方法只能用于二维平面，在三维空间中也只能先依托于基础平面再做投影
#            考虑使用spline方法 https://openhome.cc/zh-tw/cadquery/workplane/curvesurface/ 曲线质量取决于中间点数量

"""通用2D/3D圆弧中点计算（自动处理共面性）"""
def calculate_arc_midpoint(start, end, angle_rad, normal = None):
    
    start = np.array(start)
    end = np.array(end)
    dim = len(start)  # 2D或3D
    
    # 处理直线边
    if angle_rad == 0:
        return ((start + end) / 2).tolist()
    
    # 计算圆心和半径
    chord = end - start                                 #弦
    length = np.linalg.norm(chord)                      #弦长
    #angle_rad = np.radians(abs(angle_deg))             angle_deg>0为逆时针圆弧，<0为顺时针圆弧
    abs_angel = abs(angle_rad)
    radius = length / (2 * np.sin(abs(angle_rad) / 2))       #半径长度,直接使用弧度
    
    #2D情况下
    if dim == 2:
        # 计算法向量方向（由angle_deg决定）
        normal_dir = np.array([-chord[1], chord[0]])    #基础逆时针法向量
        
        if angle_rad < 0:                               #顺逆时针判断
            normal_dir = -normal_dir                    
        if abs_angel > np.pi:                           #优弧判断
            normal_dir = -normal_dir

        normal_dir = normal_dir / np.linalg.norm(normal_dir)  # 单位化
        
        # 计算圆心
        mid_point = (start + end) / 2
        center = mid_point + np.sqrt(radius**2 - (length/2)**2) * normal_dir
        
        # 计算中点（旋转一半角度）
        vec_start = start - center
        theta = angle_rad / 2
        rot_matrix = np.array([
            [ np.cos(theta), -np.sin(theta)],
            [ np.sin(theta),  np.cos(theta)]
        ])
        arc_mid = center + rot_matrix @ vec_start
        
    #3D情况
    else:
        # 验证/生成法向量
        if normal is None:
            raise ValueError("需要提供法向量")
        
        normal = np.array(normal)
        if np.allclose(normal, [0, 0, 0]):
            raise ValueError("法向量不能为零向量")
        
        if not np.isclose(np.dot(normal, chord), 0, atol=1e-6):
            raise ValueError("法向量必须垂直于弦")
        
        normal = normal / np.linalg.norm(normal)

        # 计算圆心（方向由angle_deg决定）
        mid_point = (start + end) / 2
        sign = 1 if angle_rad > 0 else -1
        center = mid_point + sign * np.sqrt(radius**2 - (length/2)**2) * normal
        print(f"{center}")
        
        # 计算中点
        vec_start = start - center
        rotation = R.from_rotvec(angle_rad/2 * normal)
        arc_mid = center + rotation.apply(vec_start)

    return arc_mid.tolist()


"""动态解析多边形顶点和边"""
def parse_polygon(data, prefix="X"):        #data：profile 或 Path

    vertices = []
    edges = []
    normals = [] if prefix == "P" else None        #记录path的法向量
    
    vertex_indices = []
    pattern = re.compile(rf"^{prefix}(\d+)$")       #说是只匹配X，而不会匹配0E1
    
    for key in data:
        match = pattern.match(key)
        if match:
            index = int(match.group(1))
            vertex_indices.append(index)
            
    if not vertex_indices:
        return(vertices,edges) if prefix == "X" else (vertices, edges, normals)
    
    vertex_indices.sort()
    max_index = max(vertex_indices)
    
    for i in vertex_indices:
        current_vertex = f"{prefix}{i}"
        
        vertices.append(data[current_vertex])        
        
        next_index = None
        for candidate in sorted(vertex_indices):
            if candidate > i:
                next_index = candidate
                break
            
        if next_index is None:
            next_index = vertex_indices[0]
        
        edge_key = f"{i}E{next_index}"
        edge_value = data.get(edge_key, 0)
        
        if isinstance(edge_value, dict):  # 兼容Path的复杂边定义 
            edges.append(edge_value.get("angle", 0))
        else:
            edges.append(edge_value)
        
        if prefix == "P":
            normal_key = f"{i}N{next_index}"
            normals.append(data.get(normal_key, [0, 0, 0]))  #如果没有法向量则默认[0,0,0]
            
    
    if prefix == "X":
        return vertices, edges
    else:
        return vertices, edges, normals
    


"""生成完整CadQuery脚本"""
def generate_cadquery_script(vi_dict, output_file):
    
    #脚本头部
    script = f"""# Auto-generated CadQuery script
import cadquery as cq
import numpy as np
from scipy.spatial.transform import Rotation as R

#通用扫掠路径构建函数
def build_path(points,plane):
    return cq.Workplane(plane).polyline(points).wire()

solids = []
cuts = []
"""    
    
    for vi_key,vi_data in vi_dict.items():
        #解析旋转和平移参数
        rotation_quat = vi_data.get("R" , [0, 0, 0, 1])
        translation = vi_data.get("T" , [0,0,0])
        is_solid = vi_data.get("is_solid",True)
        
        rot = R.from_quat(rotation_quat)
        
        x_dir = rot.apply([1, 0, 0])
        y_dir = rot.apply([0, 1, 0])
        z_dir = rot.apply([0, 0, 1])

        #为当前Vi创建工作平面
        script += f"""
#===== 处理 {vi_key} =====
#创建平面
x_dir_{vi_key} = {x_dir.tolist()}
y_dir_{vi_key} = {y_dir.tolist()}
z_dir_{vi_key} = {z_dir.tolist()}

custom_plane_{vi_key} = cq.Plane(
    origin = {translation},
    xDir = cq.Vector(*x_dir_{vi_key}),
    normal = cq.Vector(*z_dir_{vi_key})
)

base_{vi_key} = cq.Workplane(custom_plane_{vi_key})
"""

        # 解析Profile(外廓)
        profile_vertices, profile_edges = parse_polygon(vi_data["Profile"], "X")    #返回顶点和边
        
        # 添加Profile顶点和边
        script += f"base_{vi_key} = base_{vi_key}.moveTo({profile_vertices[0][0]}, {profile_vertices[0][1]})\n"         #添加起点
        
        for i in range(len(profile_edges)):
            end = profile_vertices[(i+1) % len(profile_vertices)]
            angle = profile_edges[i]
            
            if angle == 0:
                script += f"base_{vi_key} = base_{vi_key}.lineTo({end[0]}, {end[1]})\n"
            else:
                start = profile_vertices[i]
                mid = calculate_arc_midpoint(start, end, angle)         #计算圆弧边的中点
                script += f"base_{vi_key} = base_{vi_key}.threePointArc(({mid[0]}, {mid[1]}), ({end[0]}, {end[1]}))\n"
        script += f"base_{vi_key}.close()\n\n"     
    
    
        # 解析Path
        path_vertices, path_edges,path_normals = parse_polygon(vi_data["Path"], "P")             #返回路径点和路径边及法向量
        
        # 添加Path路径                                                                          
        script += f"# 扫掠路径\n"
        script += f"points_{vi_key} = [\n"
        
        for i , vertex in enumerate(path_vertices):
            script += f"        ({vertex[0]}, {vertex[1]}, {vertex[2]}){','if i < len(path_vertices)-1 else ''}\n"
        script += f"]\n"
        
        script += f"""
#构建扫掠路径
path_wire_{vi_key} = build_path(points_{vi_key}, custom_plane_{vi_key})
"""

        script += f"""#执行扫掠
swept_{vi_key} = base_{vi_key}.sweep(path_wire_{vi_key}, isFrenet = False, makeSolid = True)
"""

        if is_solid:
            script += f"solids.append(swept_{vi_key})\n\n"
        else:
            script += f"cuts.append(swept_{vi_key})\n\n"
            
    script +="""
#组合所有几何体
final_model = None

#处理所有实体
for solid in solids:
    if final_model is None:
        final_model = solid
    else:
        final_model = final_model.union(solid)
        
#处理所有切割体
for cut in cuts:
    if final_model is not None:
        final_model = final_model.cut(cut)
    else:
        print("警告：有切割体但没有实体作为基础")

"""
    #错误处理说是
    script += """
# 最终模型检查
if final_model is None:
    if solids:
        final_model = solids[0]
    elif cuts:
        final_model = cuts[0]
        print("警告：只创建了切割体，没有实体")
    else:
        raise RuntimeError("未生成任何几何体")

# 导出结果
cq.exporters.export(final_model, 'output_newformat.stl', exportType='STL')
print("模型已导出为output_newformat.stl")
"""



    # 保存脚本
    with open(output_file, 'w') as f:
        f.write(script)
    print(f"Generated CadQuery script saved to {output_file}")


# 示例数据
sample_data = {
    
    "V0":{
        "R": [0, 0, 0, 1],              #旋转参数
        "T": [0, 0, 0],                        #平移参数   
        "is_solid": True,
        "Profile": {                            #面
            "X0": [-454.53, 18.21], "0E1": 0,
            "X1": [-355.47, 166.79], "1E2": -4.12,
            "X2": [-200, 250], "2E3": 0,
            "X3": [300, 250], "3E4": -2.24,
            "X4": [500, -50], "4E5": 0,
            "X5": [300, -250], "5E6": 0,
            "X6": [-300, -250], "6E7": 0,
            "X7": [-442.03, -107.97], "7E0": -1.37
        },        
        "Path": {                               #扫掠路径
            "P0": [0, 0, 0], "0E1": np.pi,"0N1": [0,0,0],
            "P1": [0, 0, 200]
        }        
    },
    
    "V1":{
        "R": [0, 0, 0, 1],
        "T": [0, 0, 200],
        "is_solid": False,
        "Profile": {
            "X0":[20, 20], "0E1":np.pi,
            "X1":[50, 50], "1E0":np.pi, 
        },
        "Path": {
            "P0": [0, 0, 0], "0E1": 0,"0N1": [0,0,0],
            "P1": [0, 0, -200]
        }
    },
    
    "V2":{
        "R": [0, 0, 0, 1],
        "T": [0, 0, 200],
        "is_solid": False,
        "Profile": {
            "X0":[0, 0], "0E1":np.pi,
            "X1":[-50, -50], "1E0":np.pi
        },
        "Path": {
            "P0": [0, 0, 0], "0E1": 0,"0N1": [0,0,0],
            "P1": [0, 0, -100]
        }
    },
    
    "V3":{
        "R": [0, 0.707, 0, 0.707],
        "T": [-50, 100, 170],
        "is_solid": False,
        "Profile": {
            "X0":[30, 30], "0E1":np.pi,
            "X1":[-30, -30], "1E0":np.pi
        },
        "Path": {
            "P0": [0, 0, -100], "0E1": 0,"0N1": [0,0,0],
            "P1": [0, 0, 100]
        }        
    }

}



output_file = "../Gen_CADquery/gen_new_dataformat.py"
generate_cadquery_script(sample_data, output_file)