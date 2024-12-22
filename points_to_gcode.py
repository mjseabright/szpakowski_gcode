import numpy as np
import csv

input_file = 'b9_points.txt'
output_file = 'b9_line_2.gcode'

input_grid_size = 12 # Grid size of input points (mm)
output_grid_size = 3 # Desired grid size of output gcode (mm)

center_coord = [128, 126] # Center coordinate for output gcode

e_per_grid = 0.342 # Amount to extrude per grid (mm)


def main():
    scale_factor = output_grid_size / input_grid_size

    points = []

    # Read in points, and scale by scale_factor
    with open(input_file, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            if len(row) != 2:
                raise ValueError("Each line in the CSV must contain exactly two floats.")
            scaled_values = [float(value) * scale_factor for value in row]
            points.extend(scaled_values)

    points_np = np.array(points)

    # Calculate min and max locations for each axis
    reshaped_array = points_np.reshape(-1, 2)
    first_column = reshaped_array[:, 0]
    second_column = reshaped_array[:, 1]
    mins = [np.min(first_column), np.min(second_column)]
    maxs = [np.max(first_column), np.max(second_column)]

    # Offset points so the center_coord is in the center
    x_offset = (mins[0] + maxs[0]) / 2 - center_coord[0]
    y_offset = (mins[1] + maxs[1]) / 2 - center_coord[1]
    translated_points = reshaped_array - np.array([x_offset, y_offset]).reshape(-1)

    # Flip Y coordinates as SVG has Y going downwards
    translated_points[:, 1] = -1 * (translated_points[:, 1] - center_coord[1]) + center_coord[1]

    # Write out gcode to file
    with open(output_file, 'w') as file:
        for x, y in translated_points:
            file.write(f"G1 X{x:.3f} Y{y:.3f} E{e_per_grid:.3f}\n")


if __name__ == '__main__':
    main()
