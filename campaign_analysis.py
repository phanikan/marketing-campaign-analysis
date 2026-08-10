"""
Compares ROI, CTR, CPC, and conversion rate across marketing campaigns.

Expects a campaign_interactions.csv with columns:
customer_id, campaign_id, channel, clicks, impressions, cost, conversion, interaction_date
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def load_interactions(path="campaign_interactions.csv"):
    df = pd.read_csv(path, parse_dates=["interaction_date"])
    return df


def campaign_rollup(df):
    rollup = df.groupby(["campaign_id", "channel"]).agg(
        impressions=("impressions", "sum"),
        clicks=("clicks", "sum"),
        conversions=("conversion", "sum"),
        cost=("cost", "sum"),
    ).reset_index()

    rollup["ctr"] = rollup["clicks"] / rollup["impressions"].replace(0, np.nan)
    rollup["cpc"] = rollup["cost"] / rollup["clicks"].replace(0, np.nan)
    rollup["conversion_rate"] = rollup["conversions"] / rollup["clicks"].replace(0, np.nan)
    rollup["cost_per_conversion"] = rollup["cost"] / rollup["conversions"].replace(0, np.nan)
    rollup["roi"] = (rollup["conversions"] * 50 - rollup["cost"]) / rollup["cost"].replace(0, np.nan)

    return rollup.sort_values("roi", ascending=False)


def plot_roi_comparison(rollup, out_path="roi_by_campaign.png"):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(rollup["campaign_id"].astype(str), rollup["roi"])
    ax.set_xlabel("Campaign")
    ax.set_ylabel("ROI")
    ax.set_title("ROI by campaign")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(out_path)
    print(f"Saved {out_path}")


def generate_sample_data(n=100_000, path="campaign_interactions.csv"):
    """Synthetic dataset for testing when you don't have real data on hand."""
    rng = np.random.default_rng(42)

    customers = [f"CUST{str(i).zfill(6)}" for i in range(15000)]
    campaigns = [f"CAMP{i}" for i in range(12)]
    channels = ["email", "search", "social", "display"]

    start = pd.Timestamp("2023-02-01")
    end = pd.Timestamp("2023-04-30")
    dates = pd.to_datetime(rng.integers(start.value, end.value, n))

    impressions = rng.integers(1, 50, n)
    clicks = np.minimum(impressions, rng.poisson(2, n))
    conversions = np.minimum(clicks, rng.binomial(clicks, 0.08))
    cost = np.round(clicks * rng.uniform(0.5, 4.0, n), 2)

    df = pd.DataFrame({
        "customer_id": rng.choice(customers, n),
        "campaign_id": rng.choice(campaigns, n),
        "channel": rng.choice(channels, n),
        "impressions": impressions,
        "clicks": clicks,
        "conversion": conversions,
        "cost": cost,
        "interaction_date": dates,
    })

    df.to_csv(path, index=False)
    return df


if __name__ == "__main__":
    try:
        interactions = load_interactions()
    except FileNotFoundError:
        print("No campaign_interactions.csv found, generating a sample dataset for a test run.")
        interactions = generate_sample_data()

    rollup = campaign_rollup(interactions)
    print(rollup[["campaign_id", "channel", "ctr", "cpc", "conversion_rate", "roi"]].to_string(index=False))

    rollup.to_csv("campaign_rollup.csv", index=False)
    print("Wrote campaign_rollup.csv")

    plot_roi_comparison(rollup)
