import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Load CSV
df = pd.read_csv('results.csv')

# Assume columns: input1, input2, input3, result
x = df['Dimension']
y = df['Block Size']
z = df['Precision']
result = df['Results']

fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

# Make marker size proportional and add edge color for clarity
sc = ax.scatter(x, y, z, c=result, cmap='viridis', s=40, edgecolor='k', alpha=0.8)

# Optional: Connecting the points to create a wave/line effect
ax.plot(x, y, z, color='gray', linewidth=0.5, alpha=0.6)


ax.set_xlabel('Dimension')
ax.set_ylabel('Block Size')
ax.set_zlabel('Precision')

ax.view_init(elev=30, azim=135)  # Adjust for better viewing angle
ax.grid(True)

fig.colorbar(sc, label='Result Value')

plt.tight_layout()
plt.show()