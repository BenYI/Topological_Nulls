# posindex_start.py: generate a plot of the vector field around a 3d magnetic null.
# A yellow transparend sphere is located at the origin, and the vector field of the
# null is shown by it's integral curves, as well as vectors located on the surface
# of a ball around the null
#
#
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

def isofield(xx):
    return xx/np.sqrt(np.sum(xx**2))**3

startlen = .35

# generate the points at which vectors are to be evaluated
ncirc=10
ncircvec=20
vecpoints = [[np.array((np.sqrt(1-z**2)*np.cos(t), np.sqrt(1-z**2)*np.sin(t), z))
                        for t in np.linspace(np.pi, 3*np.pi, ncircvec+1)[:ncircvec]]
                            for z in np.cos(np.linspace(0,np.pi,ncirc+2)[1:-1])]
vecpoints.append([np.array((0,0,1))])
vecpoints.append([np.array((0,0,-1))])

#generate the points from which streamlines are to be traced
nstreams=20
streampoints = []
for r in np.linspace(0.01, 0.5, 3):
    streampoints.extend(ig.circlePoints(np.array((0,0,1)), radius = r, slide=8,
        npoints = nstreams, rot=50*r))
    streampoints.extend(ig.circlePoints(np.array((0,0,1)), radius = r, slide=-8,
        npoints = nstreams, rot=50*r))

fn=partial(ig.ZeroField, index=1)
#def fn(xx): return np.array((0,0,1))

streams = ig.stream_multi(streampoints, vvfn=fn, tol=1e-7, iterMax=1000000, intdir = 'back')
lines = []
for stream in streams:
    print('plotting stream...')
    lines.append(bz.plot(stream.x, stream.y, stream.z, color = (1,1,1), radius=0.01))

isotropes = []
vecs = []
vc = cm.get_cmap('plasma', ncirc) # vertical colors
for num1, veccirc in enumerate(vecpoints):
    cdict = {'red':   [[0.0,  vc(num1)[0], vc(num1)[0]],
                       [1.0,  .5, .5]],
             'green': [[0.0,  vc(num1)[1], vc(num1)[1]],
                       [1.0,  .5, .5]],
             'blue':  [[0.0,  vc(num1)[2], vc(num1)[2]],
                       [1.0,  .5, .5]]}                  #colordict that starts with plamsa colors and ends at grey
    cmap = matplotlib.colors.LinearSegmentedColormap('map'+str(num1), segmentdata=cdict)
    norm = plt.Normalize(vmin=0, vmax=ncircvec)
    s_m = plt.cm.ScalarMappable(cmap = cmap, norm = norm)
    tropecircback = ig.stream_multi(veccirc, vvfn=isofield, tol=1e-7, iterMax=1000000, intdir = 'back')
    tropecircforward = ig.stream_multi(veccirc, vvfn=isofield, tol=1e-7, iterMax=1000000, intdir = 'forward')
    for num2, (forstream, backstream) in enumerate(zip(tropecircforward, tropecircback)):
        #print(num2,point)
        color = s_m.to_rgba(num2)
        isotropes.append(bz.plot(forstream.x, forstream.y, forstream.z, color=color, radius=0.01))
        isotropes.append(bz.plot(backstream.x, backstream.y, backstream.z, color=color, radius=0.01))
    for num2, point in enumerate(veccirc):
        #print(num2,point)
        point =  point
        color = s_m.to_rgba(num2)[:-1] # throw out the a of rgba
        vecs.append(bz.vec(point, -fn(point), length=0.5, color=color))



bpy.data.scenes['Scene'].render.filepath = '../nulltropesneg.png'
bpy.ops.render.render(write_still=True)
