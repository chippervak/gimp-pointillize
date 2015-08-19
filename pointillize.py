#!/usr/bin/env python

# GIMP Python plug-in template.

import os
from gimpfu import *

def pointillize(img, imagefmt, cell_size) :
    filename = img.filename
    pdb.gimp_image_clean_all(img)


register(
    "python_fu_pointillize",
    "Pointillize",
    "Longer description of doing stuff",
    "Chip Brewer",
    "Chip Brewer",
    "2015",
    "Pointillize",
    "*",      # Alternately use RGB, RGB*, GRAY*, INDEXED etc.
    [
        (PF_IMAGE, "image", "Input image", None),
        (PF_STRING, "cell_size", "Cell size?", "5")
    ],
    [],
    pointillize, menu="<Image>/Filters/Artistic")

main()
