#######################
# LOADING A SICK FILE #
#######################

def load_sick_file():
    
    #import neccesary packages
    import numpy as np
    import tkinter as tk
    from tkinter import filedialog

    #location of data of interest
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename()
    

    #gather values from the filename 
    low_x = float(file_path[-54:-46])
    high_x = float(file_path[-31:-23])
    dx = float(file_path[-71:-66])

    #load data into a 1D numpy array
    with open(file_path, 'rb') as fid:
        array = np.fromfile(fid, np.float32)

    ####################################
    # Change the array into a 2D array #
    ####################################
    #determine width of the array
    arr_width = high_x - low_x

    #determine number of adjacent profiles in the x direction (swath)
    swath = int(arr_width / dx + 1)

    #reshape the SICK data to the shape of the image
    topoprenan = np.reshape(array, (-1, swath))

    #Lets identify the -9999 and make then Nans
    topo = np.where(topoprenan < 0, np.nan, topoprenan)

    return topo

def select_topo_points(topo, colors = 'terrain'):
    #function to save selected points coordinates and z value
    import matplotlib.pyplot as plt
    import numpy as np

    fig = plt.figure(figsize=(15,8))
    ax = fig.add_subplot(111)
    ax.set_facecolor((0.0, 0.0, 0.0))
    ax = plt.imshow(topo, cmap = colors, vmin = np.nanmin(topo), vmax = np.nanmax(topo))
    ax = plt.colorbar()
    ax = plt.tight_layout()
    
    pair = []
    

    def onclick(event):
        
        if event.dblclick:
            zdata = topo[int(np.round(event.ydata)), int(np.round(event.xdata))]
            print('button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
                (event.button, event.x, event.y, event.xdata, event.ydata), 'zdata=', zdata)
            
            point = []                  #create and fill a list for x,y data for a point
            point.append(event.xdata)
            point.append(event.ydata)

            pair.append(point) #add this point to the list of control points

            plt.plot(event.xdata, event.ydata, 'o')
            fig.canvas.draw()
            #print("Points:", pair)

    def close_piece(event):
        if event.key == "x":
            print("The x key was pressed and the figure was closed")
            plt.close(fig)

    cid = fig.canvas.mpl_connect('button_press_event', onclick) #connects the button event with the actions in onclick
    cid = fig.canvas.mpl_connect("key_press_event", close_piece) # connects key event with actions in close_piece


    fig.canvas.toolbar.zoom()    
    
    ax = plt.show()

def interpolate_nans(arr):
    import numpy as np
    from scipy import interpolate

    # Create grid coordinates
    rows, cols = np.indices(arr.shape)
    coords = np.column_stack((rows.flatten(), cols.flatten()))

    # Identify non-NaN values and their coordinates
    non_nan_coords = coords[~np.isnan(arr).flatten()]
    non_nan_values = arr[~np.isnan(arr)]

    # Interpolate NaN values using griddata
    interpolated_values = interpolate.griddata(non_nan_coords, non_nan_values, coords, method='linear')

    # Reshape the interpolated values to match the original array shape
    arr_interpolated = interpolated_values.reshape(arr.shape)

    print("Original array:\n", arr)
    print("\nArray with NaNs interpolated:\n", arr_interpolated)

    return(arr_interpolated)

def single_out_wood(topo, min_difference):
    import numpy as np

    change = np.where(topo < min_difference, np.nan, topo)

    wood = np.where(change >= min_difference, 1.0, change)

#    from scipy.ndimage import label

    # Set a threshold for the minimum size of a connected cluster
#    min_cluster_size = 300

    # Iterate over unique values in the array
#    for value in np.unique(topo[~np.isnan(topo)]):
        # Binary array indicating where the current value is present
#        binary_array = topo == value
        
        # Identify connected clusters for the current value
#        labeled_array, num_clusters = label(binary_array)
        
        # Get the size of each cluster
#        cluster_sizes = np.bincount(labeled_array.ravel())
        
        # Find clusters with sizes less than the threshold
#        small_clusters = np.where(cluster_sizes < min_cluster_size)[0]
        
        # Replace values in small clusters with NaN
#        for cluster in small_clusters:
#            topo[labeled_array == cluster] = np.nan

    return(wood)

def save_jpeg(topo):
    #import neccesary packages
    import numpy as np
    import tkinter as tk
    from tkinter import filedialog

    #open file dialog to choose location and name to store file as
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.asksaveasfilename()

    #Exporting a np array as a tiff
    from PIL import Image
    im = Image.fromarray(np.uint16(topo))
    im.save(file_path + ".tiff")