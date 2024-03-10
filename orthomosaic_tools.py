#orthomosaic_tools.py

"""module containing methods used in orthorectification and mosaicing of photos and videos"""

#Load neccesary packages and modules
import csv
import os
import numpy as np
import cv2
from file_managers import FileManagers

class OrthomosaicTools():
    """Class contains methods for orthorectification and mosaicing of photos and videos"""

    def __init__(self):
        print("initialized")

    def orthorectify_image(self, cam):
        """Method for orthorectifying individual images."""

        file_manager = FileManagers() #create an instance of the file manager class

        gcps_fn = file_manager.load_fn("GCPs file") #load filename/path of the GCPs

        gcps_rw_list = [] #make list for real world coordinates of GCPs
        gcps_image_list = [] #make list for image coordinates of GCPs

        #Read csv file into a list of real world and a list of image gcp coordinates
        with open(gcps_fn, 'r', newline='', encoding="utf-8") as csvfile:
            # Create a CSV reader object
            csv_reader = csv.reader(csvfile)

            # Skip the header row
            next(csv_reader)

            # Iterate over each row in the CSV file
            for row in csv_reader:
                # Each row is a list where each element represents a column value
                gcps_image_list.append(row[1:3])
                gcps_rw_list.append(row[3:5])

        #add 2000 to the x coordinates of the real world list
        for count, i in enumerate(gcps_rw_list):
            i[0] = float(i[0]) - 2438 * (cam-1)
            i[1] = float(i[1]) + 2000

        #convert the image and destination coordinates to numpy array with float32
        src_pts = np.array(gcps_image_list)
        src_pts = np.float32(src_pts[:, np.newaxis, :])

        dst_pts = np.array(gcps_rw_list)
        dst_pts = np.float32(dst_pts[:, np.newaxis, :])

        #now we can find homography matrix
        h_matrix = cv2.findHomography(src_pts, dst_pts)

        #Step 2: load image file
        image_fn = file_manager.load_fn("Select and image to orthorectify")
        out_image_fn = os.path.splitext(image_fn)[0] + "_warped.jpg"
        image = cv2.imread(image_fn)

        warped_image = cv2.warpPerspective(image, h_matrix[0], (2438, 4000))

        # Save the warped image
        cv2.imwrite(out_image_fn, warped_image)

    def hmerge_images(self, image_list):
        """horizontally merge images of same vertical size"""

        im_h = cv2.hconcat(image_list)

        # save the output image
        file_manager = FileManagers()

        out_dn = file_manager.load_dn("select directory to store image in")
        out_path = out_dn + "//merged.jpg"
        cv2.imwrite(out_path, im_h)

    def vmerge_images(self, image_list):
        """vertically merge images of same vertical size"""

        im_v = cv2.vconcat(image_list)

        # save the output image
        file_manager = FileManagers()

        out_dn = file_manager.load_dn("select directory to store image in")
        out_path = out_dn + "//merged.jpg"
        cv2.imwrite(out_path, im_v)
