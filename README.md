# flume-analysis-tools
This repository contains the tools I have developed for processing the data collected during my flume experiments. This readme contains an overview of the tools included as well as instructions for use. 

# Files
-----------------------------------------------------------------------------------------
## file_managers.py 
This file has a range of file management tools that allow GUI selection of the files and directories of interest.

#### load_dn(self, purpose): 

This function opens a tkinter GUI for selecting a directory and returns the full path to the directory once selected.
- *purpose:*  provides expanatory text in the GUI that tells the user what directory to select.

#### load_fn(self, purpose): 

This function opens a tkinter GUI for selecting a directory and returns the full path to the file once selected.
- *purpose:*  provides expanatory text in the GUI that tells the user what file to select.

#### import_gcps(self):
This function imports ground control point image coordinates and real world coordinates from a .csv file into the correct format for later use in these methods.

#### load_video_metadata(self, vid_file):
This function loads metadata for a video file into memory. 
- *vid_file:* A video file that you would like to view the metadata for.

--------------------------------------------------------------------------------------------
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
- *image_list:* a list of cv2 images. Second image in the list is appended to the right of the first image, and further images are appended to the right. 

#### vmerge_images(self, image_list):
This function concatenates images vertically. **All images being merge must be the same width.** In order to add images together cleanly, the images must be cut so that one image ends exactly where the next image is going to start. 
- *image_list:* a list of cv2 images. Second image in the list is appended to the bottom of the first image, and further images are appended to the bottom. 

#### orthorectify_video(self, cam, start_time_s, length_s, input_fn, output_dn, gcps, final_shape = (2438, 4000)):
This function orthorectifies a video stream. This will only work if the camera is not moving. This will output a new video file with the orthorectified video. 
- *cam:* what camera does the video stream come from
- *start_time_s:*  time into the video begins being orthorectified (in seconds)
- *length_s:* duration of the orthorectified clip (in seconds)
- *input_fn:* name of the video file to be orthorectified
- *output_dn:* directory in which the orthorectified video will be stored
- *gcps:* ground control points file for the camera
- *final_shape:* (default = (2438, 4000)) Shape of the final output video. This allows cropping of the video.

#### orthomosaic_video(videos, gcps_list, offsets_list, output_dn, outname, start_time_s, length_s, compress_by, out_speed, final_shape = (2438,4000)):
This function orthorectifies multiple videos and horizontally concatenates them to make a single orthomosaiced photo.
- *gcps_list:* A list containing the ground control points for each camera in order (length = number of cameras).
- *offsets_list:* A list containing the time offsets for each video (length = number of cameras).
- *output_dn:* The directory where you would like to store the output video.
- *outname:* The name of the final output file.
- *start_time_s:* Time where you would like to start processing for the first video feed (in seconds) **NOTE: always start after 5 seconds because there is an internal cv2 bug that sometimes trips in the first few seconds. 
- *length_s:* Length of time that you want to process (in seconds).
- *compress_by:* An integer by which the output video is compressed by **NOTE: the final image for the Riverine Basin would be 9750 x 4000 pixels, which is too large for the program to handle, so this value must be 2 or greater.
- *out_speed:* An number by which the output video is sped up by. Using 1 for this value would be real time, 2 would be sped up by 2, so that 2x the frames occur in each second. 
- *final_shape:* (default = 2438, 4000) Shape of the final output video. This allows cropping of the video. Default is what I am using for the Riverine Basin.

--------------------------------------------------------------------------------------------
## video_orthorectification.py
This file accesses the neccesary modules and functions to orthorectify a single video. To run, simply edit the neccesary parameters (lines 19-21) to reflect the situation and run the script. Several file managers will pop up to allow you to select the input video file, ground control points file, and directory where you would like to store the final video. 

--------------------------------------------------------------------------------------------
## merge_videos.py
This file accesses the neccesary modules and functions to orthorectify and merge multiple videos. To run, simply edit the neccesary parameters (lines 34-43 and 47) to reflect the situation and run the script. Several file managers will pop up to allow you to select the input video files, ground control points files, and directory where you would like to store the final video. 

**Note: the codec (fourcc) is likely to fail and give you a warning. This is not an issue because the program will switch and use the correct encoder. 

--------------------------------------------------------------------------------------------
