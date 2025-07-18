import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata
from scipy.ndimage import maximum_filter

# Step 1: Read the CSV file
data = pd.read_csv('results.csv')  # Replace with the path to your CSV file

# Get unique precisions
unique_precisions = data['Precision'].unique()

# Iterate over each unique precision
for precision in unique_precisions:
    # Filter data for the current precision
    subset = data[data['Precision'] == precision]

    # Calculate the ratio of Dimension to Block Size
    subset['Dimension_BlockSize_Ratio'] = subset['Dimension'] / subset['Block Size']

    # Extract the data
    ratios = subset['Dimension_BlockSize_Ratio'].values
    dimensions = subset['Dimension'].values
    results = subset['Results'].values

    # Create a grid for the surface plot
    grid_x, grid_y = np.mgrid[min(ratios):max(ratios):100j, min(dimensions):max(dimensions):100j]

    # Interpolate the results onto the grid
    grid_z = griddata((ratios, dimensions), results, (grid_x, grid_y), method='linear')

    # Find local maxima
    neighborhood_size = 3  # Define the neighborhood size for finding local maxima
    local_maxima = (grid_z == maximum_filter(grid_z, size=neighborhood_size)) & (grid_z > 0.85)

    # Get the coordinates and values of local maxima
    max_indices = np.argwhere(local_maxima)
    max_x = grid_x[max_indices[:, 0], max_indices[:, 1]]
    max_y = grid_y[max_indices[:, 0], max_indices[:, 1]]
    max_z = grid_z[max_indices[:, 0], max_indices[:, 1]]

    # Print the values of local maxima
    for i in range(len(max_x)):
        print(f"Local Maximum {i + 1}:")
        print(f"  Dimension/Block Size Ratio: {max_x[i]}")
        print(f"  Dimension: {max_y[i]}")
        print(f"  Results: {max_z[i]}\n")

    # Step 3: Create the 3D plot
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')

    # Plot the surface
    surface = ax.plot_surface(grid_x, grid_y, grid_z, cmap='viridis', edgecolor='none')

    # Plot and annotate the local maxima
    for i in range(len(max_x)):
        ax.scatter(max_x[i], max_y[i], max_z[i], color='red', s=50)
        ax.text(max_x[i], max_y[i], max_z[i], f"({max_x[i]:.2f}, {max_y[i]:.2f}, {max_z[i]:.2f})", color='black')

    # Set labels
    ax.set_title(f'Precision: {precision}')
    ax.set_xlabel('Dimension/Block Size Ratio')
    ax.set_ylabel('Dimension')
    ax.set_zlabel('Results')

    # Add a color bar which maps values to colors
    fig.colorbar(surface, ax=ax, shrink=0.5, aspect=5)

    # Show the plot
    plt.show()
