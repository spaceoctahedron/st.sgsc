import pandas as pd
import random

# Load data from Excel file
def load_data():
    return pd.read_excel("./data/cereals_info.xlsx")

import pandas as pd
import random

# Load data from Excel file
def load_data():
    return pd.read_excel("./data/cereals_info.xlsx")

# Simulate inventory data
def simulate_inventory(df):
    df['Stock actuel'] = [random.randint(0, 100) for _ in range(len(df))]
    df['Stock maximum'] = [random.randint(100, 200) for _ in range(len(df))]
    df['Niveau critique'] = df['Stock maximum'] * 0.2
    return df

# Calculate order amount
def calculate_order_amount(row):
    if row['Stock actuel'] <= row['Niveau critique']:
        return row['Stock maximum'] - row['Stock actuel']
    return 0

# Load and prepare data
df_inventory = load_data()
df_inventory = simulate_inventory(df_inventory)
df_inventory['Quantité à commander'] = df_inventory.apply(calculate_order_amount, axis=1)

print(df_inventory.columns)
print(df_inventory.head(1))
print(df_inventory['Image'].head(1))
print(df_inventory.columns.tolist())