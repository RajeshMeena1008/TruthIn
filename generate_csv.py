"""
generate_csv.py
Run once to create nutriscan_data.csv training dataset.
"""
import numpy as np
import pandas as pd

np.random.seed(42)
rows = []

# Healthy
for _ in range(250):
    rows.append({"calories": np.random.uniform(40,200), "fat": np.random.uniform(0,7),
                 "sugar": np.random.uniform(0,5), "protein": np.random.uniform(10,35),
                 "sodium": np.random.uniform(0,180), "label": "Healthy"})
# Moderate
for _ in range(250):
    rows.append({"calories": np.random.uniform(200,380), "fat": np.random.uniform(7,18),
                 "sugar": np.random.uniform(5,14), "protein": np.random.uniform(4,14),
                 "sodium": np.random.uniform(180,500), "label": "Moderate"})
# Unhealthy
for _ in range(250):
    rows.append({"calories": np.random.uniform(380,650), "fat": np.random.uniform(18,45),
                 "sugar": np.random.uniform(14,55), "protein": np.random.uniform(0,9),
                 "sodium": np.random.uniform(500,1400), "label": "Unhealthy"})

df = pd.DataFrame(rows)
df = df.sample(frac=1).reset_index(drop=True)
df.to_csv("nutriscan_data.csv", index=False)
print(f"Generated nutriscan_data.csv with {len(df)} rows.")
