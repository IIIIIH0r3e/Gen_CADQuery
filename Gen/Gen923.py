import cadquery as cq
import numpy as np
from scipy.spatial.transform import Rotation as R
import re
import json
import os


"""通用2D/3D圆弧中点计算（自动处理共面性）"""
def calculate_arc_midpoint(start, end, angle_rad, center , normal = None):
    """
    根据起点、终点、圆心和弧度角，计算圆弧上的中点
    start, end, center: list/tuple/np.array
    angle_rad: 弧度，正为逆时针，负为顺时针
    normal: 3D情况下的法向量（仅3D用）
    """
    
    start = np.array(start)
    end = np.array(end)
    center = np.array(center)
    dim = len(start)  # 2D或3D
    
    # 处理直线边
    if angle_rad == 0:
        return ((start + end) / 2).tolist()

    #2D情况下
    if dim == 2:
        # 将起点向量旋转 angle/2 得到中点
        vec_start = start - center
        theta = angle_rad / 2
        rot_matrix = np.array([
            [ np.cos(theta) , -np.sin(theta)],
            [ np.sin(theta) ,  np.cos(theta)]
        ])
        arc_mid = center + rot_matrix @ vec_start

    #3D情况
    else:
        # 验证/生成法向量
        if normal is None:
            raise ValueError("需要提供法向量")
        normal = np.array(normal) / np.linalg.norm(normal)

        # 计算中点
        vec_start = start - center
        rotation = R.from_rotvec(angle_rad/2 * normal)
        arc_mid = center + rotation.apply(vec_start)

    return arc_mid.tolist()


def generate_sketch_elliptical_arc(wp_var, edge_params):
    
    center = edge_params.get("origin", [0, 0])
    major = edge_params["major_radius"]
    minor = edge_params["minor_radius"]
    start_angle = np.degrees(edge_params["start_angle"])  # 弧度转角度
    end_angle = np.degrees(edge_params["end_angle"])      # 弧度转角度
    x_dir = edge_params.get("dx", [1, 0])
    sense = edge_params.get("clocksign", -1)
    
    rotation_deg = np.degrees(np.arctan2(x_dir[1], x_dir[0]))
    
    """
    由于原始数据定义的xy中，x的正方向为向右，y的正方向为向下
    所以在数据处理中为了保持正确：
    1.角度取负
    2.start和end角度互换
    3.顺逆时针保持不变
    """
    if sense == 1 :
        return f"""
#椭圆弧
{wp_var} = {wp_var}.ellipseArc({major}, {minor}, rotation_angle = {rotation_deg}, angle1 = {start_angle}, angle2 = {end_angle}, startAtCurrent = True, sense = {sense})
"""
    elif sense == -1 :
        return f"""
#椭圆弧
{wp_var} = {wp_var}.ellipseArc({major}, {minor}, rotation_angle = {rotation_deg}, angle1 = {-end_angle}, angle2 = {-start_angle}, startAtCurrent = True, sense = {sense})
"""

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
    
    for i in vertex_indices:
        current_vertex = f"{prefix}{i}"
        vertices.append(data[current_vertex])        
        
        next_index = vertex_indices[(vertex_indices.index(i) + 1) % len(vertex_indices)]
        edge_key = f"{i}E{next_index}"
        edge_value = data.get(edge_key, 0)
        
        if isinstance(edge_value, (int , float)):  # 兼容Path的复杂边定义
            edge_dict = {
                "type" : "circular_arc" if edge_value != 0 else "line",
                "angle" : edge_value
            } 
        elif isinstance(edge_value , dict):
            edge_dict = edge_value
            if "type" not in edge_dict :
                edge_dict["type"] = "elliptical_arc"
        else:
            edge_dict = {"type" : "line"}
            
        edges.append(edge_dict)
                 
        if prefix == "P":
            normal_key = f"{i}N{next_index}"
            normals.append(data.get(normal_key, [0, 0, 0]))  #如果没有法向量则默认[0,0,0]
            
   
    
    if prefix == "X":
        return vertices, edges
    else:
        return vertices, edges, normals
    

