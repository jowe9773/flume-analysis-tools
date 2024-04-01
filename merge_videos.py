#merge_videos.py

"""place to figure out merging videos together"""

#import neccesary packages and modules
from file_managers import FileManagers
from orthomosaic_tools import OrthomosaicTools


#instantiate file managers and orthomosaic tools
fm = FileManagers()
ot = OrthomosaicTools()

#select videos and corresponding GCPS file
video = fm.load_fn("Video")
gcps = fm.import_gcps()

video1 = fm.load_fn("Video1")
gcps1= fm.import_gcps()

video2 = fm.load_fn("Video2")
gcps2 = fm.import_gcps()

video3 = fm.load_fn("Video3")
gcps3 = fm.import_gcps()

#create lists to send to the function we made
videos = [video, video1, video2, video3]
print(videos)

gcps_list = [gcps, gcps1, gcps2, gcps3]
print(gcps_list)

#time offsets between the videos (in ms)
offsets = [0, 1400, -1000, 5100]

#choose start time for first video and length to process
start = 15
length = 3

#choose compression and output speed
compress = 5
speed = 1

#output video file information
output_path = fm.load_dn("Choose a directory to store video in")
outn = "test1"

#run function!
ot.orthomosaic_video(videos, gcps_list, offsets, output_path, outn, start_time_s = start, length_s = length, compress_by = compress, out_speed = speed)
