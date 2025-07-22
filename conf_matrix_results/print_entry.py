import numpy as np

# Load your .npy file
data = np.load("inference_results.npy", allow_pickle=True)

# Filter for the desired configuration
target_entry = None
for entry in data:
    if (
        entry["vec_dim"] == 2048
        and entry["precision"] == 5
        and entry["vdd"] == 0.5
        and entry["block_size"] == 8
    ):
        target_entry = entry
        break

# Display the result
if target_entry:
    print("Confusion matrix for vec_dim=2048, precision=5, vdd=0.5, block_size=8:\n")
    print(target_entry["conf_matrix"])
else:
    print("No matching configuration found.")
