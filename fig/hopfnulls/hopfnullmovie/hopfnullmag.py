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
code_folder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../../../code")))
if code_folder not in sys.path:
     sys.path.insert(0, code_folder)

import integrate as ig
import BlenDaViz as bz



#guide field properties:
Rmax = 0.2
#Rs = np.concatenate((Rmax*np.ones(45)))
Rs = np.linspace(0.0001, 0.4, 45)
Phi_int=0.6
#Phis = np.linspace(Phi_int, 1.675, 45)
Phis = 1.2107*np.ones(45)
Thetas =  np.pi*np.ones(45)

First= True

isotropestart= ig.Hopf_nulls(0.01, 1.2107, np.pi)[1]
isotropestream = ig.stream(isotropestart, vvfn=ig.Hopf_isotropes, tol=1e-7, iterMax=3000,  hMin=2e-7, lMax = 100, intdir='forward')
bz.plot(isotropestream.x, isotropestream.y, isotropestream.z, color =  'g', radius=0.01)

for framenum, (R, Phi, Theta) in reversed(list( enumerate(zip(Rs, Phis, Thetas)))):
    fn = partial(ig.BHopf_guide_RPT, R=R, Phi=Phi, Theta = Theta)
#    if framenum <42:
#        print('break for framenum {}'.format(framenum))
#        continue #but skip this iteration

#generate the starting points of the streamline
    nulls = ig.Hopf_nulls(R, Phi, Theta)
    npoints=60
    startpoints = []
    null1 = ig.zeroPoints(nulls[0], ig.Dipole(nulls[0]), sign=-1, dist=0.01, npoints=npoints, radius = 0.01)
    null2 = ig.zeroPoints(nulls[1], ig.Dipole(nulls[1]), sign=1, dist = 0.01, npoints=npoints, radius = 0.01)

    n1spine = ig.stream_multi(null1.fanpoints, vvfn=fn, tol=1e-7, iterMax=3000,  hMin=2e-7, lMax = 100, intdir='forward')
    n1fan = ig.stream_multi(null1.fanpoints, vvfn=fn, tol=1e-8, iterMax=3000,  hMin=2e-7, lMax = 100, intdir='back')

    n2spine = ig.stream_multi(null2.fanpoints, vvfn=fn, tol=1e-8, iterMax=3000,  hMin=2e-7, lMax = 100, intdir='back')
    n2fan = ig.stream_multi(null2.fanpoints, vvfn=fn, tol=1e-8, iterMax=3000,  hMin=2e-6, lMax = 100, intdir='forward')
    if First:
        n1fanlines = []
        for stream in n1fan:
            n1fanlines.append(bz.plot(stream.x, stream.y, stream.z, color = (0.        , 0.37109375, 0.49609375) , radius=0.01))
        n1spinelines = []
        for stream in n1spine:
            n1spinelines.append(bz.plot(stream.x, stream.y, stream.z, color = 'r', radius=0.01))
        n2fanlines = []
        for stream in n2fan:
            n2fanlines.append(bz.plot(stream.x, stream.y, stream.z, color =  (.639, .757, .678), radius=0.01))
        n2spinelines = []
        for stream in n2spine:
            n2spinelines.append(bz.plot(stream.x, stream.y, stream.z, color = 'r', radius=0.01))
        First = False
    else:
        for num, stream in enumerate(n1fan):
            n1fanlines[num].x = stream.x
            n1fanlines[num].y = stream.y
            n1fanlines[num].z = stream.z
            n1fanlines[num].plot()
        for num, stream in enumerate(n1spine):
            n1spinelines[num].x = stream.x
            n1spinelines[num].y = stream.y
            n1spinelines[num].z = stream.z
            n1spinelines[num].plot()
        for num, stream in enumerate(n2fan):
            n2fanlines[num].x = stream.x
            n2fanlines[num].y = stream.y
            n2fanlines[num].z = stream.z
            n2fanlines[num].plot()
        for num, stream in enumerate(n2spine):
            n2spinelines[num].x = stream.x
            n2spinelines[num].y = stream.y
            n2spinelines[num].z = stream.z
            n2spinelines[num].plot()



    bpy.data.scenes['Scene'].render.filepath = 'magnitude/hopfnullmovie{}.png'.format(framenum)
    bpy.ops.render.render(write_still=True)
