import cadquery as cq
import numpy as np
from jupyter_cadquery.cadquery import show

# 1. 定义椭圆弧参数
params = {
    "major_radius": 100.0,
    "minor_radius": 50.0,
    "center": (0.0, -350.0),
    "start_angle": -0.588,  # 弧度制 ≈ -33.7°
    "end_angle": 2.214      # 弧度制 ≈ 126.8°
}

# 2. 创建完整椭圆（长轴沿X轴）
ellipse = (
    cq.Workplane("XY")
    .ellipse(params["major_radius"], params["minor_radius"])
    .translate(params["center"])
)

# 3. 构造扇形切割工具（覆盖不需要的部分）
sector = (
    cq.Workplane("XY")
    .moveTo(params["center"][0], params["center"][1])  # 圆心
    .radiusArc(
        (
            params["center"][0] + params["major_radius"] * np.cos(params["end_angle"]),
            params["center"][1] + params["minor_radius"] * np.sin(params["end_angle"])
        ),
        params["major_radius"]  # 控制扇形半径
    )
    .lineTo(params["center"][0], params["center"][1])  # 返回圆心
    .close()
)

# 4. 切割椭圆，保留所需弧段
ellipse_arc = ellipse.intersect(sector)

# 5. 显示结果
show(ellipse,height=400,grid = True)