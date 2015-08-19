#!/usr/bin/env python

# GIMP Python plug-in template.

import os
import math
from gimpfu import *

def pointillize(img, cell_size) :
    # Indicates that the process has started.
    gimp.progress_init("Pointillizing " + layer.name + "...")
    
    # Set up an undo group, so the operation will be undone in one step.
    pdb.gimp_image_undo_group_start(img)
    
    # Get the layer position.
    pos = 0;
    for i in range(len(img.layers)):
        if(img.layers[i] == layer):
            pos = i
    
    # Create a new layer to save the results (otherwise is not possible to undo the operation).
    newLayer = gimp.Layer(img, layer.name + " temp", layer.width, layer.height, layer.type, layer.opacity, layer.mode)
    img.add_layer(newLayer, pos)
    layerName = layer.name
    
    # Clear the new layer.
    pdb.gimp_edit_clear(newLayer)
    newLayer.flush()
    
    # Create a pointillized image.
    try:
        # Calculate the number of tiles.
        tn = int(layer.width / 64)
        if(layer.width % 64 > 0):
            tn += 1
        tm = int(layer.height / 64)
        if(layer.height % 64 > 0):
            tm += 1
        
        cellSize2 = cell_size * cell_size
        
        cellCount = 2.5 * layer.width * layer.height / cellSize2
        
        cols = math.sqrt(cellCount * layer.width / 8 / layer.height)
        rows = cols * layer.height / layer.width
        
        for c in range(cellCount):
            x = random.randint(0, layer.width - 1)
            y = random.randint(0, layer.height - 1)

#From the sameple.
        # Iterate over the tiles.
        for i in range(tn):
            for j in range(tm):
                # Update the progress bar.
                gimp.progress_update(float(i*tm + j) / float(tn*tm))
        
                # Get the tiles.
                srcTile = layer.get_tile(False, j, i)
                dstTile = newLayer.get_tile(False, j, i)
        
                # Iterate over the pixels of each tile.
                for x in range(srcTile.ewidth):
                    for y in range(srcTile.eheight):
                        # Get the pixel and calculate his gray value.
                        pixel = srcTile[x,y]
                        gray = (ord(pixel[0]) + ord(pixel[1]) + ord(pixel[2]))/3
                        res = chr(gray) + chr(gray) + chr(gray)
                        
                        # If the image has an alpha channel (or any other channel) copy his values.
                        if(len(pixel) > 3):
                            for k in range(len(pixel)-3):
                                res += pixel[k+3]
                                
                        # Save the value in the result layer.
                        dstTile[x,y] = res

#the rest is probably fine
        
        # Update the new layer.
        newLayer.flush()
        newLayer.merge_shadow(True)
        newLayer.update(0, 0, newLayer.width, newLayer.height)
        
        # Remove the old layer.
        img.remove_layer(layer)
        
        # Change the name of the new layer (two layers can not have the same name).
        newLayer.name = layerName
    except Exception as err:
        gimp.message("Unexpected error: " + str(err))
    
    # Close the undo group.
    pdb.gimp_image_undo_group_end(img)
    
    # End progress.
    pdb.gimp_progress_end()
    

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
