import cadquery as cq
import numpy as np
from scipy.spatial.transform import Rotation as R


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
    for key in data:
        if key.startswith(prefix) and key[1:].isdigit():
            vertex_indices.append(int(key[1:]))
            
    if not vertex_indices:
        return(vertices,edges) if prefix == "X" else (vertices, edges, normals)
    
    max_index = max(vertex_indices)
    
    i = 0
    
    while i <= max_index:
        current_vertex = f"{prefix}{i}"
        if current_vertex not in data:
            i += 1
            continue
        
        vertices.append(data[current_vertex])        
        
        next_idx = i + 1 if i + 1 <= max_index else 0
        
        edge_key = f"E{i}{next_idx}"
        edge_value = data.get(edge_key, 0)
        
        if isinstance(edge_value, dict):  # 兼容Path的复杂边定义 
            edges.append(edge_value.get("angle", 0))
        else:
            edges.append(edge_value)
        
        if prefix == "P":
            normal_key = f"N{i}{next_idx}"
            normals.append(data.get(normal_key, [0, 0, 0]))  #如果没有法向量则默认[0,0,0]
            
        i += 1 
    
    if prefix == "X":
        return vertices, edges
    else:
        return vertices, edges, normals
    

"""从Holes中提取Hole"""
def split_holes(Holes):
    hole_groups = {}
    
    for key, value in Holes.items():
        hole_id = ""
        for char in key:
            if char.isdigit():
                hole_id += char
            else:
                break
        if not hole_id:
            continue
    
        attr_key = key[len(hole_id):]
    
        if hole_id not in hole_groups:
            hole_groups[hole_id] = {}
        hole_groups[hole_id][attr_key] = value
        
    return hole_groups


"""生成完整CadQuery脚本"""
def generate_cadquery_script(vi_data, output_file):
    
    #解析旋转和平移参数
    rotation_quat = vi_data.get("R" , [0, 0, 0, 1])
    translation = vi_data.get("T" , [0,0,0])
    
    rot = R.from_quat(rotation_quat)
    
    x_dir = rot.apply([1, 0, 0])
    y_dir = rot.apply([0, 1, 0])
    z_dir = rot.apply([0, 0, 1])
    
    # 生成脚本
    script = f"""# Auto-generated CadQuery script
import cadquery as cq
import numpy as np
from scipy.spatial.transform import Rotation as R


#创建工作平面,应用初始旋转和平移
x_dir = {x_dir.tolist()}
y_dir = {y_dir.tolist()}
z_dir = {z_dir.tolist()}

custom_plane = cq.Plane(
    origin = {translation},
    xDir = cq.Vector(*x_dir),
    normal = cq.Vector(*z_dir)
)

base = cq.Workplane(custom_plane)
"""

    # 解析Profile(外廓)
    profile_vertices, profile_edges = parse_polygon(vi_data["Profile"], "X")    #返回顶点和边
    
    # 添加Profile顶点和边
    script += f"base = base.moveTo({profile_vertices[0][0]}, {profile_vertices[0][1]})\n"         #添加起点
    
    for i in range(len(profile_edges)):
        end = profile_vertices[(i+1) % len(profile_vertices)]
        angle = profile_edges[i]
        
        if angle == 0:
            script += f"base = base.lineTo({end[0]}, {end[1]})\n"
        else:
            start = profile_vertices[i]
            mid = calculate_arc_midpoint(start, end, angle)         #计算圆弧边的中点
            script += f"base = base.threePointArc(({mid[0]}, {mid[1]}), ({end[0]}, {end[1]}))\n"
    script += f"base.close()\n\n"     
    
    
    #解析孔洞
    has_holes = "Holes" in vi_data and vi_data["Holes"]
    if has_holes :
        hole_groups = split_holes(vi_data["Holes"])
        script += """#孔洞截面\n"""
        
        for hole_id, hole_data in hole_groups.items():
            hole_vertices, hole_edges = parse_polygon(hole_data,prefix="X")                 #对每个孔洞提取了顶点和圆弧角
            script += f"""#Hole {hole_id}
base = base.moveTo({hole_vertices[0][0]},{hole_vertices[0][1]})\n"""
    
            for i in range(len(hole_edges)):
                end = hole_vertices[(i+1) % len(hole_vertices)]
                angle = hole_edges[i]
                
                if angle == 0:
                    script += f"base = base.lineTo({end[0],{end[1]}})\n"
                else:
                    start = hole_vertices[i]
                    mid = calculate_arc_midpoint(start,end,angle)
                    script += f"base = base.threePointArc(({mid[0]},{mid[1]}),({end[0]},{end[1]}))\n"
            
            script += f"base = base.close()\n"
            #script += f"    holes.append(hole)\n"
            
        #script += f"    return holes\n\n"
    
    # 解析Path
    path_vertices, path_edges,path_normals = parse_polygon(vi_data["Path"], "P")             #返回路径点和路径边及法向量
    
    # 添加Path路径                                                                          
    script += f"""# 扫掠路径（{len(path_vertices)}个点）
def build_path():\n\n"""

    points = []
    script += f"    points = [\n"
    
    for i , vertex in enumerate(path_vertices):
        script += f"        ({vertex[0]}, {vertex[1]}, {vertex[2]}){','if i < len(path_vertices)-1 else ''}\n"
    script += f"    ]\n"
    
    script += f"""
    result = cq.Workplane(custom_plane).polyline(points)\n
    return result.wire()\n\n"""

    script += """#执行扫掠
model = base.sweep(build_path(), isFrenet=False,makeSolid=True)

# 导出结果
#cq.exporters.export(model, "output.step")
cq.exporters.export(model, 'output.stl', exportType='STL')  
"""

    # 保存脚本
    with open(output_file, 'w') as f:
        f.write(script)
    print(f"Generated CadQuery script saved to {output_file}")


# 示例数据
sample_data = {
    "R": [0.707, 0, 0, 0.707],              #旋转参数
    "T": [100, 100, 100],                        #平移参数       
    
    "Profile": {                            #面
        "X0": [-454.53, 18.21], "E01": 0,
        "X1": [-355.47, 166.79], "E12": -4.12,
        "X2": [-200, 250], "E23": 0,
        "X3": [300, 250], "E34": -2.24,
        "X4": [500, -50], "E45": 0,
        "X5": [300, -250], "E56": 0,
        "X6": [-300, -250], "E67": 0,
        "X7": [-442.03, -107.97], "E70": -1.37
    },
    
    "Holes":{
        "0X0":[20, 20], "0E01":np.pi,
        "0X1":[50, 50], "0E10":np.pi,
        
        "1X0":[0, 0], "1E01":np.pi,
        "1X1":[-50, -50], "1E10":np.pi
    },
    
    "Path": {                               #扫掠路径
        "P0": [0, 0, 0], "E01": np.pi,"N01": [0,0,0],
        "P1": [0, 0, 50]
    }
}

output_file = "../Gen_CADquery/gen_only1_strightpath_with_hole_changed_workplane.py"
generate_cadquery_script(sample_data, output_file)