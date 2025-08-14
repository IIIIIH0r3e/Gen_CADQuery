import cadquery as cq
from cadquery.func import *
from cadquery.vis import *

c = circle(1).toSplines().close()
spine = spline([(0, 0, 0), (-3, -3, 5)], tgts=[(0, 0, 1), (0, -1, 0)])
f = sweep(c,spine,makeSolid = True)

cq.exporters.export(f, 'output.stl', exportType='STL')