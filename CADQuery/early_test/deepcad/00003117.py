import cadquery as cq
# Generating a workplane for sketch 0
wp_sketch0 = cq.Workplane(cq.Plane(cq.Vector(0.0, -0.75, 0.0), cq.Vector(3.749399456654644e-33, 1.0, -6.123233995736766e-17), cq.Vector(1.0, 0.0, 6.123233995736766e-17)))
loop0=wp_sketch0.moveTo(0.7578947368421053, 0.0).circle(0.7578947368421053)
loop1=wp_sketch0.moveTo(0.7578947368421053, 0.0).circle(0.25263157894736843)
solid0=wp_sketch0.add(loop0).add(loop1).extrude(-0.0234375)
solid=solid0
cq.exporters.export(solid, "./00003117.stl",exportType="STL")