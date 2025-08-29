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
x_dir_V0 = [0.9999999999999998, 0.0, 0.0]
y_dir_V0 = [0.0, -0.42319915997318586, 0.9060366830310953]
z_dir_V0 = [0.0, -0.9060366830310953, -0.42319915997318586]

custom_plane_V0 = cq.Plane(
    origin = [500.0, 0.0, 0.0],
    xDir = cq.Vector(*x_dir_V0),
    normal = cq.Vector(*z_dir_V0)
)

base_V0 = cq.Workplane(custom_plane_V0)
base_V0 = base_V0.moveTo(-300.0, 50.000000000000036)
base_V0 = base_V0.threePointArc((-241.42135623730948, 191.42135623730945), (-100.00000000000006, 250.0))
base_V0 = base_V0.lineTo(299.9999999999999, 250.00000000000009)
base_V0 = base_V0.threePointArc((366.98729810778065, 3.8211354595198523e-14), (300.0, -250.0))
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
x_dir_V1 = [0.9999999999999998, 0.0, 0.0]
y_dir_V1 = [0.0, -0.42319915997318586, 0.9060366830310953]
z_dir_V1 = [0.0, -0.9060366830310953, -0.42319915997318586]

custom_plane_V1 = cq.Plane(
    origin = [500.0, 0.0, 0.0],
    xDir = cq.Vector(*x_dir_V1),
    normal = cq.Vector(*z_dir_V1)
)

base_V1 = cq.Workplane(custom_plane_V1)
base_V1 = base_V1.moveTo(0.0, 0.0)
base_V1 = base_V1.lineTo(-1.273756467240565e-14, 50.0)
base_V1 = base_V1.threePointArc((-35.35533905932738, 135.35533905932738), (50.0, 100.0))
base_V1 = base_V1.lineTo(100.0, 100.0)
base_V1 = base_V1.lineTo(100.0, 49.999999999999986)
base_V1 = base_V1.threePointArc((85.35533905932738, 14.644660940672622), (50.000000000000014, 0.0))
base_V1 = base_V1.lineTo(0.0, 0.0)
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
x_dir_V2 = [0.23697287233094833, 0.9715162673775566, 0.0]
y_dir_V2 = [-0.9715162673775566, 0.23697287233094833, 0.0]
z_dir_V2 = [0.0, 0.0, 1.0]

custom_plane_V2 = cq.Plane(
    origin = [0.0, 0.0, 400.0],
    xDir = cq.Vector(*x_dir_V2),
    normal = cq.Vector(*z_dir_V2)
)

base_V2 = cq.Workplane(custom_plane_V2)
base_V2 = base_V2.moveTo(-300.0, 200.0)
base_V2 = base_V2.lineTo(-250.0, 250.0)
base_V2 = base_V2.lineTo(250.0, 250.0)
base_V2 = base_V2.threePointArc((285.3553390593274, 235.35533905932738), (300.0, 200.0))
base_V2 = base_V2.lineTo(300.0, -200.0)
base_V2 = base_V2.threePointArc((340.56210925877804, -279.23551423318827), (252.5658350974743, -265.8113883008419))
base_V2 = base_V2.lineTo(83.20502943378435, -322.2649901887385)

#椭圆弧
base_V2 = base_V2.ellipseArc(100.0, 50.0, rotation_angle = 0.0, angle2 = 33.690067525979806, angle1 = -126.86989764584402, startAtCurrent = True, sense = -1)
base_V2 = base_V2.lineTo(-150.00000000000003, -450.0)
base_V2 = base_V2.threePointArc((-294.97911956540634, -420.56757880486725), (-425.0, -350.0))
base_V2 = base_V2.lineTo(-300.0, -250.0)
base_V2 = base_V2.lineTo(-300.0, 200.0)
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
solids.append(swept_V2)


#===== 处理 V3 =====
#创建平面
x_dir_V3 = [1.0, 0.0, 0.0]
y_dir_V3 = [0.0, 1.0, 0.0]
z_dir_V3 = [0.0, 0.0, 1.0]

custom_plane_V3 = cq.Plane(
    origin = [-800.0, 0.0, 0.0],
    xDir = cq.Vector(*x_dir_V3),
    normal = cq.Vector(*z_dir_V3)
)

base_V3 = cq.Workplane(custom_plane_V3)
base_V3 = base_V3.moveTo(-300.0, 50.000000000000036)
base_V3 = base_V3.threePointArc((-241.42135623730948, 191.42135623730945), (-100.00000000000006, 250.0))
base_V3 = base_V3.lineTo(300.0, 250.0)
base_V3 = base_V3.lineTo(300.0, -250.0)
base_V3 = base_V3.lineTo(-300.0, -250.0)
base_V3 = base_V3.lineTo(-300.0, 50.000000000000036)
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
solids.append(swept_V3)


#===== 处理 V4 =====
#创建平面
x_dir_V4 = [1.0, 0.0, 0.0]
y_dir_V4 = [0.0, 1.0, 0.0]
z_dir_V4 = [0.0, 0.0, 1.0]

custom_plane_V4 = cq.Plane(
    origin = [-800.0, 0.0, 0.0],
    xDir = cq.Vector(*x_dir_V4),
    normal = cq.Vector(*z_dir_V4)
)

base_V4 = cq.Workplane(custom_plane_V4)
base_V4 = base_V4.moveTo(0.0, 0.0)
base_V4 = base_V4.lineTo(0.0, 50.0)
base_V4 = base_V4.threePointArc((14.64466094067263, 85.35533905932736), (49.999999999999986, 100.0))
base_V4 = base_V4.lineTo(100.0, 100.0)
base_V4 = base_V4.lineTo(100.00000000000001, 0.0)
base_V4 = base_V4.threePointArc((50.00000000000002, -13.397459621556152), (0.0, 0.0))
base_V4.close()

# 扫掠路径
points_V4 = [
        (0, 0, 16.0),
        (0, 0, 18.0)
]

#构建扫掠路径
path_wire_V4 = build_path(points_V4, custom_plane_V4)
#执行扫掠
swept_V4 = base_V4.sweep(path_wire_V4, isFrenet = False, makeSolid = True, normal = cq.Vector(*z_dir_V4))
cuts.append(swept_V4)


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
cq.exporters.export(final_model, './muti-Vi.stl', exportType='STL')
print("模型已导出")
