import pandas as pd
import numpy as np
from scipy import stats

# Read dataset
df = pd.read_csv("tiktok_shop_merchant_onboarding_raw.csv")

# Filter for fully configured merchants reaching activation decision point
df_eval = df[df['logistics_configured'] == 1]

control = df_eval[df_eval['ab_group'] == 'Control_v1.0']['activated_30d']
variant = df_eval[df_eval['ab_group'] == 'Variant_v2.0']['activated_30d']

# Sample sizes and successes
n_control, n_variant = len(control), len(variant)
success_control, success_variant = control.sum(), variant.sum()

p_control = success_control / n_control
p_variant = success_variant / n_variant

# Pooled Proportion Z-Test
p_pooled = (success_control + success_variant) / (n_control + n_variant)
se = np.sqrt(p_pooled * (1 - p_pooled) * ((1 / n_control) + (1 / n_variant)))
z_stat = (p_variant - p_control) / se
p_value = stats.norm.sf(abs(z_stat)) * 2

abs_lift = p_variant - p_control
rel_lift = (p_variant - p_control) / p_control * 100

print("=== TIKTOK SHOP A/B EXPERIMENTATION RESULTS ===")
print(f"Control v1.0 Activation Rate: {p_control:.4f} (n = {n_control})")
print(f"Variant v2.0 Activation Rate: {p_variant:.4f} (n = {n_variant})")
print(f"Absolute Lift: {abs_lift * 100:.2f}%")
print(f"Relative Lift: {rel_lift:.2f}%")
print(f"Z-Statistic: {z_stat:.4f}")
print(f"P-Value: {p_value:.4e}")

if p_value < 0.001:
    print("DECISION: Statistically significant positive lift detected (p < 0.001). Recommend 100% rollout of Variant v2.0.")
