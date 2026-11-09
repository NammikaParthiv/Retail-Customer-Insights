<<<<<<< HEAD
# Retail Customer Insights

This project analyzes retail transactions to understand how recently customers purchased, how often they ordered, and how much they spent. It creates practical customer segments, examines purchase cohorts, and provides an interactive dashboard for exploring results.

## Files needed to run the project

- `online_retail_final.csv` — supplied source transaction data.
- `rfm_analysis.ipynb` — data preparation, RFM analysis, charts, and output generation.
- `app.py` — Streamlit dashboard.
- `requirements.txt` — Python dependencies.

## Generated files

Running the notebook creates four CSV files: `rfm_customers.csv` (one row per customer), `rfm_segments.csv` (segment-level summary), `rfm_cohorts.csv` (monthly cohort activity), and `campaign_ideas.csv` (project-authored test ideas and measures). The first three are derived from the supplied data; the campaign ideas file is a planning table. The dashboard uses the first three files. All four are reproducible and ignored by Git.

## Run

Use Python 3.10 or newer. From this folder:

```bash
python -m pip install -r requirements.txt
jupyter notebook rfm_analysis.ipynb
```

Run all cells from top to bottom, then start the dashboard from this folder:

```bash
streamlit run app.py
```

The dashboard filters by segment and recency, compares customer counts and historical sales, provides a customer search and CSV download, and displays cohort retention.

## Measure definitions

The analysis keeps rows with a customer ID, valid invoice date, positive quantity and unit price, and an invoice number that does not start with `C`. Line sales are quantity multiplied by unit price. Returns, cancellation invoices, and nonpositive lines are excluded rather than netted against purchases.

- **Recency:** days since the latest qualifying purchase, measured from one day after the latest date in the data.
- **Frequency:** distinct qualifying invoice count.
- **Monetary:** sum of positive line sales in GBP. This is gross historical sales, not profit, net revenue, or predicted customer value.
- **Scores:** relative quintile ranks within this dataset; scores and segment sizes may change with the population or period.
- **Cohort retention:** share of customers grouped by first purchase month active in each later calendar month. This describes history and is not a forecast.

## Interpretation and limitations

Segments are a way to organize customers for investigation; they do not prove churn or campaign effectiveness. Campaign ideas are hypotheses. Evaluate them with randomized holdouts when possible, measuring incremental repeat purchases, contribution margin after discounts, and opt-outs. This is a descriptive analysis of one historical dataset. It does not predict churn or lifetime value, calculate product margin, or estimate causal campaign lift. Invoice count is a practical frequency measure and may differ from a retailer’s exact order definition.

## Source data

The transaction file is the supplied Online Retail dataset. This project documents its own data preparation, RFM definitions, segmentation, analysis, dashboard, and campaign hypotheses. Preserve the source dataset’s attribution and usage terms when redistributing it.
=======
# Retail-Customer-Insights
>>>>>>> 9aaa7be64ba9fc3fa93a32edb461ae639a002fa0
