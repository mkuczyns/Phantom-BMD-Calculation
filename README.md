# Phantom-BMD-Calculation
Python script using ITK to automatically calculate BMD in Phantom scans.

## Script Steps:
1. Cut out an ROI representing the six phantom rods
    - One ROI for the right most phantoms
    - One ROI for the left most phantoms 
2. Process the new ROI such that the edges of the six circles can be seen
    - Median filter
    - Enhance contrast
    - Optionally erode/dilate
    - Hough Circle Transform
3. Create six new ROIs, one for each phantom rod
    - Based on data from the above processing (Hough Transform)
4. Calculate BMD for each rod
5. Export results
