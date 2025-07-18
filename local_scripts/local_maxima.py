import pandas as pd
import numpy as np
from scipy.interpolate import griddata
from scipy.ndimage import maximum_filter
from scipy.spatial.distance import cdist

# Step 1: Read the CSV file
data = pd.read_csv('results.csv')  # Replace with the path to your CSV file

# Prepare a list to store the mapped maxima
mapped_maxima = []

# Get unique precisions
unique_precisions = data['Precision'].unique()

# Iterate over each unique precision
for precision in unique_precisions:
    # Filter data for the current precision and make a copy
    subset = data[data['Precision'] == precision].copy()

    # Calculate the ratio of Dimension to Block Size
    subset.loc[:, 'Dimension_BlockSize_Ratio'] = subset['Dimension'] / subset['Block Size']

    # Extract the data
    ratios = subset['Dimension_BlockSize_Ratio'].values
    dimensions = subset['Dimension'].values
    block_sizes = subset['Block Size'].values
    results = subset['Results'].values

    # Create a grid for the surface plot
    grid_x, grid_y = np.mgrid[min(ratios):max(ratios):100j, min(dimensions):max(dimensions):100j]

    # Interpolate the results onto the grid
    grid_z = griddata((ratios, dimensions), results, (grid_x, grid_y), method='linear')

    # Clip the interpolated values to the range [0, 1]

    # Find local maxima
    neighborhood_size = 3
    local_maxima = (grid_z == maximum_filter(grid_z, size=neighborhood_size)) & (grid_z > 0.85)

    # Get the coordinates of local maxima
    max_indices = np.argwhere(local_maxima)
    max_x = grid_x[max_indices[:, 0], max_indices[:, 1]]
    max_y = grid_y[max_indices[:, 0], max_indices[:, 1]]
    max_z = grid_z[max_indices[:, 0], max_indices[:, 1]]

    # Create a DataFrame for the original data points including block size
    original_points = subset[['Dimension_BlockSize_Ratio', 'Dimension', 'Block Size', 'Results']].values

    # Find the nearest original point for each local maximum
    for i in range(len(max_x)):
        # Calculate distances between the local maximum and all original points
        distances = cdist([[max_x[i], max_y[i]]], original_points[:, :2])  # Use only ratio and dimension for distance

        # Find the index of the nearest original point
        nearest_idx = np.argmin(distances)

        # Get the nearest original point including block size
        nearest_point = original_points[nearest_idx]

        # Store the mapped maximum including block size
        mapped_maxima.append({
            'Precision': precision,
            'Interpolated_Ratio': max_x[i],
            'Interpolated_Dimension': max_y[i],
            'Interpolated_Results': max_z[i],
            'Nearest_Ratio': nearest_point[0],
            'Nearest_Dimension': nearest_point[1],
            'Nearest_Block_Size': nearest_point[2],
            'Nearest_Results': nearest_point[3]
        })

# Convert the list of mapped maxima to a DataFrame
mapped_maxima_df = pd.DataFrame(mapped_maxima)

# Write the results to a new CSV file
mapped_maxima_df.to_csv('mapped_maxima.csv', index=False)
