import os
import duckdb

os.makedirs("summary", exist_ok=True)
con = duckdb.connect("bank.db", read_only=True)

QUERIES = {
    "overview": """
        SELECT COUNT(*) AS customers,
               SUM(Exited) AS churned,
               ROUND(100.0 * SUM(Exited) / COUNT(*), 2) AS churn_pct
        FROM customers
    """,
    "churn_by_country": """
        SELECT Geography,
               COUNT(*) AS customers,
               SUM(Exited) AS churned,
               ROUND(100.0 * SUM(Exited) / COUNT(*), 2) AS churn_pct,
               ROUND(AVG(Balance), 2) AS avg_balance
        FROM customers
        GROUP BY Geography
        ORDER BY churn_pct DESC
    """,
    "churn_by_age_group": """
        SELECT CASE WHEN Age < 30 THEN 'under 30'
                    WHEN Age < 45 THEN '30-44'
                    WHEN Age < 60 THEN '45-59'
                    ELSE '60+' END AS age_group,
               COUNT(*) AS customers,
               ROUND(100.0 * SUM(Exited) / COUNT(*), 2) AS churn_pct
        FROM customers
        GROUP BY age_group
        ORDER BY age_group
    """,
    "churn_by_activity": """
        SELECT IsActiveMember,
               COUNT(*) AS customers,
               ROUND(100.0 * SUM(Exited) / COUNT(*), 2) AS churn_pct
        FROM customers
        GROUP BY IsActiveMember
        ORDER BY IsActiveMember
    """,
    "balance_by_country_exit": """
        SELECT Geography,
               Exited,
               COUNT(*) AS customers,
               ROUND(AVG(Balance), 2) AS avg_balance
        FROM customers
        GROUP BY Geography, Exited
        ORDER BY Geography, Exited
    """,
}

for name, sql in QUERIES.items():
    df = con.execute(sql).fetchdf()
    df.to_csv(f"summary/{name}.csv", index=False)
    print("saved", f"summary/{name}.csv", len(df), "rows")