# Auto-generated CadQuery script
import cadquery as cq
import numpy as np
from scipy.spatial.transform import Rotation as R

# Profile截面（8边形）
def build_profile():
    profile = cq.Workplane("XY")
    profile = profile.moveTo(-454.53, 18.21)
    profile = profile.lineTo(-355.47, 166.79)
    profile = profile.threePointArc((-347.01747633839705, 337.8427418138516), (-200, 250))
    profile = profile.lineTo(300, 250)
    profile = profile.threePointArc((494.0424302579047, 162.69495350526972), (500, -50))
    profile = profile.lineTo(300, -250)
    profile = profile.lineTo(-300, -250)
    profile = profile.lineTo(-442.03, -107.97)
    profile = profile.threePointArc((-470.77487817547114, -47.1084512378617), (-454.53, 18.21))
    return profile.close()

# 扫掠路径（2个点）
def build_path():

    points = [
        (0, 0, 0),
        (0, 0, 18)
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
