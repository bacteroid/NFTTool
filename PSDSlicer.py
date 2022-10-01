# -*- coding: utf-8 -*-
"""
Created on Sat Oct  1 21:41:37 2022
@author: Mercteria

Usage:
Put this script under same directory with .psd files you want to split.

Script shoud be placed in the same folder with your psd files.  
  
Sample Input:
(Layers in PSD)
|-Group1
| |-G1_Layer1
| |-G1_Layer2
| |-...
|
|-Group2
| |-G2_Layer1
| |-G2_Layer2
| |-...
|
|-Base_Layer
  
Sample Output:  
(Output Folder)
|-Group1
| |-G1_Layer1.png
| |-G1_Layer2.png
| |-...
|
|-Group2
| |-G2_Layer1.png
| |-G2_Layer2.png
| |-...
|
|-Base
| |-Base_Layer.png

"""

from psd_tools import PSDImage
import sys
import os

# Load PSD list
bas = os.path.abspath(os.path.dirname(sys.argv[0])) # Your base directory
patlst = [f for f in os.listdir(bas) if f.endswith(".psd")]

# Main splitting function
def genlay(pat,bas=bas):
    psd = PSDImage.open(pat)
    lstpt = "base"
    for layer in psd.descendants():
        svpt = os.path.join(bas,"Export",lstpt)
        if not os.path.exists(svpt):
                os.makedirs(svpt)
        print(layer)
        layer.visible = True
        if layer.is_group():
            lstpt = layer.name
        else:
            layer_image = layer.composite()
            layer_image.save(os.path.join(svpt,layer.name+'.png'))

# Run through PSD under your path
for p in patlst:
    fp = os.path.join(bas,p)
    genlay(fp)