# Phantom-BMD-Calculation
C++ program using ITK to automatically calculate BMD in Phantom scans.

## Script Steps:
1. Cut out an ROI representing the six phantom rods
    - One ROI for the right most phantoms
    - One ROI for the left most phantoms 
2. Process the new ROI such that the edges of the six circles can be seen
    - Median filter
    - Adaptive histogram equalization/Edge detection
    - Threshold using Otsu's method
    - Hough Circle Transform
3. Create six new ROIs, one for each phantom rod
    - Based on data from the above processing (Hough Transform)
4. Calculate BMD for each rod
5. Export results

## How-to Run:
1. Configure and generate binary files using CMake
2. Build using your favorite compiler (I use Visual Studio)
3. Run the executable located in the bin\Debug folder from the command line
    ```
    automatic_BMD_calculation.exe <PATH_TO_DICOM_FOLDER>
    ```