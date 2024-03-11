#video_orthorectification.py

"""for now this file is being used to build the neccesary 
steps to orthrectify videos. Once it is done, it will be 
broken up in the way that makes the most sense."""

#Load neccesary packages and modules
import os
import cv2
from file_managers import FileManagers
from orthomosaic_tools import OrthomosaicTools

#choose which camera you will be working with
CAM = 1

ortho_tools = OrthomosaicTools()
matrix = ortho_tools.find_homoragphy(CAM)

#load input video
file_managers = FileManagers()
input_video = file_managers.load_fn("Choose a video file")

#choose a place to store output video
output_dn = file_managers.load_dn("Choose a directory to store corrected video in")
fn = os.path.basename(input_video).split('.')[0]
output_path = output_dn + '\\' + fn + "_corrected.mp4"



#heres where we get into the video
cap = cv2.VideoCapture(input_video)

fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

os.environ['OPENCV_FFMPEG_READ_ATTEMPTS'] = '10000'  # update ffmpeg read attempts
fourcc = cv2.VideoWriter_fourcc(*"hevc")
# Create VideoWriter object to save the output video
out = cv2.VideoWriter(output_path, fourcc, fps, (2438, 4000))
print('done!')

START_TIME = 53000 #in milliseconds
LENGTH = 30 #in seconds
COUNT = 0
success, frame = cap.read()
cap.set(cv2.CAP_PROP_POS_MSEC,(START_TIME))
while success and COUNT <= LENGTH:

    # correct frame with warpPerspective
    corrected_frame = cv2.warpPerspective(frame, matrix, (2438, 4000))

    # Write the brightened frame to the output video
    out.write(corrected_frame)

    success, frame = cap.read()
    COUNT = COUNT + 1/fps

# Release video capture and writer objects
cap.release()
out.release()

# Close all OpenCV windows
cv2.destroyAllWindows()
