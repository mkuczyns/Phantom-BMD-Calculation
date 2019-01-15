/*----------------------------------------------------- 
* automatic_BMD_calculation.cxx
*
* Created by:   Michael Kuczynski
* Created on:   2018.12.20
*
* Description: -Used for automatic phantom BMD calculations in Ankle PRE_OA data.
*              -Only works for decompressed DICOM data.
*              -Performs the following steps:
*                   1. Crop out the rod ROIs
*                   2. Filter to remove noise
*                   3. Enhance contrast (histogram equalization)
*                   4. Convert to 8-bit grayscale image
*                   5. Threshold
*                   6. Erode or dilate as needed (optional)
*                   7. Hough Transform (circle)
*                   8. Use Hough Transform results to crop individual circles from original image
*                   9. Calculate BMD for each circle ROI
*----------------------------------------------------- 
*
* Requirements:
*   -itk
*
* Usage:
*   -Use CMake to configure and generate binary files
*   -Build the project using whatever compiler you have installed
*   -Run the executable located in <PATH_TO_YOUR_PROJECT>\bin\Debug\automatic_BMD_calculation.exe
*
* TO-DO:
*   -Add error checking (try/catch)
*
*----------------------------------------------------- */

#include "itkImage.h"

#include "itkImageSeriesReader.h"
#include "itkImageFileWriter.h"
#include "itkGDCMImageIO.h"
#include "itkGDCMSeriesFileNames.h"

#include "itkMedianImageFilter.h"
#include "itkSobelEdgeDetectionImageFilter.h"
#include <itkExtractImageFilter.h>

int main(int argc, char * argv[])
{
    // Check input arguements
    if (argc < 2 || argc > 3)
    {
        std::cerr << "ERROR: Incorrect usage: \n";
        std::cerr << "Usage option #1: " << argv[0] << ".exe <Dicom_Directory>\n";
        std::cerr << "Usage option #2: " << argv[0] << ".exe <Dicom_Directory> <Output_Filename>\n";
        std::cerr << "\nNote: <Output_Filename> must be a 3D file type.\n";
        std::cerr << "Note: If an <Output_Filename> is not specified, a default <Output_Filename> is used (temp.nii)\n";
    }

    // Default output file name is "temp.nii"
    std::string dirName = argv[1];
    std::string outputFilename = "temp.nii";
    if (argc == 3)
    {
        outputFilename = argv[2];
    }

    // Set image type
    using PixelType = signed short;
    constexpr unsigned int Dimension = 3;
    using ImageType = itk::Image< PixelType, Dimension >;

    // Generate list of DICOM names and series ID
    using NamesGeneratorType = itk::GDCMSeriesFileNames;
    NamesGeneratorType::Pointer nameGenerator = NamesGeneratorType::New();

    // TO-DO: Limit series restriction depending on DICOM series
    nameGenerator->SetUseSeriesDetails(true);
    nameGenerator->AddSeriesRestriction("00000002|00000325");
    nameGenerator->SetGlobalWarningDisplay(false);
    nameGenerator->SetDirectory(dirName);

    try
    {
        using SeriesIdContainer = std::vector< std::string >;
        const SeriesIdContainer & seriesUID = nameGenerator->GetSeriesUIDs();
        auto seriesItr = seriesUID.begin();
        auto seriesEnd = seriesUID.end();

        if (seriesItr != seriesEnd)
        {
            // Print out all DICOM series in the provided directory
            std::cout << "The directory: ";
            std::cout << dirName << std::endl;
            std::cout << "Contains the following DICOM Series: ";
            std::cout << std::endl;
        }
        else
        {
            std::cout << "No DICOMs in: " << dirName << std::endl;
            return EXIT_SUCCESS;
        }

        while (seriesItr != seriesEnd)
        {
            std::cout << seriesItr->c_str() << std::endl;
            ++seriesItr;
        }

        seriesItr = seriesUID.begin();

        // Loop through each DICOM series in the directory
        // TO-DO: only perform processing on the first encountered DICOM series
        // TO-DO: add option for specifying the DICOM series
        while (seriesItr != seriesUID.end())
        {
            std::string seriesIdentifier;
            
            seriesIdentifier = seriesItr->c_str();
            seriesItr++;

            // Read in the images
            std::cout << "\nReading: ";
            std::cout << seriesIdentifier << std::endl;
            using FileNamesContainer = std::vector< std::string >;
            FileNamesContainer fileNames =
            nameGenerator->GetFileNames(seriesIdentifier);

            using ReaderType = itk::ImageSeriesReader< ImageType >;
            ReaderType::Pointer reader = ReaderType::New();
            using ImageIOType = itk::GDCMImageIO;
            ImageIOType::Pointer dicomIO = ImageIOType::New();
            reader->SetImageIO(dicomIO);
            reader->SetFileNames(fileNames);

            try
            {
                reader->Update();
            }
            catch (itk::ExceptionObject &ex)
            {
                std::cout << ex << std::endl;
                return EXIT_FAILURE;
            }

            ImageType::Pointer readerOutput = reader->GetOutput();

            /* 01 - Crop Phantom ROIs
            *---------------------------------------------------------------------------------------
            * ROI #1 = (265, 410) -> (400, 460)
            * ROI #2 = (...) -> (...)
            */
            std::cout << "Cropping first ROI..." << std::endl;

            // Define the starting coordinates and size of the ROI
            int size[3] = {135, 50, 9};      // TO-DO: Get a better way to find # of files in directory...

            int start[3] = {265, 410, 0};

            // Set the desired region to crop
            ImageType::IndexType desiredStart;
            desiredStart.SetElement(0, 265);
            desiredStart.SetElement(1, 410);
            desiredStart.SetElement(2, 0);

            ImageType::SizeType desiredSize;
            desiredSize.SetElement(0, 135);
            desiredSize.SetElement(1, 50);
            desiredSize.SetElement(2, 9);

            ImageType::RegionType desiredRegion(desiredStart, desiredSize);

            // Define the extraction filter
            typedef itk::ExtractImageFilter< ImageType, ImageType > ExtractFilterType;
            ExtractFilterType::Pointer extractFilter = ExtractFilterType::New();
            extractFilter->SetExtractionRegion(desiredRegion);
            extractFilter->SetInput( readerOutput );
            
            #if ITK_VERSION_MAJOR >= 4
                extractFilter->SetDirectionCollapseToIdentity(); // This is required.
            #endif

            try
            {
                extractFilter->Update();
            }
            catch (itk::ExceptionObject &ex)
            {
                std::cout << ex << std::endl;
                return EXIT_FAILURE;
            }

            ImageType::Pointer extractFilterOutput = extractFilter->GetOutput();
            extractFilterOutput->DisconnectPipeline();
            extractFilterOutput->FillBuffer(2);

            // Write out file
            using WriterType = itk::ImageFileWriter< ImageType >;
            WriterType::Pointer writer = WriterType::New();
            
            writer->SetFileName(outputFilename);
            writer->UseCompressionOn();
            writer->SetInput( extractFilter->GetOutput() );
            std::cout << "Writing: " << outputFilename << std::endl;
            try
            {
                writer->Update();
            }
            catch (itk::ExceptionObject &ex)
            {
                std::cout << ex << std::endl;
                continue;
            }
        }
    }
    catch (itk::ExceptionObject &ex)
    {
        std::cout << ex << std::endl;
        return EXIT_FAILURE;
    }
    return EXIT_SUCCESS;
}