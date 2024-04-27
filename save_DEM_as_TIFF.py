#load functions from functions file
from sick_functions import *
from sick_functions import save_jpeg

#choose a file containing processed sick scans (as they come from the cart computer)
topo_raw = load_sick_file()

#save data
save_jpeg(topo_raw)
