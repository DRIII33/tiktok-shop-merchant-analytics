-- BigQuery View Alternative: vw_diagnostic_summary
-- This view combines aggregated KPIs with the Google Sheets summary data
-- to provide a comprehensive dataset for the diagnostic table.
CREATE OR REPLACE VIEW `driiiportfolio.tiktok_shop_analytics.vw_diagnostic_summary` AS
SELECT
    kpis.region,
    kpis.category,
    kpis.ab_group,
    kpis.total_merchants,
    kpis.total_approved,
    kpis.total_fully_configured,
    kpis.total_activated,
    kpis.activation_rate_pct,
    kpis.total_gmv_30d,
    kpis.avg_gmv_per_merchant,
    kpis.avg_support_tickets,
    COALESCE(gs.tickets_per_merchant, kpis.avg_support_tickets) AS blended_tickets_per_merchant, -- Use blended if available, else original
    CASE
        WHEN COALESCE(gs.tickets_per_merchant, kpis.avg_support_tickets) > 2 THEN "HIGH FRICTION"
        WHEN COALESCE(gs.tickets_per_merchant, kpis.avg_support_tickets) BETWEEN 1 AND 2 THEN "MEDIUM FRICTION"
        ELSE "LOW FRICTION"
    END AS friction_score_index
FROM
    `driiiportfolio.tiktok_shop_analytics.vw_executive_summary_kpis` AS kpis
LEFT JOIN
    `driiiportfolio.tiktok_shop_analytics.google_sheets_summary` AS gs
ON
    kpis.region = gs.region AND kpis.category = gs.category;
