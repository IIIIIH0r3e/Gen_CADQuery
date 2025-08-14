# Auto-generated CadQuery script
import cadquery as cq
import numpy as np

from cadquery.func import *

#创建工作平面,应用初始旋转和平移
x_dir = [1.0000000000000002, 0.0, 0.0]
y_dir = [0.0, 0.0, 1.0000000000000002]
z_dir = [0.0, 1.0000000000000002, 0.0]

custom_plane = cq.Plane(
    origin = [100, 100, 100],
    xDir = cq.Vector(*x_dir),
    normal = cq.Vector(*z_dir)
)

base = cq.Workplane(custom_plane)
base = base.moveTo(-454.53, 18.21)
base = base.lineTo(-355.47, 166.79)
base = base.threePointArc((-347.01747633839705, 337.8427418138516), (-200, 250))
base = base.lineTo(300, 250)
base = base.threePointArc((494.0424302579047, 162.69495350526972), (500, -50))
base = base.lineTo(300, -250)
base = base.lineTo(-300, -250)
base = base.lineTo(-442.03, -107.97)
base = base.threePointArc((-470.77487817547114, -47.1084512378617), (-454.53, 18.21))
base.close()

#孔洞截面
#Hole 0
base = base.moveTo(20,20)
base = base.threePointArc((50.0,20.0),(50,50))
base = base.threePointArc((20.0,50.0),(20,20))
base = base.close()
#Hole 1
base = base.moveTo(0,0)
base = base.threePointArc((-50.0,0.0),(-50,-50))
base = base.threePointArc((0.0,-50.0),(0,0))
base = base.close()
# 扫掠路径（2个点）
def build_path():

    points = [
        (0, 0, 0),
        (0, 0, 50)
    ]

    result = cq.Workplane(custom_plane).polyline(points)

    return result.wire()

#spine = spline([(0, 0, 0), (-200, -200, 500)], tgts=[(0, 0, 1), (0, 1, 0)])

#执行扫掠
model = base.sweep(build_path(), isFrenet=False,makeSolid=True)

# 导出结果
#cq.exporters.export(model, "output.step")
cq.exporters.export(model, 'output.stl', exportType='STL')  
