-- Create Analytics View: Merchant Onboarding & Activation Metrics
CREATE OR REPLACE VIEW `driiiportfolio.tiktok_shop_analytics.vw_merchant_funnel_performance` AS
SELECT
  merchant_id,
  region,
  category,
  DATE(onboarding_start_date) AS start_date,
  ab_group,
  kyc_submitted,
  kyc_approved,
  catalog_uploaded,
  logistics_configured,
  activated_30d,
  gmv_30d,
  support_tickets_raised,
  
  -- Funnel Step Calculations
  CASE
    WHEN kyc_submitted = 0 THEN '01_KYC_Pending'
    WHEN kyc_approved = 0 THEN '02_KYC_Rejected'
    WHEN catalog_uploaded = 0 THEN '03_Catalog_Pending'
    WHEN logistics_configured = 0 THEN '04_Logistics_Pending'
    WHEN activated_30d = 0 THEN '05_Configured_Zero_GMV'
    ELSE '06_Fully_Activated'
  END AS merchant_lifecycle_stage,
  
  -- Flag High-Value Merchants (GMV > $2,500)
  CASE WHEN gmv_30d >= 2500 THEN 1 ELSE 0 END AS is_high_value_merchant
FROM
  `driiiportfolio.tiktok_shop_analytics.raw_merchant_onboarding`;

-- Create Aggregated Executive Summary View for Looker Studio
CREATE OR REPLACE VIEW `driiiportfolio.tiktok_shop_analytics.vw_executive_summary_kpis` AS
SELECT
  region,
  category,
  ab_group,
  COUNT(merchant_id) AS total_merchants,
  SUM(kyc_approved) AS total_approved,
  SUM(logistics_configured) AS total_fully_configured,
  SUM(activated_30d) AS total_activated,
  ROUND(SAFE_DIVIDE(SUM(activated_30d), SUM(logistics_configured)) * 100, 2) AS activation_rate_pct,
  ROUND(SUM(gmv_30d), 2) AS total_gmv_30d,
  ROUND(AVG(gmv_30d), 2) AS avg_gmv_per_merchant,
  ROUND(AVG(support_tickets_raised), 2) AS avg_support_tickets
FROM
  `driiiportfolio.tiktok_shop_analytics.vw_merchant_funnel_performance`
GROUP BY
  region, category, ab_group;
