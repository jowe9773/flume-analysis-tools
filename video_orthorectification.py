#video_orthorectification.py
"""script for orthorecifying a video"""

#load neccesary packages and modules
from orthomosaic_tools import OrthomosaicTools
from file_managers import FileManagers

#create an instance of the OrthomosaicTools class and the FileManagers class
ot = OrthomosaicTools()
fm = FileManagers()

#select video to orthorectify
in_vid = fm.load_fn("select video you wish to orthorectify")

#select GCPs file
gcps = fm.import_gcps()

#choose camera, start time (seconds) and length (seconds)
CAM = 4
START_TIME = 2
LENGTH = 10

#select directory to store orthorectified video in
out_dn = fm.load_dn("delect directory to store orthorecitfied video in")

ot.orthorectify_video(cam=CAM,
                      start_time_s=START_TIME,
                      length_s=LENGTH,
                      input_fn=in_vid,
                      output_dn=out_dn,
                      gcps = gcps)
