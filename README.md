# Topological_Nulls

Code to completely generate the poster: 'Magnetic Nulls from the Topological Perspective' presented at APS DPP 2019 by Ben Israeli et al. 

Prerequisites: Blender, LaTeX (including the LaTeX packages: qrcode, beamer, beamerposter)

![null](fig/posindex/posindex_start.png?raw=true "Illustration of a null with positive topological index")

Setup: 
download this repo *recursively*:
```
git clone --recurse-submodules git@github.com:BenYI/Topological_Nulls.git
```
Install Blender (for ubuntu use apt-get install, for CentOS yum install).
```
Pacman -S blender
```
Check blender version:
``` 
blender -v
```
if you have blender version 2.79:
```
cd Topological_Nulls/code/BlenDaViz
git checkout master
```

To make just the poster, go to the root folder of your repository and type: 
```
make poster
```

To render all of the images on the poster use: 
```
make
```
This will take approximately 1.5 cpu-hrs on a modern machine to generate all the images. (On a quad core device it should be ready in approximately 20-30 minutes). 



As of the current version I am unable to link the earth image texture to the object, this must be done by hand in blender. 
If you see a magenta shpere in some of the images, open the scene_earth.blend in the respective image folders in blender, and link to the texture in /fig/scenes/earth.jpg.
