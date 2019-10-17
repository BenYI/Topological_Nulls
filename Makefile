default:   images poster

poster:
	pdflatex -synctex=1 -interaction=nonstopmode -enable-write18 nulls.tex
	bibtex nulls
	pdflatex -synctex=1 -interaction=nonstopmode  -enable-write18 nulls.tex
	pdflatex -synctex=1 -interaction=nonstopmode -enable-write18 nulls.tex

images:  nulltropes onlyhopf hopftropes mainfig posindex negindex separatrix_dipole 

nulltropes:
	cd fig/nulltropes; blender -b scene.blend -P nulltropes.py

hopftropes:
	cd fig/hopftropes; blender -b scene.blend -P hopftropes.py; blender -b scene.blend -P onlyhopf.py

onlyhopf:
	cd fig/hopftropes; blender -b scene.blend -P onlyhopf.py

merger:
	cd fig/merger; blender -b scene.blend -P merger.py

mainfig:
	cd fig/Mainfig; blender -b scene_earth.blend -P mainfig.py

posindex:
	cd fig/posindex; blender -b scene_ball_small.blend -P posindex_start.py; blender -b scene_ball_small.blend -P posindex_end.py

negindex:
	cd fig/negindex; blender -b scene_ball_small.blend -P negindex_start.py; blender -b scene_ball_small.blend -P negindex_end.py

separatrix_dipole:
	cd fig/separatrix_dipole; blender -b scene_earth_centered.blend -P separatrix_dipole.py


