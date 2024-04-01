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

    def find_homography(self, cam, gcps):
        """Method for finding homography matrix."""

        #add 2000 to the x coordinates of the real world list
        for count, i in enumerate(gcps[0]):
            i[0] = float(i[0]) - 2438 * (cam-1)
            i[1] = float(i[1]) + 2000

        #convert the image and destination coordinates to numpy array with float32
        src_pts = np.array(gcps[1])
        src_pts = np.float32(src_pts[:, np.newaxis, :])

        dst_pts = np.array(gcps[0])
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
        if save_image is True:
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
                           output_dn, gcps, final_shape = (2438,4000)):
        """ method for orthorecifying videos"""

        #Find homography matrix
        matrix = self.find_homography(cam, gcps)

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

    def orthomosaic_video(self, videos, gcps_list, offsets_list, output_dn, outname, start_time_s, length_s, compress_by, out_speed, final_shape = (2438,4000)):
        """ method for orthorecifying videos"""

        compressed_shape = tuple([int(s / compress_by) for s in final_shape])
        output_shape = (int(4 * compressed_shape[0]), compressed_shape[1])

        #instantiate the orthomosaic tools module
        ot = OrthomosaicTools()

        #choose a place to store output video
        output_fn = output_dn + "\\" + outname + ".mp4"

        #Find homography matrix
        matrix = ot.find_homography(1, gcps_list[0])
        matrix1 = ot.find_homography(2, gcps_list[1])
        matrix2 = ot.find_homography(3, gcps_list[2])
        matrix3 = ot.find_homography(4, gcps_list[3])

        #heres where we get into the video
        cap = cv2.VideoCapture(videos[0])
        cap1 = cv2.VideoCapture(videos[1])
        cap2 = cv2.VideoCapture(videos[2])
        cap3 = cv2.VideoCapture(videos[3])

        fps = cap.get(cv2.CAP_PROP_FPS)

        fourcc = cv2.VideoWriter_fourcc(*"HEIC")
        # Create VideoWriter object to save the output video
        out = cv2.VideoWriter(output_fn, fourcc, fps*out_speed, output_shape)
        print('done!')

        start_time = start_time_s *1000
        count = 0

        ret, frame = cap.read()
        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()
        ret3, frame3 = cap3.read()

        cap.set(cv2.CAP_PROP_POS_MSEC,(start_time + offsets_list[0]))
        cap1.set(cv2.CAP_PROP_POS_MSEC,(start_time + offsets_list[1]))
        cap2.set(cv2.CAP_PROP_POS_MSEC,(start_time + offsets_list[2]))
        cap3.set(cv2.CAP_PROP_POS_MSEC,(start_time + offsets_list[3]))

        while ret and ret1 and ret2 and ret3 and count <= length_s:
            # correct frames with warpPerspective
            corrected_frame = cv2.warpPerspective(frame, matrix, final_shape)
            corrected_frame = cv2.resize(corrected_frame, compressed_shape)
            corrected_frame1 = cv2.warpPerspective(frame1, matrix1, final_shape)
            corrected_frame1 = cv2.resize(corrected_frame1, compressed_shape)
            corrected_frame2 = cv2.warpPerspective(frame2, matrix2, final_shape)
            corrected_frame2 = cv2.resize(corrected_frame2, compressed_shape)
            corrected_frame3 = cv2.warpPerspective(frame3, matrix3, final_shape)
            corrected_frame3 = cv2.resize(corrected_frame3, compressed_shape)

            merged = cv2.hconcat([corrected_frame, corrected_frame1, corrected_frame2, corrected_frame3])
            out.write(merged)

            ret, frame = cap.read()
            ret1, frame1 = cap1.read()
            ret2, frame2 = cap2.read()
            ret3, frame3 = cap3.read()

            count = count + 1/fps
            print(cap.get(cv2.CAP_PROP_POS_MSEC))

        # Release video capture and writer objects
        cap.release()
        out.release()

        # Close all OpenCV windows
        cv2.destroyAllWindows()
