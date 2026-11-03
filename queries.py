import duckdb

con = duckdb.connect("bank.db", read_only=True)


def run(title, sql):
    print("\n" + title)
    print(con.execute(sql).fetchdf().to_string(index=False))


run(
    "1. Total customers",
    """
    SELECT COUNT(*) AS total_customers
    FROM customers
    """,
)

run(
    "2. Average balance by country",
    """
    SELECT Geography, ROUND(AVG(Balance), 2) AS avg_balance
    FROM customers
    GROUP BY Geography
    ORDER BY avg_balance DESC
    """,
)

run(
    "3. Top 10 customers by balance",
    """
    SELECT Surname, Geography, Balance
    FROM customers
    ORDER BY Balance DESC
    LIMIT 10
    """,
)

run(
    "4. Churn rate (%) by country",
    """
    SELECT Geography,
           COUNT(*) AS customers,
           ROUND(100.0 * SUM(Exited) / COUNT(*), 2) AS churn_pct
    FROM customers
    GROUP BY Geography
    ORDER BY churn_pct DESC
    """,
)

run(
    "5. Churn rate (%) by age group",
    """
    SELECT CASE WHEN Age < 30 THEN 'under 30'
                WHEN Age < 45 THEN '30-44'
                WHEN Age < 60 THEN '45-59'
                ELSE '60+' END AS age_group,
           COUNT(*) AS customers,
           ROUND(100.0 * SUM(Exited) / COUNT(*), 2) AS churn_pct
    FROM customers
    GROUP BY age_group
    ORDER BY churn_pct DESC
    """,
)

run(
    "6. Average balance: churned vs retained, by country",
    """
    SELECT Geography,
           Exited,
           COUNT(*) AS customers,
           ROUND(AVG(Balance), 2) AS avg_balance
    FROM customers
    GROUP BY Geography, Exited
    ORDER BY Geography, Exited
    """,
)