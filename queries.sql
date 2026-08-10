-- Segment customers by engagement level based on interaction count and recency
WITH customer_activity AS (
    SELECT
        customer_id,
        COUNT(*) AS interaction_count,
        MAX(interaction_date) AS last_interaction,
        CURRENT_DATE - MAX(interaction_date) AS days_since_last
    FROM campaign_interactions
    GROUP BY customer_id
)
SELECT
    customer_id,
    interaction_count,
    days_since_last,
    CASE
        WHEN days_since_last <= 7 AND interaction_count >= 5 THEN 'highly_engaged'
        WHEN days_since_last <= 30 THEN 'active'
        WHEN days_since_last <= 90 THEN 'at_risk'
        ELSE 'dormant'
    END AS engagement_segment
FROM customer_activity;

-- Roll up performance by campaign: CTR, CPC, conversion rate, and total cost
SELECT
    campaign_id,
    channel,
    SUM(impressions) AS total_impressions,
    SUM(clicks) AS total_clicks,
    SUM(conversion) AS total_conversions,
    SUM(cost) AS total_cost,
    ROUND(SUM(clicks)::numeric / NULLIF(SUM(impressions), 0), 4) AS ctr,
    ROUND(SUM(cost)::numeric / NULLIF(SUM(clicks), 0), 2) AS cpc,
    ROUND(SUM(conversion)::numeric / NULLIF(SUM(clicks), 0), 4) AS conversion_rate,
    ROUND(SUM(cost)::numeric / NULLIF(SUM(conversion), 0), 2) AS cost_per_conversion
FROM campaign_interactions
GROUP BY campaign_id, channel
ORDER BY cost_per_conversion ASC;

-- Compare engagement segment response rates by campaign, to see which
-- segments respond best to which campaigns
WITH segmented AS (
    SELECT
        ci.customer_id,
        ci.campaign_id,
        ci.conversion,
        CASE
            WHEN ca.days_since_last <= 7 AND ca.interaction_count >= 5 THEN 'highly_engaged'
            WHEN ca.days_since_last <= 30 THEN 'active'
            WHEN ca.days_since_last <= 90 THEN 'at_risk'
            ELSE 'dormant'
        END AS engagement_segment
    FROM campaign_interactions ci
    JOIN (
        SELECT
            customer_id,
            COUNT(*) AS interaction_count,
            CURRENT_DATE - MAX(interaction_date) AS days_since_last
        FROM campaign_interactions
        GROUP BY customer_id
    ) ca ON ci.customer_id = ca.customer_id
)
SELECT
    campaign_id,
    engagement_segment,
    COUNT(*) AS total_interactions,
    SUM(conversion) AS total_conversions,
    ROUND(SUM(conversion)::numeric / COUNT(*), 4) AS segment_conversion_rate
FROM segmented
GROUP BY campaign_id, engagement_segment
ORDER BY campaign_id, segment_conversion_rate DESC;
