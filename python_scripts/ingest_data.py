import pandas as pd

# Load CSV files into Pandas DataFrames
clients_df = pd.read_csv("data/clients.csv")
transactions_df = pd.read_csv("data/transactions.csv")

# Display loaded data
print("Clients Data:")
print(clients_df)

print("\nTransactions Data:")
print(transactions_df)
