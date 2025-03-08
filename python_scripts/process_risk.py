import pandas as pd
from datetime import datetime

# Load data
clients_df = pd.read_csv("data/clients.csv")
transactions_df = pd.read_csv("data/transactions.csv")

# Define high-risk countries
high_risk_countries = ["Russia"]

# Join data sources
merged_df = transactions_df.merge(clients_df, on="client_id")

# Apply risk scoring
risk_events = []

for _, row in merged_df.iterrows():
    risk_score = 0
    reason = ""

    # High transaction amount
    if row["transaction_amount"] > 10000:
        risk_score += 50
        reason += "High transaction amount. "

    # High-risk country
    if row["country"] in high_risk_countries:
        risk_score += 30
        reason += "Client from high-risk country. "

    # Save risk event
    if risk_score > 0:
        risk_events.append({
            "event_id": len(risk_events) + 1,
            "client_id": row["client_id"],
            "risk_score": risk_score,
            "trigger_reason": reason,
            "evaluation_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

# Convert to DataFrame
risk_events_df = pd.DataFrame(risk_events)
risk_events_df.to_csv("data/risk_events.csv", index=False)

print("Risk Events Generated:")
print(risk_events_df)
