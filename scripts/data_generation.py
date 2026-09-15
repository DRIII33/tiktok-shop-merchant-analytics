import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

NUM_MERCHANTS = 50000

merchant_ids = [f"MERCH_{100000 + i}" for i in range(NUM_MERCHANTS)]
regions = np.random.choice(["US_West", "US_East", "US_Central", "US_South"], size=NUM_MERCHANTS, p=[0.30, 0.35, 0.15, 0.20])
merchant_categories = np.random.choice(["Apparel", "Beauty_Personal_Care", "Electronics", "Home_Improvement", "Collectibles"], size=NUM_MERCHANTS, p=[0.35, 0.25, 0.15, 0.15, 0.10])

# Onboarding Start Dates
start_dates = [datetime(2026, 1, 1) + timedelta(days=int(np.random.randint(0, 180))) for _ in range(NUM_MERCHANTS)]

# Simulate Funnel Progression
kyc_submitted = np.random.choice([1, 0], size=NUM_MERCHANTS, p=[0.90, 0.10])
kyc_approved = np.where(kyc_submitted == 1, np.random.choice([1, 0], size=NUM_MERCHANTS, p=[0.85, 0.15]), 0)
catalog_uploaded = np.where(kyc_approved == 1, np.random.choice([1, 0], size=NUM_MERCHANTS, p=[0.75, 0.25]), 0)
logistics_configured = np.where(catalog_uploaded == 1, np.random.choice([1, 0], size=NUM_MERCHANTS, p=[0.80, 0.20]), 0)

# Onboarding Experiment Allocation (A/B Test Variant v2.0 vs Control v1.0)
ab_group = np.random.choice(["Control_v1.0", "Variant_v2.0"], size=NUM_MERCHANTS, p=[0.50, 0.50])

# Activate (First Sale within 30 days) - Variant v2.0 increases activation likelihood
activation_prob = np.where(
    logistics_configured == 1,
    np.where(ab_group == "Variant_v2.0", 0.58, 0.48),
    0.0
)
activated_30d = np.random.binomial(1, activation_prob)

# 30-Day GMV ($)
gmv_30d = np.where(
    activated_30d == 1,
    np.round(np.random.exponential(scale=1200, size=NUM_MERCHANTS) + 50, 2),
    0.00
)

# Support Tickets Raised
support_tickets = np.random.poisson(lam=1.2, size=NUM_MERCHANTS)

df = pd.DataFrame({
    "merchant_id": merchant_ids,
    "region": regions,
    "category": merchant_categories,
    "onboarding_start_date": start_dates,
    "ab_group": ab_group,
    "kyc_submitted": kyc_submitted,
    "kyc_approved": kyc_approved,
    "catalog_uploaded": catalog_uploaded,
    "logistics_configured": logistics_configured,
    "activated_30d": activated_30d,
    "gmv_30d": gmv_30d,
    "support_tickets_raised": support_tickets
})

# Export to CSV
df.to_csv("tiktok_shop_merchant_onboarding_raw.csv", index=False)
print("Dataset generated successfully with 50,000 records.")
