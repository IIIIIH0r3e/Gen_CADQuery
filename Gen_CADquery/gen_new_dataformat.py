# Auto-generated CadQuery script
import cadquery as cq
import numpy as np
from scipy.spatial.transform import Rotation as R

#通用扫掠路径构建函数
def build_path(points,plane):
    return cq.Workplane(plane).polyline(points).wire()

solids = []
cuts = []

#===== 处理 V0 =====
#创建平面
x_dir_V0 = [1.0, 0.0, 0.0]
y_dir_V0 = [0.0, 1.0, 0.0]
z_dir_V0 = [0.0, 0.0, 1.0]

custom_plane_V0 = cq.Plane(
    origin = [0, 0, 0],
    xDir = cq.Vector(*x_dir_V0),
    normal = cq.Vector(*z_dir_V0)
)

base_V0 = cq.Workplane(custom_plane_V0)
base_V0 = base_V0.moveTo(-454.53, 18.21)
base_V0 = base_V0.lineTo(-355.47, 166.79)
base_V0 = base_V0.threePointArc((-347.01747633839705, 337.8427418138516), (-200, 250))
base_V0 = base_V0.lineTo(300, 250)
base_V0 = base_V0.threePointArc((494.0424302579048, 162.69495350526986), (500, -50))
base_V0 = base_V0.lineTo(300, -250)
base_V0 = base_V0.lineTo(-300, -250)
base_V0 = base_V0.lineTo(-442.03, -107.97)
base_V0 = base_V0.threePointArc((-470.77487817547114, -47.108451237861686), (-454.53, 18.21))
base_V0.close()

# 扫掠路径
points_V0 = [
        (0, 0, 0),
        (0, 0, 200)
]

#构建扫掠路径
path_wire_V0 = build_path(points_V0, custom_plane_V0)
#执行扫掠
swept_V0 = base_V0.sweep(path_wire_V0, isFrenet = False, makeSolid = True)
solids.append(swept_V0)


#===== 处理 V1 =====
#创建平面
x_dir_V1 = [1.0, 0.0, 0.0]
y_dir_V1 = [0.0, 1.0, 0.0]
z_dir_V1 = [0.0, 0.0, 1.0]

custom_plane_V1 = cq.Plane(
    origin = [0, 0, 200],
    xDir = cq.Vector(*x_dir_V1),
    normal = cq.Vector(*z_dir_V1)
)

base_V1 = cq.Workplane(custom_plane_V1)
base_V1 = base_V1.moveTo(20, 20)
base_V1 = base_V1.threePointArc((50.0, 20.0), (50, 50))
base_V1 = base_V1.threePointArc((20.0, 50.0), (20, 20))
base_V1.close()

# 扫掠路径
points_V1 = [
        (0, 0, 0),
        (0, 0, -200)
]

#构建扫掠路径
path_wire_V1 = build_path(points_V1, custom_plane_V1)
#执行扫掠
swept_V1 = base_V1.sweep(path_wire_V1, isFrenet = False, makeSolid = True)
cuts.append(swept_V1)


#===== 处理 V2 =====
#创建平面
x_dir_V2 = [1.0, 0.0, 0.0]
y_dir_V2 = [0.0, 1.0, 0.0]
z_dir_V2 = [0.0, 0.0, 1.0]

custom_plane_V2 = cq.Plane(
    origin = [0, 0, 200],
    xDir = cq.Vector(*x_dir_V2),
    normal = cq.Vector(*z_dir_V2)
)

base_V2 = cq.Workplane(custom_plane_V2)
base_V2 = base_V2.moveTo(0, 0)
base_V2 = base_V2.threePointArc((-50.0, 0.0), (-50, -50))
base_V2 = base_V2.threePointArc((0.0, -50.0), (0, 0))
base_V2.close()

# 扫掠路径
points_V2 = [
        (0, 0, 0),
        (0, 0, -100)
]

#构建扫掠路径
path_wire_V2 = build_path(points_V2, custom_plane_V2)
#执行扫掠
swept_V2 = base_V2.sweep(path_wire_V2, isFrenet = False, makeSolid = True)
cuts.append(swept_V2)


#===== 处理 V3 =====
#创建平面
x_dir_V3 = [0.0, 0.0, -1.0000000000000002]
y_dir_V3 = [0.0, 1.0000000000000002, 0.0]
z_dir_V3 = [1.0000000000000002, 0.0, 0.0]

custom_plane_V3 = cq.Plane(
    origin = [-50, 100, 170],
    xDir = cq.Vector(*x_dir_V3),
    normal = cq.Vector(*z_dir_V3)
)

base_V3 = cq.Workplane(custom_plane_V3)
base_V3 = base_V3.moveTo(30, 30)
base_V3 = base_V3.threePointArc((-29.999999999999996, 30.000000000000004), (-30, -30))
base_V3 = base_V3.threePointArc((29.999999999999996, -30.000000000000004), (30, 30))
base_V3.close()

# 扫掠路径
points_V3 = [
        (0, 0, -100),
        (0, 0, 100)
]

#构建扫掠路径
path_wire_V3 = build_path(points_V3, custom_plane_V3)
#执行扫掠
swept_V3 = base_V3.sweep(path_wire_V3, isFrenet = False, makeSolid = True)
cuts.append(swept_V3)


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
cq.exporters.export(final_model, 'output_newformat.step', exportType='STEP')
print("模型已导出为output_newformat.stl")
