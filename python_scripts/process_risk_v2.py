import pandas as pd
import numpy as np

# Load CSV files into DataFrames
clients_df = pd.read_csv("data/clients.csv")
transactions_df = pd.read_csv("data/transactions.csv")
risk_events_df = pd.read_csv("data/risk_events.csv")

print(clients_df,transactions_df,risk_events_df)

# Convert date related columns to proper date format
transactions_df["transaction_date"] = pd.to_datetime(transactions_df["transaction_date"])
risk_events_df["evaluation_timestamp"] = pd.to_datetime(risk_events_df["evaluation_timestamp"])

# Define high-risk countries
HIGH_RISK_COUNTRIES = ["Russia", "North Korea", "Iran"]

# Define risk scoring function
def calculate_risk_score(row):
    risk_score = 0
    trigger_reasons = []

    # Rule 1: High Transaction Amount
    if row["transaction_amount"] > 10000:
        risk_score += 50
        trigger_reasons.append("High Transaction Amount")

    # Rule 2: Client from High-Risk Country
    if row["country"] in HIGH_RISK_COUNTRIES:
        risk_score += 40
        trigger_reasons.append("High-Risk Country")

    # Rule 3: Frequent Transactions in the Last 7 Days
    recent_transactions = transactions_df[
        (transactions_df["client_id"] == row["client_id"]) &
        (transactions_df["transaction_date"] >= row["transaction_date"] - pd.Timedelta(days=7))
    ]
    if len(recent_transactions) > 5:
        risk_score += 30
        trigger_reasons.append("Frequent Transactions")

    return risk_score, ", ".join(trigger_reasons) if trigger_reasons else "No Risk"

# Merge transactions with client data
merged_df = transactions_df.merge(clients_df, on="client_id")
print(merged_df)
# Apply risk scoring to each transaction
merged_df[["risk_score", "trigger_reason"]] = merged_df.apply(
    lambda row: pd.Series(calculate_risk_score(row)), axis=1
)
print(risk_events_df)
# Merge risk scores with existing risk events
risk_output_df = merged_df.merge(risk_events_df, on=["client_id"], how="left")
print(risk_output_df)
# Fill missing risk event details
risk_output_df["risk_score"] = risk_output_df["risk_score_y"].fillna(0)
risk_output_df["trigger_reason"] = risk_output_df["trigger_reason_x"].fillna("No Risk")

# Save output dataset
risk_output_df.to_csv("data/client_risk_output.csv", index=False)

# Display sample output
print(risk_output_df[["client_id", "transaction_id", "transaction_amount", "risk_score", "trigger_reason"]].head())
