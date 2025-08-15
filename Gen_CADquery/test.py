import cadquery as cq
# Generating a workplane for sketch 0
wp_sketch0 = cq.Workplane(cq.Plane(cq.Vector(-0.3359375, 0.453125, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop0=wp_sketch0.moveTo(0.3367598684210526, -0.44901315789473684).lineTo(0.6735197368421052, 0.0).threePointArc((0.5827915773209776, 0.2890819688050377), (0.3367598684210526, 0.11225328947368421)).threePointArc((0.09072815952112763, 0.2890819688050377), (0.0, 0.0)).close()
solid0=wp_sketch0.add(loop0).extrude(0.1875)


# Generating a workplane for sketch 1
wp_sketch1 = cq.Workplane(cq.Plane(cq.Vector(-0.15, 0.55, 0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop1=wp_sketch1.moveTo(0.3367598684210526, -0.44901315789473684).lineTo(0.6735197368421052, 0.0).threePointArc((0.5827915773209776, 0.2890819688050377), (0.3367598684210526, 0.11225328947368421)).threePointArc((0.09072815952112763, 0.2890819688050377), (0.0, 0.0)).close()
solid1=wp_sketch1.add(loop1).extrude(0.1875)

solid=solid0.union(solid1) - solid0.intersect(solid1)


cq.exporters.export(solid, "./heart.stl")