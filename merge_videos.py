#merge_videos.py

"""place to figure out merging videos together"""

#import neccesary packages and modules
import cv2
from file_managers import FileManagers
from orthomosaic_tools import OrthomosaicTools

def orthorectify_video(vid, vid1, vid2, vid3, output_dn, gcps, gcps1, gcps2, gcps3, start_time_s, length_s, final_shape = (2438,4000)):
    """ method for orthorecifying videos"""

    #instantiate the orthomosaic tools module
    ot = OrthomosaicTools()

    #Find homography matrix
    matrix = ot.find_homography(1, gcps)
    matrix1 = ot.find_homography(2, gcps1)
    matrix2 = ot.find_homography(3, gcps2)
    matrix3 = ot.find_homography(4, gcps3)

    #choose a place to store output video
    output_fn = output_dn + "\\merged.mp4"

    #heres where we get into the video
    cap = cv2.VideoCapture(vid)
    cap1 = cv2.VideoCapture(vid1)
    cap2 = cv2.VideoCapture(vid2)
    cap3 = cv2.VideoCapture(vid3)

    fps = cap.get(cv2.CAP_PROP_FPS)

    fourcc = cv2.VideoWriter_fourcc(*"HEIC")
    # Create VideoWriter object to save the output video
    out = cv2.VideoWriter(output_fn, fourcc, fps, (4876, 2000))
    print('done!')

    start_time = start_time_s *1000
    count = 0

    ret, frame = cap.read()
    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()
    ret3, frame3 = cap3.read()

    cap.set(cv2.CAP_PROP_POS_MSEC,(start_time))
    cap1.set(cv2.CAP_PROP_POS_MSEC,(start_time))
    cap2.set(cv2.CAP_PROP_POS_MSEC,(start_time))
    #cap3.set(cv2.CAP_PROP_POS_MSEC,(start_time))

    while ret and ret1 and ret2 and ret3 and count <= length_s:

        # correct frames with warpPerspective
        corrected_frame = cv2.warpPerspective(frame, matrix, final_shape)
        corrected_frame = cv2.resize(corrected_frame, (1219,2000))
        corrected_frame1 = cv2.warpPerspective(frame1, matrix1, final_shape)
        corrected_frame1 = cv2.resize(corrected_frame1, (1219,2000))
        corrected_frame2 = cv2.warpPerspective(frame2, matrix2, final_shape)
        corrected_frame2 = cv2.resize(corrected_frame2, (1219,2000))
        corrected_frame3 = cv2.warpPerspective(frame3, matrix3, final_shape)
        corrected_frame3 = cv2.resize(corrected_frame3, (1219,2000))

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


#instantiate file managers
fm = FileManagers()

#select videos
video = fm.load_fn("Video")
video1 = fm.load_fn("Video1")
video2 = fm.load_fn("Video2")
video3 = fm.load_fn("Video3")


videos = [video, video1, video2]
print(videos)

#select control point files
gcps = fm.import_gcps()
gcps1= fm.import_gcps()
gcps2 = fm.import_gcps()
gcps3 = fm.import_gcps()


gcps_list = [gcps, gcps1, gcps2]
print(gcps_list)

output_path = fm.load_dn("Choose a directory to store video in")

orthorectify_video(video, video1, video2, video3, output_path, gcps, gcps1, gcps2, gcps3, start_time_s=50, length_s=3)
