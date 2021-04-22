# WildCo-FaceBlur
Obscures human identities in camera trap images after processing via Microsoft MegaDetector

## This project requires two files:
### WildCoFaceBlur.R
This script acts as a user interface and takes care of data loading, including for running multiple sites with a single call. As most camera trap users are familiar with R (and less so with Python), this script allows us to maximize the efficiency of image processing in Python, with the familiar interface of R. This script is also accesible for those with little coding experience, as there are only four inputs. 

### FaceBlur.py
This is the where the blurring process actually happens. This script takes the output from MegaDetector (a .json file), a folder of images, a confidence threshold, and a "blurriness" level, and reads the MegaDetector bounding boxes designated as humans that are above your confidence threshold, then applies a gaussian blur within that box. This script is not currently designed to be called directly within Python, and is instead called via the above R script (although it can be easily edited to do so if you're a Python user). 

## Additional Requirements
If you do not have a previous installation of Anaconda, you will need to install miniconda (a free, lightweight copy of Python, which also includes essential data science packages). This takes a few minutes to install once downloaded. 

Miniconda can be downloaded here: https://docs.conda.io/en/latest/miniconda.html

## Usage
1. Download both of the above files (easiest to just download this whole repo)

2. Download Miniconda if you have't done so already

3. Put both of these files, as well as the .RProj file into a single folder 

4. In the same folder, create an "input" folder with your desired name
* Within your "input" folder, create individual sub-folders for each of your camera trap sites/deployments. 
* Within these site specific folders, paste the MegaDetector .json file and camera trap photos corresponding to the site. No sub-folders within the site folders. 
  
5. Open up the R project (or create a new one), setting the working directory to the folder from step 3. (with everything inside)

6. Open up WildCoFaceBlur.R 
6a. Set your arguments:
* img_dir_in = your "input" folder from step 4
* img_dir_out = where you want the blurred images to go
* blur_level = The "blurriness" applied to each human. Lower values are more obscured. I reccomend values between 3 and 7. 
* conf = The MegaDetector confidence threshold you wish to apply blurring above. This is situationally dependent on MegaDetector performance for your study area, so may     require fine tuning. 
    
 7. Run the script! The first few installation steps may take a few minutes the first time as new Python packages are installed, but otherwise you should be smooth sailing. 

