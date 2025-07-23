import pandas as pd
import numpy as np

# Step 1: Load the Pareto data
df = pd.read_csv("inference_pareto.csv")


df = df[df["inference_result"] >= 0.9].copy()
# Step 2: Sort by increasing power (optional, but helps ensure consistent slope calculation)
df = df.sort_values(by="avg_power_vec").reset_index(drop=True)

# Step 3: Compute finite differences (first derivative)
x = df["avg_power_vec"].values
y = df["inference_result"].values

dx = np.diff(x)
dy = np.diff(y)
slope = dy / dx  # Δaccuracy / Δpower

# Step 4: Create new DataFrame (slope has one less element than x)
deriv_df = df.iloc[:-1].copy()
deriv_df["slope"] = slope

# Step 5: Save the result
deriv_df.to_csv("inference_pareto_derivative.csv", index=False)
print("Saved to inference_pareto_derivative.csv")