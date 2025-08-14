# Auto-generated CadQuery script
import cadquery as cq
import numpy as np
from scipy.spatial.transform import Rotation as R

# Profile截面（5边形）
def build_profile():
    profile = cq.Workplane("XY")
    profile = profile.moveTo(0, 0)
    profile = profile.threePointArc((2.0, -0.263304995174793), (4, 0))
    profile = profile.lineTo(6, 3)
    profile = profile.threePointArc((7.838093094884382, 3.00192268100321), (3, 5))
    profile = profile.lineTo(0, 3)
    profile = profile.threePointArc((-0.40192378864668354, 1.4999999999999998), (0, 0))
    return profile.close()

# 扫掠路径（3个点）
def build_path():
#    path = cq.Workplane("XY").moveTo(0, 0, 0)
#    path = path.workplane(origin=(0,0,0)).lineTo(5, 5, 5)
#    path = path.workplane(origin=(0,5,5)).lineTo(0,5,50)

    points = [
        (0, 0, 0),
        (0, 5, 5),
        (10,10,10)
    ]
    
    result = cq.Workplane("XY").polyline(points)
    return result.wire()

# 构建最终模型
profile = build_profile()

path = build_path()

model = profile.sweep(path, isFrenet=False,makeSolid=True)

# 应用变换（旋转和平移）
#rotation = R.from_quat([0.707, 0, 0, 0.707]).as_euler('xyz', degrees=True)
#translation = [10, 5, 0]
#model = model.rotate((0,0,0), (1,0,0), rotation[0])\
#          .rotate((0,0,0), (0,1,0), rotation[1])\
#          .rotate((0,0,0), (0,0,1), rotation[2])\
#          .translate(translation)

# 导出结果
#cq.exporters.export(model, "output.step")
cq.exporters.export(model, 'output.stl', exportType='STL')