def filter_path_points(path_vertices, tol = 1e-6,path_edges = None):
    """按顺序过滤连续近重合点；返回过滤后的点列表"""
    filtered_points = []
    path_vertices = np.array(path_vertices)

    for i, edge in enumerate(path_edges):
        pts = path_vertices[i:i+2]  # 每条边的两个端点
        if hasattr(edge, "type"):
            if edge.type == "line":
                # 如果是直线，根据距离过滤
                if np.linalg.norm(pts[1] - pts[0]) > tol:
                    filtered_points.append(pts[0])
            elif edge.type in ["circle", "ellipse"]:
                # 圆弧或椭圆弧，保留首尾点
                filtered_points.append(pts[0])
            else:
                # 其他类型直接保留
                filtered_points.append(pts[0])
        else:
            # edge没有type属性，默认保留
            filtered_points.append(pts[0])
    # 最后加上最后一个顶点
    filtered_points.append(path_vertices[-1])

    return np.array(filtered_points)

def path_total_length(points):
    """计算折线总长度"""
    if len(points) < 2:
        return 0.0
    pts = np.array(points, dtype=float)
    segs = pts[1:] - pts[:-1]
    return float(np.linalg.norm(segs, axis=1).sum())

def path_is_valid(path_points, tol=1e-6, edges = None):
    """检查路径是否合法：至少两点且总长度 > tol"""
    return len(path_points) >= 2 and path_total_length(path_points) >= tol


