# flume-analysis-tools
This repository contains the tools I have developed for processing the data collected during my flume experiments. This readme contains an overview of the tools included as well as instructions for use. 

# Files
## file_managers.py 
This file has a range of file management tools that allow GUI selection of the files and directories of interest.

### load_dn(self, purpose) ### : 
        This function opens a tkinter GUI for selecting a directory and returns the full path to the directory once selected.

        * purpose *: provides expanatory text in the GUI that tells the user what directory to select.