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
#   -Add functionality for multiple DICOM series in a single directory
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
if len(sys.argv) < 2:
    print("ERROR: Incorrect script usage:")
    print("Usage Option #1: python " + sys.argv[0] + " <Dicom_Directory>")
    print("Usage Option #2: python " + sys.argv[0] + " <Dicom_Directory> <Output_NIfTI_FILENAME>")
    sys.exit(1)

# Use the specified directory
dirName = sys.argv[1]

# Create input and output image variables
# Using NIfTI temporarily...
output_filename = "temp.nii"
if len(sys.argv) > 2:
    output_filename = sys.argv[2]

# Specify the DICOM image parameters
PixelType = itk.ctype("signed short")
Dimension = 3

ImageType = itk.Image[PixelType, Dimension]

# Generate list of DICOM names and series ID
namesGenerator = itk.GDCMSeriesFileNames.New()
namesGenerator.SetUseSeriesDetails(True)

# TO-DO: Limit series restriction depending on DICOM series
namesGenerator.AddSeriesRestriction("00000002|00000325")

namesGenerator.SetGlobalWarningDisplay(False)
namesGenerator.SetDirectory(dirName)

seriesUID = namesGenerator.GetSeriesUIDs()

# Check if directory contains DICOMs
if len(seriesUID) < 1:
    print("No DICOMs in: " + dirName)
    sys.exit(1)

# Print out all DICOM series in the provided directory
print("The directory: " + dirName + " contains the following DICOM Series: ")

for uid in seriesUID:
    print(uid)

# Loop through each DICOM series in the directory
seriesFound = False

for uid in seriesUID:
    seriesIdentifier = uid

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

    # 02 - Enhance Contrast

    # 03 - Threshold

    # 04 - Optional Erode/Dilate

    # 05 - Hough Circle Transform

    # 06 - Create individual ROIs

    # 07 - Calculate BMD

    print("Writing out " + output_filename + "...")

    # Write out the modified images as NIfTI
    writer = itk.ImageFileWriter[ImageType].New()
    writer.SetFileName(output_filename)
    writer.UseCompressionOn()
    writer.SetInput(median.GetOutput())
    writer.Update()
    
    # To avoid an infinite loop...
    seriesFound = True

    if seriesFound:
        break

print("Done!")