# Hopfnulls.py: creates the field lines of the Hopf fibration in a constant guide field.
#
#
#To change the angle and strength of the guide field change the variables on lines 30-32
#
# coded by Christopher Berg Smiet on Oktober 16
# csmiet@pppl.gov
#
import os, sys, inspect       # For importing the submodules in a platform-independend robust way
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib
import bpy                    # This module is only available inside of Blender's version of python, comment when debugging
from functools import partial # create new funtions from old functions (and strip the kwargs)

# Make sure that the path to BlenDaViz and the integration library are in the front of the path.
code_folder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../../code")))
if code_folder not in sys.path:
     sys.path.insert(0, code_folder)

import integrate as ig
import BlenDaViz as bz


#guide field properties:
R = 0.3
Phi = 0.
Theta = np.pi



fn = partial(ig.BHopf_guide_RPT, R=R, Phi=Phi, Theta = Theta)

#generate the starting points of the streamline
nulls = ig.Hopf_nulls(R, Phi, Theta)
npoints=60
startpoints = []
null1 = ig.zeroPoints(nulls[0], ig.Dipole(nulls[0]), sign=-1, npoints=npoints)
null2 = ig.zeroPoints(nulls[1], ig.Dipole(nulls[1]), sign=1, npoints=npoints)


n1spine = ig.stream_multi(null1.fanpoints, vvfn=fn, tol=1e-7, iterMax=300000,  hMin=2e-7, lMax = 100, intdir='forward')
n1fan = ig.stream_multi(null1.fanpoints, vvfn=fn, tol=1e-8, iterMax=300000,  hMin=2e-7, lMax = 100, intdir='back')

n2spine = ig.stream_multi(null2.fanpoints, vvfn=fn, tol=1e-8, iterMax=300000,  hMin=2e-7, lMax = 100, intdir='back')
n2fan = ig.stream_multi(null2.fanpoints, vvfn=fn, tol=1e-8, iterMax=300000,  hMin=2e-6, lMax = 100, intdir='forward')

fieldlines = []
for stream in n1fan:
    fieldlines.append(bz.plot(stream.x, stream.y, stream.z, color = (0.        , 0.37109375, 0.49609375) , radius=0.01))

for stream in n1spine:
    fieldlines.append(bz.plot(stream.x, stream.y, stream.z, color = 'r', radius=0.01))

for stream in n2fan:
    fieldlines.append(bz.plot(stream.x, stream.y, stream.z, color =  (.639, .757, .678), radius=0.01))

for stream in n2spine:
    fieldlines.append(bz.plot(stream.x, stream.y, stream.z, color = 'r', radius=0.01))


bpy.data.scenes['Scene'].render.filepath = '../Hopfnulls.png'
bpy.ops.render.render(write_still=True)
