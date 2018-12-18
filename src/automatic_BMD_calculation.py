# coding=utf-8
#----------------------------------------------------- 
# automatic_BMD_calculation.py
#
# Created by:   Michael Kuczynski
# Created on:   2018.12.13
#
# Description: -Used for automatic phantom BMD calculations in Ankle PRE_OA data.
#              -Only works for decompressed DICOM data.
#              -Performs the following steps:
#                   1.  Crop out the rod ROIs
#                   2.  Filter to remove noise
#                   3.  Enhance contrast (histogram equalization)
#                   4.  Convert to 8-bit grayscale image
#                   5.  Threshold
#                   6.  Convert to mask
#                   7.  Erode or dilate as needed (optional)
#                   8.  Hough Transform (circle)
#                   9.  Use Hough Transform results to crop individual circles from original image
#                   10. Calculate BMD for each circle ROI
#----------------------------------------------------- 
#
# Requirements:
#   -Python 2.7, 3.4 or later
#   -itk
#
# Usage:
#   automatic_BMD_calculation.py <DICOM_FOLDER_NAME>
#
# TO-DO:
#   -Add error checking (try/catch)
#   -Crop phantom ROIs
#   -Enhance contrast
#   -Convert to mask
#   -Optional dilate/erode
#   -Hough Circle Transform
#   -Crop individual phantoms
#   -Calculate BMD and save data
#----------------------------------------------------- 

import sys
import itk

# Check input arguements
'''
if len(sys.argv) < 2:
    print("ERROR: Incorrect script usage:")
    print("Usage: " + sys.argv[0] + " <Dicom_Directory>")
'''

# Create input and output image variables
# Using NIfTI temporarily...
#input_filename = sys.argv[1]
output_filename = "median.nii"

# Specify the DICOM image parameters
PixelType = itk.ctype("signed short")
Dimension = 3

ImageType = itk.Image[PixelType, Dimension]

# Image directory
dirName = 'D:\DICOMs\IMAGES\DECOMPRESSED\BONE PLUS'

# Generate list of DICOM names and series ID
namesGenerator = itk.GDCMSeriesFileNames.New()
namesGenerator.SetUseSeriesDetails(True)
namesGenerator.AddSeriesRestriction("00000002|00000325")
namesGenerator.SetGlobalWarningDisplay(False)
namesGenerator.SetDirectory(dirName)

seriesUID = namesGenerator.GetSeriesUIDs()

if len(seriesUID) < 1:
    print('No DICOMs in: ' + dirName)
    sys.exit(1)

print('The directory: ' + dirName)
print('Contains the following DICOM Series: ')
for uid in seriesUID:
    print(uid)

# Loop through each DICOM series in the directory
seriesFound = False

for uid in seriesUID:
    seriesIdentifier = uid

    if len(sys.argv) > 3:
        seriesIdentifier = sys.argv[3]
        seriesFound = True

    print('Reading: ' + seriesIdentifier)

    fileNames = namesGenerator.GetFileNames(seriesIdentifier)

    # Read in the images
    reader = itk.ImageSeriesReader[ImageType].New()
    dicomIO = itk.GDCMImageIO.New()
    reader.SetImageIO(dicomIO)
    reader.SetFileNames(fileNames)
    #reader.ForceOrthogonalDirectionOff()

    # 01 - Filter
    median = itk.MedianImageFilter.New(reader.GetOutput(), Radius = 2)

    print("Writing out " + output_filename + "...")

    # Write out the modified images as NIfTI
    writer = itk.ImageFileWriter[ImageType].New()
    writer.SetFileName(output_filename)
    writer.UseCompressionOn()
    writer.SetInput(median.GetOutput())
    writer.Update()
    
    if seriesFound:
        break

print("Done!")