"""生成完整CadQuery脚本"""
def generate_cadquery_script(vi_dict, output_file, shangpin_ID):
    
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
        
        # ===== 先准备 Path 点，并做过滤与合法性检查 =====
        path_vertices, path_edges,path_normals = parse_polygon(vi_data["Path"], "P")             #返回路径点和路径边及法向量
        filtered_path = filter_path_points(path_vertices, tol=1e-6,path_edges=path_edges)
        total_len = path_total_length(filtered_path)
        
        if not path_is_valid(filtered_path, tol=1e-6):
            script += f"# 跳过 {vi_key}：Path 无效（过滤后点数={len(filtered_path)}，总长={total_len:.6g} < 1e-6）\n"
            continue
        
        path_start = np.array(filtered_path[0])
        
        
        # ===== 路径有效，再开始缓冲该 VI 的脚本 =====
        vi_chunk = ""
        
        #解析旋转和平移参数
        M = np.array(vi_data["M"])
        R_mat = M[:3, :3]   #旋转
        T_vec = M[:3, 3]
        
        rot = R.from_matrix(R_mat)
        translation = T_vec + R_mat @ path_start
        is_solid = vi_data.get("is_solid",True)
        
        x_dir = rot.apply([1, 0, 0])
        y_dir = rot.apply([0, 1, 0])
        z_dir = rot.apply([0, 0, 1])

        #为当前Vi创建工作平面
        vi_chunk += f"""
#===== 处理 {vi_key} =====
#创建平面
x_dir_{vi_key} = {x_dir.tolist()}
y_dir_{vi_key} = {y_dir.tolist()}
z_dir_{vi_key} = {z_dir.tolist()}

custom_plane_{vi_key} = cq.Plane(
    origin = {translation.tolist()},
    xDir = cq.Vector(*x_dir_{vi_key}),
    normal = cq.Vector(*z_dir_{vi_key})
)

base_{vi_key} = cq.Workplane(custom_plane_{vi_key})
"""

        # 解析Profile(外廓)
        profile_vertices, profile_edges = parse_polygon(vi_data["Profile"], "X")    #返回顶点和边
        vi_chunk += f"base_{vi_key} = base_{vi_key}.moveTo({profile_vertices[0][0]}, {profile_vertices[0][1]})\n"         #添加起点
        
        last_point = profile_vertices[0]
        tol = 1e-6
        
        
        for i, edge in enumerate(profile_edges):
            end = profile_vertices[(i+1) % len(profile_vertices)]
            
            if edge["type"] == "line" :
                dist = np.linalg.norm(np.array(end) - np.array(last_point))
                if dist < tol:
                    vi_chunk += f"# 跳过零长度 lineTo({end[0]}, {end[1]})\n"
                    continue
                vi_chunk += f"base_{vi_key} = base_{vi_key}.lineTo({end[0]}, {end[1]})\n"
                last_point = end
            
            elif edge["type"] == "circular_arc" :
                start = profile_vertices[i]
                center = edge["origin"]
                angle = edge.get("angle", None)
                
                if np.allclose(start , end , atol=tol) and angle is not None and abs(abs(angle) - 2*np.pi) < 1e-3 :
                    #整圆
                    radius = np.linalg.norm(np.array(start) - np.array(center))
                    vi_chunk += f"base_{vi_key} = base_{vi_key}.center({center[0]}, {center[1]}).circle({radius})\n"
                    
                else:       #圆弧
                    mid = calculate_arc_midpoint(start , end , angle , center)
                    vi_chunk += f"base_{vi_key} = base_{vi_key}.threePointArc(({mid[0]}, {mid[1]}), ({end[0]}, {end[1]}))\n"
                
                last_point = end
                
            elif edge["type"] == "elliptical_arc" :
                vi_chunk += generate_sketch_elliptical_arc(f"base_{vi_key}", edge)
                last_point = end
           
        vi_chunk += f"base_{vi_key}.close()\n\n"     
    
         
        # 添加Path路径                                                                          
        vi_chunk += f"# 扫掠路径（已过滤近重合点；总长≈{total_len:.6g}）\n"
        vi_chunk += f"points_{vi_key} = [\n"
        
        for i , vertex in enumerate(path_vertices):
            vx, vy, vz = np.array(vertex) - path_start
            vi_chunk += f"        ({vx}, {vy}, {vz}){','if i < len(filtered_path)-1 else ''}\n"
        vi_chunk += f"]\n"
        
        vi_chunk += f"""
#构建扫掠路径
path_wire_{vi_key} = build_path(points_{vi_key}, custom_plane_{vi_key})
"""

        vi_chunk += f"""#执行扫掠
swept_{vi_key} = base_{vi_key}.sweep(path_wire_{vi_key}, isFrenet = False, makeSolid = True, normal = cq.Vector(*z_dir_{vi_key}))
"""

        if is_solid == "True":
            vi_chunk += f"solids.append(swept_{vi_key})\n\n"
        else:
            vi_chunk += f"cuts.append(swept_{vi_key})\n\n"
            
        script += vi_chunk
            
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
    script += f"""
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
cq.exporters.export(final_model, '/data/aihao/DATA/0919/test2/STL/{shangpin_ID}.stl', exportType='STL')
"""



    # 保存脚本
    with open(output_file, 'w') as f:
        f.write(script)
    #print(f"Generated CadQuery script saved to {output_file}")


def process_json_files(input_folder , output_folder):
    os.makedirs(output_folder, exist_ok=True)
    
    all_files = [ f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]
    
    for filename in all_files:
        file_path = os.path.join(input_folder, filename)
        
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            shangpin_ID = os.path.splitext(filename)[0]
            output_path = os.path.join(output_folder, f"{shangpin_ID}.py")
            
            generate_cadquery_script(data, output_path, shangpin_ID)
            
            print(f"已处理： {filename} -> {output_path}")
        
        except json.JSONDecodeError:
            print(f"跳过文件 {filename}: 不是有效的JSON格式")
        except Exception as e:
            print(f"处理文件 {filename} 时出错： {str(e)}")



if __name__ == "__main__":
    
    input_folder = "/data/aihao/DATA/0919/test2/JSON"
    output_folder = "/data/aihao/DATA/0919/test2/CADQuery"
    
    process_json_files(input_folder , output_folder)