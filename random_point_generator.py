#random_point_generator.py

#this file is going to be used to find random points within the flume. 

from file_managers import FileManagers
import random
import csv

fm = FileManagers()

def generate_random_coordinates(min_x, max_x, min_y, max_y, min_deg, max_deg, num_points):
    coordinates = []
    for _ in range(num_points):
        x = random.uniform(min_x, max_x)
        y = random.uniform(min_y, max_y)
        deg = random.uniform(min_deg, max_deg)
        coordinates.append((x, y, deg))
    return coordinates

def save_coordinates_to_csv(short_coords, inter_coords, long_coords, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["x", "y", "deg", "type"])  # Write the header row
        for coord in short_coords:
            writer.writerow([coord[0], coord[1], coord[2], "short"])
        for coord in inter_coords:
            writer.writerow([coord[0], coord[1], coord[2], "intermediate"])
        for coord in long_coords:
            writer.writerow([coord[0], coord[1], coord[2], "long"])

# Number of pieces of each size
short = 79
intermediate = 59
long = 15

# Coordinates of bounding box for points
xlow = 1000
xhigh = 8750
ylow = -1700
yhigh = 1700

# Possible range of angle
deglow = 0
deghigh = 180

# Generate the random coordinates for each point size
short_random_coordinates = generate_random_coordinates(xlow, xhigh, ylow, yhigh, deglow, deghigh, short)
inter_random_coordinates = generate_random_coordinates(xlow, xhigh, ylow, yhigh, deglow, deghigh, intermediate)
long_random_coordinates = generate_random_coordinates(xlow, xhigh, ylow, yhigh, deglow, deghigh, long)

# Print the lists of coords
print("Short Coordinates:", short_random_coordinates)
print("Intermediate Coordinates:", inter_random_coordinates)
print("Long Coordinates:", long_random_coordinates)

# Save the random coordinates to a CSV file
csv_filename = fm.load_dn("Choose location to store points in") + "/points.csv"
save_coordinates_to_csv(short_random_coordinates, inter_random_coordinates, long_random_coordinates, csv_filename)

print(f"Random coordinates saved to {csv_filename}")