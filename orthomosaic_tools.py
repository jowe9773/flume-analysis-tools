#orthomosaic_tools.py

"""module containing methods used in orthorectification and mosaicing of photos and videos"""

#Load neccesary packages and modules
import os
import numpy as np
import cv2
from file_managers import FileManagers

class OrthomosaicTools():
    """Class contains methods for orthorectification and mosaicing of photos and videos"""

    def __init__(self):
        print("initialized")

    def find_homoragphy(self, cam, gcps_rw_list, gcps_image_list):
        """Method for finding homography matrix."""

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

    def orthorectify_video(self, cam, start_time_s, length_s, input_fn,
                           output_dn, gcps_rw_list, gcps_image_list, final_shape = (2438,4000)):
        """ method for orthorecifying videos"""

        #Find homography matrix
        matrix = self.find_homoragphy(cam, gcps_rw_list, gcps_image_list)

        #choose a place to store output video
        fn = os.path.basename(input_fn).split('.')[0]
        output_path = output_dn + '\\' + fn + "_corrected.mp4"

        #heres where we get into the video
        cap = cv2.VideoCapture(input_fn)

        fps = cap.get(cv2.CAP_PROP_FPS)

        os.environ['OPENCV_FFMPEG_READ_ATTEMPTS'] = '10000'  # update ffmpeg read attempts
        fourcc = cv2.VideoWriter_fourcc(*"HEIC")
        # Create VideoWriter object to save the output video
        out = cv2.VideoWriter(output_path, fourcc, fps, final_shape)
        print('done!')

        start_time = start_time_s *1000
        count = 0
        success, frame = cap.read()
        cap.set(cv2.CAP_PROP_POS_MSEC,(start_time))
        while success and count <= length_s:

            # correct frame with warpPerspective
            corrected_frame = cv2.warpPerspective(frame, matrix, final_shape)

            # Write the brightened frame to the output video
            out.write(corrected_frame)

            success, frame = cap.read()
            count = count + 1/fps

        # Release video capture and writer objects
        cap.release()
        out.release()

        # Close all OpenCV windows
        cv2.destroyAllWindows()
