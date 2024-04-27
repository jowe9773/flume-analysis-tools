#load functions from functions file
from sick_functions import load_sick_file
from sick_functions import interpolate_nans
from sick_functions import save_jpeg

#choose a file containing processed sick scans (as they come from the cart computer)
topo_raw = load_sick_file()

topo_int = interpolate_nans(topo_raw)

#save data
save_jpeg(topo_int)