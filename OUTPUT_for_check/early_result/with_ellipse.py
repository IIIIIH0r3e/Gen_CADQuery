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
    origin = [0.0, 0.0, 0.0],
    xDir = cq.Vector(*x_dir_V0),
    normal = cq.Vector(*z_dir_V0)
)

base_V0 = cq.Workplane(custom_plane_V0)
base_V0 = base_V0.moveTo(-300.0, 200.0)
base_V0 = base_V0.lineTo(-250.0, 250.0)
base_V0 = base_V0.lineTo(250.0, 250.0)
base_V0 = base_V0.threePointArc((285.3553390593274, 235.35533905932738), (300.0, 200.0))
base_V0 = base_V0.lineTo(300.0, -200.0)
base_V0 = base_V0.threePointArc((340.56210925877804, -279.23551423318827), (252.5658350974743, -265.8113883008419))
base_V0 = base_V0.lineTo(83.20502943378435, -322.2649901887385)

#椭圆弧
base_V0 = base_V0.ellipseArc(100.0, 50.0, rotation_angle = 0.0, angle2 = 33.690067525979806, angle1 = -126.86989764584402, startAtCurrent = True, sense = -1)
base_V0 = base_V0.lineTo(-150.00000000000003, -450.0)
base_V0 = base_V0.threePointArc((-294.97911956540634, -420.56757880486725), (-425.0, -350.0))
base_V0 = base_V0.lineTo(-300.0, -250.0)
base_V0 = base_V0.lineTo(-300.0, 200.0)
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
cq.exporters.export(final_model, './test/ellipse.stl', exportType='STL')
print("模型已导出")
