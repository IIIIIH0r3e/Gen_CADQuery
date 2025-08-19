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
x_dir_V0 = [0.4447773445345138, 0.8195399470031683, -0.3612857443283225]
y_dir_V0 = [-0.6487021997069673, 0.5729056488889889, 0.5009636449548291]
z_dir_V0 = [0.6175423628255539, 0.011549577357211932, 0.7864528195503538]

custom_plane_V0 = cq.Plane(
    origin = [111.0, 222.0, 333.0],
    xDir = cq.Vector(*x_dir_V0),
    normal = cq.Vector(*z_dir_V0)
)

base_V0 = cq.Workplane(custom_plane_V0)
base_V0 = base_V0.moveTo(-300.0, 50.000000000000036)
base_V0 = base_V0.threePointArc((-241.42135623730948, 191.42135623730945), (-100.00000000000006, 250.0))
base_V0 = base_V0.lineTo(300.0, 250.0)
base_V0 = base_V0.lineTo(300.0, -50.00000000000006)
base_V0 = base_V0.threePointArc((241.4213562373095, -191.4213562373095), (100.00000000000006, -250.0))
base_V0 = base_V0.lineTo(-300.0, -250.0)
base_V0 = base_V0.lineTo(-300.0, 50.000000000000036)
base_V0.close()

# 扫掠路径
points_V0 = [
        (0, 0, 0),
        (0, 0, 18.0)
]

#构建扫掠路径
path_wire_V0 = build_path(points_V0, custom_plane_V0)
#执行扫掠
swept_V0 = base_V0.sweep(path_wire_V0, isFrenet = False, makeSolid = True, normal = cq.Vector(*z_dir_V0))
solids.append(swept_V0)


#===== 处理 V1 =====
#创建平面
x_dir_V1 = [0.4447773445345138, 0.8195399470031683, -0.3612857443283225]
y_dir_V1 = [-0.6487021997069673, 0.5729056488889889, 0.5009636449548291]
z_dir_V1 = [0.6175423628255539, 0.011549577357211932, 0.7864528195503538]

custom_plane_V1 = cq.Plane(
    origin = [111.0, 222.0, 333.0],
    xDir = cq.Vector(*x_dir_V1),
    normal = cq.Vector(*z_dir_V1)
)

base_V1 = cq.Workplane(custom_plane_V1)
base_V1 = base_V1.moveTo(19.999999999999993, 0.0)
base_V1 = base_V1.threePointArc((5.857864376269047, 5.857864376269051), (0.0, 19.999999999999996))
base_V1 = base_V1.lineTo(0.0, 50.0)
base_V1 = base_V1.lineTo(29.999999999999996, 50.0)
base_V1 = base_V1.threePointArc((44.14213562373095, 44.14213562373095), (50.0, 30.000000000000004))
base_V1 = base_V1.lineTo(50.0, 0.0)
base_V1 = base_V1.lineTo(19.999999999999993, 0.0)
base_V1.close()

# 扫掠路径
points_V1 = [
        (0, 0, 0),
        (0, 0, 18.0)
]

#构建扫掠路径
path_wire_V1 = build_path(points_V1, custom_plane_V1)
#执行扫掠
swept_V1 = base_V1.sweep(path_wire_V1, isFrenet = False, makeSolid = True, normal = cq.Vector(*z_dir_V1))
cuts.append(swept_V1)


#===== 处理 V2 =====
#创建平面
x_dir_V2 = [0.4447773445345138, 0.8195399470031683, -0.3612857443283225]
y_dir_V2 = [-0.6487021997069673, 0.5729056488889889, 0.5009636449548291]
z_dir_V2 = [0.6175423628255539, 0.011549577357211932, 0.7864528195503538]

custom_plane_V2 = cq.Plane(
    origin = [111.0, 222.0, 333.0],
    xDir = cq.Vector(*x_dir_V2),
    normal = cq.Vector(*z_dir_V2)
)

base_V2 = cq.Workplane(custom_plane_V2)
base_V2 = base_V2.moveTo(19.999999999999993, 55.0)
base_V2 = base_V2.threePointArc((5.857864376269047, 60.85786437626905), (0.0, 75.0))
base_V2 = base_V2.lineTo(0.0, 105.0)
base_V2 = base_V2.lineTo(30.0, 105.0)
base_V2 = base_V2.threePointArc((44.14213562373095, 99.14213562373095), (50.0, 85.0))
base_V2 = base_V2.lineTo(50.0, 55.0)
base_V2 = base_V2.lineTo(19.999999999999993, 55.0)
base_V2.close()

# 扫掠路径
points_V2 = [
        (0, 0, 0),
        (0, 0, 18.0)
]

#构建扫掠路径
path_wire_V2 = build_path(points_V2, custom_plane_V2)
#执行扫掠
swept_V2 = base_V2.sweep(path_wire_V2, isFrenet = False, makeSolid = True, normal = cq.Vector(*z_dir_V2))
cuts.append(swept_V2)


