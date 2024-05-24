#sick_analysis.py

#load functions from functions file
from sick_functions import *
from sick_functions import select_topo_points
from sick_functions import interpolate_nans
from sick_functions import save_jpeg

#choose a file containing processed sick scans (as they come from the cart computer)
topo_raw = load_sick_file()


#view the raw topo
select_topo_points(topo_raw)

#interpolate nan values
interpolated = interpolate_nans(topo_raw)

#view the difference map
select_topo_points(interpolated, colors = 'YlOrBr')

#save data
save_jpeg(interpolated)
