import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Bank Churn Analysis", layout="wide")

st.title("Bank Customer Churn: SQL Analysis and AI SQL Accuracy Test")
st.caption(
    "Built by Yogesh Shinde with Python, DuckDB and SQL. "
    "Data: public Kaggle bank churn dataset (10,000 customers). "
    "Only summary numbers are shown on this page."
)

overview = pd.read_csv("summary/overview.csv")
by_country = pd.read_csv("summary/churn_by_country.csv")
by_age = pd.read_csv("summary/churn_by_age_group.csv")
by_activity = pd.read_csv("summary/churn_by_activity.csv")
bal = pd.read_csv("summary/balance_by_country_exit.csv")

c1, c2, c3 = st.columns(3)
c1.metric("Customers", f"{int(overview['customers'].iloc[0]):,}")
c2.metric("Left the bank", f"{int(overview['churned'].iloc[0]):,}")
c3.metric("Overall churn", f"{overview['churn_pct'].iloc[0]}%")

st.header("Churn by country")
fig = px.bar(
    by_country, x="Geography", y="churn_pct", text="churn_pct",
    labels={"churn_pct": "Churn rate (%)"},
)
st.plotly_chart(fig)

st.header("Churn by age group")
order = ["under 30", "30-44", "45-59", "60+"]
by_age["age_group"] = pd.Categorical(by_age["age_group"], categories=order, ordered=True)
by_age = by_age.sort_values("age_group")
fig = px.bar(
    by_age, x="age_group", y="churn_pct", text="churn_pct",
    labels={"churn_pct": "Churn rate (%)", "age_group": "Age group"},
)
st.plotly_chart(fig)

st.header("Active vs inactive members")
by_activity["Member"] = by_activity["IsActiveMember"].map({0: "Inactive", 1: "Active"})
fig = px.bar(
    by_activity, x="Member", y="churn_pct", text="churn_pct",
    labels={"churn_pct": "Churn rate (%)"},
)
st.plotly_chart(fig)

st.header("Average balance: customers who left vs stayed")
bal["Status"] = bal["Exited"].map({0: "Stayed", 1: "Left"})
fig = px.bar(
    bal, x="Geography", y="avg_balance", color="Status", barmode="group",
    labels={"avg_balance": "Average balance"},
)
st.plotly_chart(fig)

st.header("What the data shows")
st.markdown(
    """
- Germany has the highest churn rate (32.44%) and the highest average balance.
- In France and Spain, customers who left held about 18-22% higher average balances than those who stayed. In Germany the gap is under 1%, so balance alone does not explain its churn.
- Inactive members churn at 26.87% versus 14.27% for active members.
- 2,034 of the 2,044 customers who complained left the bank. This looks like data leakage (the complaint is probably recorded at or after exit), so it should not be used to predict churn.

These are averages and patterns, not proven causes.
"""
)

st.header("AI SQL accuracy test")
st.write(
    "I wrote 10 business questions with SQL I verified by hand. "
    "An AI assistant, given only the table schema, wrote SQL for the same "
    "questions. A script ran both and compared the result tables."
)

QUESTIONS = [
    (1, "How many customers are there in total?", True),
    (2, "How many customers have exited?", True),
    (3, "What is the average credit score?", True),
    (4, "How many customers are there in each country?", True),
    (5, "Who are the top 5 customers by balance?", False),
    (6, "What is the average estimated salary by gender?", True),
    (7, "What is the churn rate (%) for each card type?", True),
    (8, "What is the churn rate (%) for active vs inactive members?", True),
    (9, "How many customers complained, and how many of them exited?", False),
    (10, "Among German customers with above-average balance, how many are there and what is their churn rate?", True),
]
table = pd.DataFrame(
    [(q, text, "CORRECT" if ok else "WRONG") for q, text, ok in QUESTIONS],
    columns=["Q", "Question", "Result"],
)
correct = int((table["Result"] == "CORRECT").sum())
st.metric("First attempt score", f"{correct}/10 ({correct * 10}%)")
st.dataframe(table, hide_index=True)

st.info(
    "The two misses (Q5, Q9): the AI's numbers were right, but the result "
    "shape differed from my golden query because my questions were ambiguous. "
    "The scoring is strict, so they count as wrong. The AI step was done "
    "manually in a chat window; only the scoring is automated."
)