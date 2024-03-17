# flume-analysis-tools
This repository contains the tools I have developed for processing the data collected during my flume experiments. This readme contains an overview of the tools included as well as instructions for use. 

# Files
## file_managers.py 
This file has a range of file management tools that allow GUI selection of the files and directories of interest.

#### load_dn(self, purpose): 

This function opens a tkinter GUI for selecting a directory and returns the full path to the directory once selected.
- *purpose:*  provides expanatory text in the GUI that tells the user what directory to select.

#### load_fn(self, purpose): 

This function opens a tkinter GUI for selecting a directory and returns the full path to the file once selected.
- *purpose:*  provides expanatory text in the GUI that tells the user what file to select.

## orthomosaic_tools.py 
This file has a range of tools that are used to orthorectify and mosiac images and videos.

#### find_homography(self, cam, gcps): 

This function finds a homography matrix based on ground control points. Has a "cam" option to shift the image to the proper place. Returns a homography matrix
- *cam:*  what camera are the gcps from.
- *gcps:* ground control points (a list of lists. list 1 is ground control coordinates in the image, list 2 is ground control coordinates in the real world). Use output from FileManagers.import_gcps() for a given camera. 

#### orthorectify_image(self, matrix, save_image = False):
This function applies a homography matrix to an image to warp the image perspective to rectilinear. returns an image.
- *matrix:* homography matrix. Can be found for a particular image with a set of ground control points using OrthomoseaicTools.find_homography().
- *save_image:* (default = True) If you would like to save the image as a file, this parameter should be set to true.
