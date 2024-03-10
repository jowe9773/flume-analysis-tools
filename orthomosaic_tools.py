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

    def find_homoragphy(self, cam):
        """Method for finding homography matrix."""

        file_managers = FileManagers() #create an instance of the file manager class
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

        #now we can find homography matrix
        h_matrix = cv2.findHomography(src_pts, dst_pts)

        return h_matrix[0]

    def orthorectify_image(self, matrix, save_image = False):
        """Method for orthorectifying individual images."""

        #load image file
        file_manager = FileManagers()
        image_fn = file_manager.load_fn("Select and image to orthorectify")
        out_image_fn = os.path.splitext(image_fn)[0] + "_warped.jpg"
        image = cv2.imread(image_fn)

        warped_image = cv2.warpPerspective(image, matrix, (2438, 4000))

        # Save the warped image (if input = True)
        if save_image == True:
            cv2.imwrite(out_image_fn, warped_image)

        else:
            return warped_image

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

    def orthorectify_video(self, camera, start_time = 0, step = 1/24, clip_duration = 30):
        """ method for orthorecifying videos"""

        ortho_tools = OrthomosaicTools()
        matrix = ortho_tools.find_homoragphy(camera)

        #load input video
        file_managers = FileManagers()
        input_video = file_managers.load_fn("Choose a video file")

        #choose a place to store output video
        output_dn = file_managers.load_dn("Choose a directory to store corrected video in")
        fn = os.path.basename(input_video).split('.')[0]
        output_path = output_dn + '\\' + fn + "_corrected.mp4"

        #select information for video
        count = start_time
        success = True

        cap = cv2.VideoCapture(input_video)

        # Get the video's frames per second and frame size
        fps = cap.get(cv2.CAP_PROP_FPS)


        # Create VideoWriter object to save the output video
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (2438, 4000))

        while success and count <= start_time + clip_duration:
            cap.set(cv2.CAP_PROP_POS_MSEC,(count*1000))    # added this line

            if success == True:
                ret, frame = cap.read()

                # Increase brightness using cv2.addWeighted
                corrected_frame = cv2.warpPerspective(frame, matrix, (2438, 4000))

                # Write the brightened frame to the output video
                out.write(corrected_frame)

                count = count + (1/fps)

            # Break the loop if no more frames are available
            else:
                break

        # Release video capture and writer objects
        cap.release()
        out.release()

        # Close all OpenCV windows
        cv2.destroyAllWindows()
