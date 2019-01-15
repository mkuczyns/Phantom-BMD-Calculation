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
#   -Optional dilate/erode
#   -Hough Circle Transform
#   -Crop individual phantoms
#   -Calculate BMD and save data
#----------------------------------------------------- 

<<<<<<< HEAD
from sys import argv
from os import listdir, path
=======
import sys
import os
>>>>>>> b40b5d9ee73d728f13f5aeb2ca43fb0e00bc2414
import itk

# Check input arguements
if len(argv) < 2:
    print("ERROR: Incorrect script usage:")
    print("Usage Option #1: python " + argv[0] + " <Dicom_Directory>")
    print("Usage Option #2: python " + argv[0] + " <Dicom_Directory> <Output_NIfTI_FILENAME>")
    exit(1)

# Use the specified directory
dirName = argv[1]

# Get the number of DICOMs in the specified diretory
count = len([name for name in listdir(dirName) if path.isfile(path.join(dirName, name))])

count = len([name for name in os.listdir(dirName) if os.path.isfile(os.path.join(dirName, name))])

count = len([name for name in os.listdir(dirName) if os.path.isfile(os.path.join(dirName, name))])

# Create input and output image variables
# Using NIfTI temporarily...
output_filename = "temp.nii"
if len(argv) > 2:
    output_filename = argv[2]

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
    exit(1)

# Print out all DICOM series in the provided directory
print("The directory: " + dirName + " contains the following DICOM Series: ")

for uid in seriesUID:
    print(uid)

# Loop through each DICOM series in the directory
seriesFound = False

for uid in seriesUID:
    seriesIdentifier = uid

    print('\nReading: ' + seriesIdentifier)

    fileNames = namesGenerator.GetFileNames(seriesIdentifier)

    # Read in the images
    reader = itk.ImageSeriesReader[ImageType].New()
    dicomIO = itk.GDCMImageIO.New()
    reader.SetImageIO(dicomIO)
    reader.SetFileNames(fileNames)
    reader.Update()

    # 01 - Crop Phantom ROIs
<<<<<<< HEAD
    #---------------------------------------------------------------------------------------
    # ROI #1 = (265, 410) -> (400, 460)
    # ROI #2 = (...) -> (...)

=======
>>>>>>> b40b5d9ee73d728f13f5aeb2ca43fb0e00bc2414
    size_x = 135
    size_y = 50
    size_z = count - 1
    index_x = 265
    index_y = 410
    index_z = 0

    print("Cropping ROI #1...")

<<<<<<< HEAD
    cropper = itk.ExtractImageFilter.New(reader.GetOutput())
=======
    cropper = itk.ExtractImageFilter.New(Input = reader.GetOutput())
>>>>>>> b40b5d9ee73d728f13f5aeb2ca43fb0e00bc2414
    extraction_region = cropper.GetExtractionRegion()
    size = extraction_region.GetSize()
    size[0] = int(size_x)
    size[1] = int(size_y)
    size[2] = int(size_z)
    index = extraction_region.GetIndex()
    index[0] = int(index_x)
    index[1] = int(index_y)
    index[2] = int(index_z)
    extraction_region.SetSize(size)
    extraction_region.SetIndex(index)
    cropper.SetExtractionRegion(extraction_region)
    cropper.Update()

    # 02 - Filter
<<<<<<< HEAD
    #---------------------------------------------------------------------------------------
    # Median filter, radius = 3

=======
>>>>>>> b40b5d9ee73d728f13f5aeb2ca43fb0e00bc2414
    MF_radius = 3
    print("Applying median filter with radius = " + str(MF_radius))
    median = itk.MedianImageFilter.New(Input = cropper.GetOutput(), Radius = MF_radius)
    median.Update()

    # 03 - Adaptive Histogram Equalization
