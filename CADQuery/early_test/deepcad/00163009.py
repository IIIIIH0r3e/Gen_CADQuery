import cadquery as cq
# Generating a workplane for sketch 0
wp_sketch0 = cq.Workplane(cq.Plane(cq.Vector(0.0, 0.0, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))       #第三参数决定拉伸方向，草图在另两个轴构成的平面
loop0=wp_sketch0.moveTo(0.078125, 0.0).lineTo(0.078125, 0.006578947368421052).lineTo(0.006578947368421052, 0.006578947368421052).lineTo(0.006578947368421052, 0.078125).lineTo(0.0, 0.078125).lineTo(0.0, 0.0).close()
solid0=wp_sketch0.add(loop0).extrude(0.75)
solid=solid0
cq.exporters.export(solid, "./00163009.stl",exportType="STL")