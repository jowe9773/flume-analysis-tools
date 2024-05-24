#rand_fp_points.py

import geopandas as gpd
from file_managers import FileManagers

def shapefile_to_csv(shapefile_path, csv_path):
    # Read the shapefile
    gdf = gpd.read_file(shapefile_path)
    
    # Extract x and y coordinates
    gdf['x'] = gdf.geometry.x
    gdf['y'] = gdf.geometry.y
    gdf['path'] = gdf['path']
    
    # Save to CSV
    gdf[['x', 'y', 'path']].to_csv(csv_path, index=False)


fm = FileManagers()
shapefile_path = fm.load_fn("Choose shapefile")
csv_path = fm.load_dn("Choose destination folder for csv") + "/points.csv"

# Example usage
shapefile_to_csv(shapefile_path, csv_path)
