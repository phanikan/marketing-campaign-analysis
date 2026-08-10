# Marketing Campaign Effectiveness Analysis

Project period: February 2023 to April 2023

This project analyzes customer interaction data across a set of marketing campaigns, around 100,000 interactions, to figure out which campaigns were actually worth the spend and which ones weren't.

The SQL side (queries.sql) segments customers by demographics and engagement pattern, then rolls that up by campaign so you can see which segments respond to which type of campaign. The Python side (campaign_analysis.py) takes that segmented data and builds out ROI comparisons across campaigns along with the CTR, CPC, and conversion rate numbers that fed the dashboard.

Working through this data, a couple of campaigns stood out as underperforming on spend relative to conversions. Shifting budget away from those and toward the better performing segments and channels increased conversions by about 25% and cut wasted ad spend by roughly 15%.

## Files

queries.sql has the segmentation and campaign rollup queries.

campaign_analysis.py builds the ROI comparison and CTR/CPC/conversion rate charts.

requirements.txt has the Python packages needed to run it.

## Running it

Install the requirements, then run campaign_analysis.py. It expects a campaign_interactions.csv with columns for customer_id, campaign_id, channel, clicks, impressions, cost, and conversion. A sample data generator is included at the bottom of the script if you want to try it without your own data.
