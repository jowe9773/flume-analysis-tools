#video_orthorectification.py

"""for now this file is being used to build the neccesary 
steps to orthrectify videos. Once it is done, it will be 
broken up in the way that makes the most sense."""

#Load neccesary packages and modules
import os
import numpy as np
import cv2
from file_managers import FileManagers
from orthomosaic_tools import OrthomosaicTools

#choose which camera you will be working with
camera = 1

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
start_time = 0
clip_duration = 30
step = 1/24
count = start_time
success = True

cap = cv2.VideoCapture(input_video)

# Get the video's frames per second and frame size
fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Create VideoWriter object to save the output video
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(output_path, fourcc, fps, (2438, 4000))

while success and count <= start_time + clip_duration:
    cap.set(cv2.CAP_PROP_POS_MSEC,(count*1000))    # added this line 

    if success == True:
        ret, frame = cap.read()

        # Increase brightness using cv2.addWeighted
        corrected_frame = cv2.warpPerspective(frame, matrix, (2438, 4000))

        # Write the brightened frame to the output video
        out.write(corrected_frame)

        count = count + step

    # Break the loop if no more frames are available
    else:
        break

# Release video capture and writer objects
cap.release()
out.release()

# Close all OpenCV windows
cv2.destroyAllWindows()
