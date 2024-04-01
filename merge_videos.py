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

offsets = [0, 1400, -1000, 5100]

#output_path = fm.load_dn("Choose a directory to store video in")

output_path = 'C:/Users/josie/OneDrive/Desktop/GoPro Video Test/'
outn = "winter_PIV_video_no_wood"

ot.orthomosaic_video(videos, gcps_list, offsets, output_path, outn, start_time_s = 15, length_s = 90, compress_by = 5, out_speed = 1)