#===== 处理 V3 =====
#创建平面
x_dir_V3 = [0.4447773445345138, 0.8195399470031683, -0.3612857443283225]
y_dir_V3 = [-0.6487021997069673, 0.5729056488889889, 0.5009636449548291]
z_dir_V3 = [0.6175423628255539, 0.011549577357211932, 0.7864528195503538]

custom_plane_V3 = cq.Plane(
    origin = [111.0, 222.0, 333.0],
    xDir = cq.Vector(*x_dir_V3),
    normal = cq.Vector(*z_dir_V3)
)

base_V3 = cq.Workplane(custom_plane_V3)
base_V3 = base_V3.moveTo(75.0, 0.0)
base_V3 = base_V3.threePointArc((60.85786437626905, 5.857864376269049), (55.0, 19.999999999999996))
base_V3 = base_V3.lineTo(55.0, 50.0)
base_V3 = base_V3.lineTo(85.0, 50.0)
base_V3 = base_V3.threePointArc((99.14213562373095, 44.14213562373095), (105.0, 30.000000000000004))
base_V3 = base_V3.lineTo(105.0, 0.0)
base_V3 = base_V3.lineTo(75.0, 0.0)
base_V3.close()

# 扫掠路径
points_V3 = [
        (0, 0, 0),
        (0, 0, 18.0)
]

#构建扫掠路径
path_wire_V3 = build_path(points_V3, custom_plane_V3)
#执行扫掠
swept_V3 = base_V3.sweep(path_wire_V3, isFrenet = False, makeSolid = True, normal = cq.Vector(*z_dir_V3))
cuts.append(swept_V3)


#===== 处理 V4 =====
#创建平面
x_dir_V4 = [0.4447773445345138, 0.8195399470031683, -0.3612857443283225]
y_dir_V4 = [-0.6487021997069673, 0.5729056488889889, 0.5009636449548291]
z_dir_V4 = [0.6175423628255539, 0.011549577357211932, 0.7864528195503538]

custom_plane_V4 = cq.Plane(
    origin = [111.0, 222.0, 333.0],
    xDir = cq.Vector(*x_dir_V4),
    normal = cq.Vector(*z_dir_V4)
)

base_V4 = cq.Workplane(custom_plane_V4)
base_V4 = base_V4.moveTo(75.0, 55.0)
base_V4 = base_V4.threePointArc((60.85786437626905, 60.85786437626905), (55.0, 75.0))
base_V4 = base_V4.lineTo(55.0, 105.0)
base_V4 = base_V4.lineTo(85.0, 105.0)
base_V4 = base_V4.threePointArc((99.14213562373095, 99.14213562373095), (105.0, 85.0))
base_V4 = base_V4.lineTo(105.0, 55.0)
base_V4 = base_V4.lineTo(75.0, 55.0)
base_V4.close()

# 扫掠路径
points_V4 = [
        (0, 0, 0),
        (0, 0, 18.0)
]

#构建扫掠路径
path_wire_V4 = build_path(points_V4, custom_plane_V4)
#执行扫掠
swept_V4 = base_V4.sweep(path_wire_V4, isFrenet = False, makeSolid = True, normal = cq.Vector(*z_dir_V4))
cuts.append(swept_V4)


#===== 处理 V5 =====
#创建平面
x_dir_V5 = [0.4447773445345138, 0.8195399470031683, -0.3612857443283225]
y_dir_V5 = [-0.6487021997069673, 0.5729056488889889, 0.5009636449548291]
z_dir_V5 = [0.6175423628255539, 0.011549577357211932, 0.7864528195503538]

custom_plane_V5 = cq.Plane(
    origin = [111.0, 222.0, 333.0],
    xDir = cq.Vector(*x_dir_V5),
    normal = cq.Vector(*z_dir_V5)
)

base_V5 = cq.Workplane(custom_plane_V5)
base_V5 = base_V5.moveTo(170.0, 150.0)
base_V5 = base_V5.threePointArc((155.85786437626905, 155.85786437626905), (150.0, 170.0))
base_V5 = base_V5.lineTo(150.0, 200.0)
base_V5 = base_V5.lineTo(180.0, 200.0)
base_V5 = base_V5.threePointArc((194.14213562373095, 194.14213562373095), (200.0, 180.0))
base_V5 = base_V5.lineTo(200.0, 150.0)
base_V5 = base_V5.lineTo(170.0, 150.0)
base_V5.close()

# 扫掠路径
points_V5 = [
        (0, 0, 10.0),
        (0, 0, 18.0)
]

#构建扫掠路径
path_wire_V5 = build_path(points_V5, custom_plane_V5)
#执行扫掠
swept_V5 = base_V5.sweep(path_wire_V5, isFrenet = False, makeSolid = True, normal = cq.Vector(*z_dir_V5))
cuts.append(swept_V5)


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
cq.exporters.export(final_model, './test/test818.stl', exportType='STL')
print("模型已导出为test818.stl")
