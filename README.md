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

#### hmerge_images(self, image_list):
This function concatenates images horizontally. **All images being merge must be the same height.** In order to add images together cleanly, the images must be cut so that one image ends exactly where the next image is going to start. 
-*image_list:* a list of cv2 images. Second image in the list is appended to the right of the first image, and further images are appended to the right. 

#### vmerge_images(self, image_list):
This function concatenates images vertically. **All images being merge must be the same width.** In order to add images together cleanly, the images must be cut so that one image ends exactly where the next image is going to start. 
-*image_list:* a list of cv2 images. Second image in the list is appended to the bottom of the first image, and further images are appended to the bottom. 

####orthorectify_video(self, cam, start_time_s, length_s, input_fn, output_dn, gcps, final_shape = (2438, 4000)):
This function orthorectifies a video stream. This will only work if the camera is not moving. This will output a new video file with the orthorectified video. 
- *cam:* what camera does the video stream come from
- *start_time_s:* what time into the video would you like to begin orthorectifying
- 
