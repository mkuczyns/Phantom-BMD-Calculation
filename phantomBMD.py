# coding=utf-8
#----------------------------------------------------- 
# phantomBMD.py
#
# Created by:   Michael Kuczynski
# Created on:   2018.10.24
#
# Description: Automatically calculate BMD for six phantom rods in 
#              DICOM images in ImageJ.
#----------------------------------------------------- 
#
# Requirements:
#   -Python 2.7, 3.4 or later
#   -Fiji (since there is no scripting functionality in ImageJ alone)
#
# Usage:
#   TBD
#----------------------------------------------------- 
import os
from ij import IJ, ImagePlus

path = "D:\DICOMs\IMAGES\DECOMPRESSED\BONE PLUS\00000002.dcm"
imp = IJ.openImage(path)
imp.show()