<<<<<<< HEAD
    #---------------------------------------------------------------------------------------
    # Alpha = 1 -> unsharp mask
    # Beta  = 0
    # Window/Radius = 5

    AHE_alpha = float(1)
    AHE_beta = float(0)
    AHE_radius = int(5)

    print("Appying adaptive histogram equalization with alpha = " + str(AHE_alpha) + 
            ", beta = " + str(AHE_beta) + ", and radius = " + str(AHE_radius))

    histogramEqualization = itk.AdaptiveHistogramEqualizationImageFilter.New(median.GetOutput())
    histogramEqualization.SetAlpha(AHE_alpha)
    histogramEqualization.SetBeta(AHE_beta)

    radius = itk.Size[Dimension]()
    radius.Fill(AHE_radius)
    histogramEqualization.SetRadius(radius)
    histogramEqualization.Update()

    # 04 - Threshold
    #---------------------------------------------------------------------------------------
    # Otsu Segmentation

    num_bins = 128
    num_thresh = 1
    label_offset = 0

    print("Applying Otsu's method for image segmentation with " + str(num_bins) + " bins, "
            + str(num_thresh) + " threshold(s), and a label offset of " + str(label_offset))

    thresholdFilter = itk.OtsuMultipleThresholdsImageFilter[ImageType, ImageType].New()
    thresholdFilter.SetInput(histogramEqualization.GetOutput())

    # Default values
    thresholdFilter.SetNumberOfHistogramBins(num_bins)
    thresholdFilter.SetNumberOfThresholds(num_thresh)
    thresholdFilter.SetLabelOffset(label_offset)
    thresholdFilter.Update()

    rescaler = itk.RescaleIntensityImageFilter[ImageType, ImageType].New()
    rescaler.SetInput(thresholdFilter.GetOutput())
    rescaler.SetOutputMinimum(0)
    rescaler.SetOutputMaximum(125)
    rescaler.Update()

    # 05 - Optional Erode/Dilate
    #---------------------------------------------------------------------------------------
    # TO-DO: test and implement or remove completely


    # 06 - Hough Circle Transform
    #---------------------------------------------------------------------------------------
    
    print("Starting Hough Circle Transform...")

    AccumulatorImageType = itk.Image[itk.F, Dimension]

    circle = itk.HoughTransform2DCirclesImageFilter[].New()
    circle.SetInput(rescaler.GetOutput())
    circle.SetMinimumRadius(30.0)
    circle.SetMaximumRadius(40.0)
    circle.Update()

    # 07 - Create individual ROIs
    #---------------------------------------------------------------------------------------
    # Use data from the Hough Circle Transform


    # 08 - Calculate BMD
    #---------------------------------------------------------------------------------------

=======
    AHE_alpha = float(1)
    AHE_beta = float(0)
    AHE_radius = int(5)

    print("Appying adaptive histogram equalization with alpha = " + str(AHE_alpha) + 
            ", beta = " + str(AHE_beta) + ", and radius = " + str(AHE_radius))

    histogramEqualization = itk.AdaptiveHistogramEqualizationImageFilter.New(median.GetOutput())
    histogramEqualization.SetAlpha(AHE_alpha)
    histogramEqualization.SetBeta(AHE_beta)
    histogramEqualization.Update()

    radius = itk.Size[Dimension]()
    radius.Fill(AHE_radius)
    histogramEqualization.SetRadius(radius)

    # 04 - Threshold

    # 05 - Optional Erode/Dilate

    # 06 - Hough Circle Transform

    # 07 - Create individual ROIs

    # 08 - Calculate BMD

>>>>>>> b40b5d9ee73d728f13f5aeb2ca43fb0e00bc2414
    print("\nWriting out " + output_filename + "...")

    # Write out the modified images as NIfTI
    writer = itk.ImageFileWriter[ImageType].New()
    writer.SetFileName(output_filename)
    writer.UseCompressionOn()
<<<<<<< HEAD
    writer.SetInput(circle.GetOutput())
=======
    writer.SetInput(histogramEqualization.GetOutput())
>>>>>>> b40b5d9ee73d728f13f5aeb2ca43fb0e00bc2414
    writer.Update()

    # To avoid an infinite loop...
    seriesFound = True

    if seriesFound:
        break

print("\nDone!")
