#video_orthorectification.py

"""for now this file is being used to build the neccesary 
steps to orthrectify videos. Once it is done, it will be 
broken up in the way that makes the most sense."""

#Load neccesary packages and modules
import csv
import os
import numpy as np
import cv2
from file_managers import FileManagers

#######################################
# Step 1: find homography from points #
#######################################

cam = 1 #state which camera you are working with

#load gcps
file_managers = FileManagers()
gcps_rw_list, gcps_image_list = file_managers.import_gcps()

#add 2000 to the x coordinates of the real world list
for count, i in enumerate(gcps_rw_list):
    i[0] = float(i[0]) - 2438 * (cam-1)
    i[1] = float(i[1]) + 2000

#convert the image and destination coordinates to numpy array with float32
src_pts = np.array(gcps_image_list)
src_pts = np.float32(src_pts[:, np.newaxis, :])

dst_pts = np.array(gcps_rw_list)
dst_pts = np.float32(dst_pts[:, np.newaxis, :])

#####################################
# Now we can find homography matrix #
#####################################

h_matrix = cv2.findHomography(src_pts, dst_pts)

#Step 2: load image file
image_fn = file_manager.load_fn("Select and image to orthorectify")
out_image_fn = os.path.splitext(image_fn)[0] + "_warped.jpg"
image = cv2.imread(image_fn)

warped_image = cv2.warpPerspective(image, h_matrix[0], (2438, 4000))

# Save the warped image
cv2.imwrite(out_image_fn, warped_image)


####################################
# Concatenate the 4 images into 1: #
####################################

'''cam1 = file_manager.load_fn("Cam1")
cam2 = file_manager.load_fn("Cam2")
cam3 = file_manager.load_fn("Cam3")
cam4 = file_manager.load_fn("Cam4")

im1 = cv2.imread(cam1)
im2 = cv2.imread(cam2)
im3 = cv2.imread(cam3)
im4 = cv2.imread(cam4)

# vertically concatenates images
# of same width
im_h = cv2.hconcat([im1, im2, im3, im4])

# save the output image
out_dn = file_manager.load_dn("select directory to store image in")
out_path = out_dn + "//merged.jpg"
cv2.imwrite(out_path, im_h)'''
