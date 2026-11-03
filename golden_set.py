import duckdb

GOLDEN = [
    {
        "id": 1,
        "question": "How many customers are there in total?",
        "sql": """
            SELECT COUNT(*) AS total_customers
            FROM customers
        """,
    },
    {
        "id": 2,
        "question": "How many customers have exited?",
        "sql": """
            SELECT COUNT(*) AS churned_customers
            FROM customers
            WHERE Exited = 1
        """,
    },
    {
        "id": 3,
        "question": "What is the average credit score?",
        "sql": """
            SELECT ROUND(AVG(CreditScore), 2) AS avg_credit_score
            FROM customers
        """,
    },
    {
        "id": 4,
        "question": "How many customers are there in each country?",
        "sql": """
            SELECT Geography, COUNT(*) AS customers
            FROM customers
            GROUP BY Geography
            ORDER BY Geography
        """,
    },
    {
        "id": 5,
        "question": "Who are the top 5 customers by balance?",
        "sql": """
            SELECT CustomerId, Balance
            FROM customers
            ORDER BY Balance DESC
            LIMIT 5
        """,
    },
    {
        "id": 6,
        "question": "What is the average estimated salary by gender?",
        "sql": """
            SELECT Gender, ROUND(AVG(EstimatedSalary), 2) AS avg_salary
            FROM customers
            GROUP BY Gender
            ORDER BY Gender
        """,
    },
    {
        "id": 7,
        "question": "What is the churn rate (%) for each card type?",
        "sql": """
            SELECT "Card Type",
                   ROUND(100.0 * SUM(Exited) / COUNT(*), 2) AS churn_pct
            FROM customers
            GROUP BY "Card Type"
            ORDER BY "Card Type"
        """,
    },
    {
        "id": 8,
        "question": "What is the churn rate (%) for active vs inactive members?",
        "sql": """
            SELECT IsActiveMember,
                   ROUND(100.0 * SUM(Exited) / COUNT(*), 2) AS churn_pct
            FROM customers
            GROUP BY IsActiveMember
            ORDER BY IsActiveMember
        """,
    },
    {
        "id": 9,
        "question": "How many customers complained, and how many of them exited?",
        "sql": """
            SELECT Complain,
                   COUNT(*) AS customers,
                   SUM(Exited) AS exited
            FROM customers
            GROUP BY Complain
            ORDER BY Complain
        """,
    },
    {
        "id": 10,
        "question": "Among German customers with a balance above the overall average, how many are there and what is their churn rate (%)?",
        "sql": """
            SELECT COUNT(*) AS customers,
                   ROUND(100.0 * SUM(Exited) / COUNT(*), 2) AS churn_pct
            FROM customers
            WHERE Geography = 'Germany'
              AND Balance > (SELECT AVG(Balance) FROM customers)
        """,
    },
]

if __name__ == "__main__":
    con = duckdb.connect("bank.db", read_only=True)
    for item in GOLDEN:
        print(f"\nQ{item['id']}. {item['question']}")
        print(con.execute(item["sql"]).fetchdf().to_string(index=False))