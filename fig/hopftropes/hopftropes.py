# Fig1_main.py: instrucions to generate the first figure in the report.
# Integrates several field lines of the Hopf field.
# Plots the lines in colors using different colormaps
#
#
#

import os, sys, inspect       # For importing the submodules in a platform-independend robust way
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import importlib
import bpy
from functools import partial # create new funtions from old functions (and strip the kwargs)
code_folder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../../code")))
if code_folder not in sys.path:
     sys.path.insert(0, code_folder)

import integrate as ig
import BlenDaViz as bz

colormaps = ['Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
            'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
            'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn']

def mystreamline(xx, **kwargs):
    def function(xx): return ig.BHopf(xx,w1=1, w2=1)
    return ig.stream(xx=xx,vvfn=function,
        tol= 1e-7, hMin=1e-8, iterMax=50000, lMax = 50
        ).tracers


radii= np.array([1.1,1.5,2.,2.5,3. ])
num_circles = 11
vecs = []

fn=partial(ig.BHopf, w1=1, w2=1)

for num, radius in enumerate(radii):
    cmap = plt.cm.get_cmap(colormaps[num])
    norm = plt.Normalize(vmin=0, vmax=num_circles)
    s_m = plt.cm.ScalarMappable(cmap = cmap, norm = norm)
    for j in range(num_circles):
        print(num, j)
        angle = np.linspace(0,2*np.pi, num_circles+1)[j] # on the circle, last element is first
        color = s_m.to_rgba(j)[:-1] # throw out the a of rgba
        xx=radius*np.array([np.sin(angle),np.cos(angle),0])
        streamline = mystreamline(xx)
        bz.plot(streamline[:,0], streamline[:,1], streamline[:,2],
        radius=0.01,  color=(.5,.5,.5,1))
        isotropeforward = ig.stream(xx, vvfn=ig.Hopf_isotropes,
        tol= 1e-7, hMin=1e-6, iterMax=1000, lMax = 50).tracers
        bz.plot(isotropeforward[:,0], isotropeforward[:,1], isotropeforward[:,2],
        radius=0.02,  color=color)
        isotropeback = ig.stream(xx, vvfn=ig.Hopf_isotropes, intdir='back',
        tol= 1e-7, hMin=1e-6, iterMax=1000, lMax = 50).tracers
        bz.plot(isotropeback[:,0], isotropeback[:,1], isotropeback[:,2],
        radius=0.02,  color=color)
        vecs.append(bz.vec(xx, fn(xx), length=1.0, color=color))


bpy.data.scenes['Scene'].render.filepath = '../hopftropes.png'
bpy.ops.render.render(write_still=True)
