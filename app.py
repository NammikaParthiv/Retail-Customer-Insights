from pathlib import Path
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Retail Customer Insights", page_icon="🛍️", layout="wide")
BASE = Path(__file__).parent

st.title("Retail Customer Insights")
st.caption("Explore the RFM segments and historical purchasing patterns in the supplied retail dataset.")

@st.cache_data
def load_data():
    customers = pd.read_csv(BASE / "rfm_customers.csv")
    summary = pd.read_csv(BASE / "rfm_segments.csv")
    cohorts = pd.read_csv(BASE / "rfm_cohorts.csv", index_col=0)
    return customers, summary, cohorts

try:
    customers, summary, cohorts = load_data()
except FileNotFoundError as exc:
    st.error(f"Required export not found: {exc.filename}. Run all cells in rfm_analysis.ipynb first.")
    st.stop()

if "Segment" not in customers.columns or "Segment" not in summary.columns:
    st.error("The exports do not match the expected schema. Re-run the notebook to regenerate them.")
    st.stop()

segments = sorted(customers["Segment"].dropna().unique())
selected = st.sidebar.multiselect("Segments", segments, default=segments)
min_recency, max_recency = int(customers.Recency.min()), int(customers.Recency.max())
recency = st.sidebar.slider("Recency (days)", min_recency, max_recency, (min_recency, max_recency))
filtered = customers[
    customers.Segment.isin(selected)
    & customers.Recency.between(recency[0], recency[1])
]

k1, k2, k3, k4 = st.columns(4)
k1.metric("Customers in view", f"{len(filtered):,}")
k2.metric("Share of all customers", f"{len(filtered) / len(customers):.1%}" if len(customers) else "0%")
k3.metric("Historic gross sales", f"£{filtered.Monetary.sum():,.0f}")
k4.metric("Average invoices", f"{filtered.Frequency.mean():.2f}" if len(filtered) else "—")

left, right = st.columns(2)
with left:
    st.subheader("Segment size")
    view = summary[summary.Segment.isin(selected)].sort_values("Customers", ascending=False)
    st.bar_chart(view.set_index("Segment")[["Customers"]])
with right:
    st.subheader("Share of historic sales")
    st.bar_chart(view.set_index("Segment")[["HistoricSalesSharePct"]])

st.subheader("Segment profile")
columns = [c for c in ["Segment", "Customers", "CustomerSharePct", "AvgRecencyDays", "AvgInvoices", "AvgHistoricSales", "HistoricSales", "HistoricSalesSharePct"] if c in view.columns]
st.dataframe(view[columns].style.format({
    "CustomerSharePct": "{:.1f}%", "HistoricSalesSharePct": "{:.1f}%",
    "AvgRecencyDays": "{:.1f}", "AvgInvoices": "{:.2f}",
    "AvgHistoricSales": "£{:,.2f}", "HistoricSales": "£{:,.2f}"
}), use_container_width=True, hide_index=True)

st.subheader("Customer explorer")
search = st.text_input("Filter CustomerID", placeholder="Type an ID or leave blank")
customer_view = filtered.copy()
if search.strip():
    customer_view = customer_view[customer_view.CustomerID.astype(str).str.contains(search.strip(), case=False, na=False)]
st.dataframe(customer_view.sort_values("Monetary", ascending=False), use_container_width=True, hide_index=True)
st.download_button("Download current customer view", customer_view.to_csv(index=False).encode("utf-8"), "filtered_customer_segments.csv", "text/csv")

st.subheader("Cohort retention")
st.caption("Share of each first-purchase-month cohort active in subsequent calendar months. Descriptive history, not a forecast.")
st.dataframe(cohorts.style.format("{:.0%}").background_gradient(cmap="Blues", vmin=0, vmax=1), use_container_width=True)

st.info("Monetary values are gross positive historical sales. They are not profit, net sales, forecast revenue, or guaranteed recoverable value. Campaign effectiveness requires a randomized holdout or another credible evaluation.")
