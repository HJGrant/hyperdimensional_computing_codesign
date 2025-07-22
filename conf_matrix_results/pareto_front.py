import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load your .npy dataset
data = np.load("inference_results.npy", allow_pickle=True)
df = pd.DataFrame(data.tolist())
print(df.columns.tolist())

# OPTIONAL: If any column is a numpy float type, convert it to float for consistency
df['avg_power_vec'] = df['avg_power_vec'].astype(float)
df['inference_result'] = df['inference_result'].astype(float)

# Define Pareto front function
def is_pareto_efficient(costs):
    is_efficient = np.ones(costs.shape[0], dtype=bool)
    for i, c in enumerate(costs):
        if is_efficient[i]:
            is_efficient[is_efficient] = np.any(costs[is_efficient] < c, axis=1) | np.all(costs[is_efficient] == c, axis=1)
            is_efficient[i] = True
    return is_efficient

# We want to MINIMIZE power and MAXIMIZE accuracy => negate accuracy
costs = np.column_stack((df['avg_power_vec'], -df['inference_result']))
pareto_mask = is_pareto_efficient(costs)

# Extract Pareto-optimal rows
pareto_df = df[pareto_mask].copy()

# Sort to see top entries
pareto_df = pareto_df.sort_values(by='inference_result', ascending=False)

# Show top results
print("\nPareto-optimal configurations (detailed):")
for _, row in pareto_df.iterrows():
    print(f"vec_dim={row['vec_dim']:>4}, block_size={row['block_size']:>2}, "
          f"precision={row['precision']:>2}, vdd={row['vdd']:.1f}, "
          f"power={row['avg_power_vec']:.6f}, accuracy={row['inference_result']:.4f}")

# Optional: visualize
plt.figure(figsize=(8, 5))
plt.scatter(df['avg_power_vec'], df['inference_result'], label="All configs", alpha=0.4)
plt.scatter(pareto_df['avg_power_vec'], pareto_df['inference_result'], color='red', label="Pareto-optimal")
plt.xlabel("Average Power per Vector")
plt.ylabel("Inference Accuracy")
plt.title("Pareto Front: Accuracy vs Power")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
