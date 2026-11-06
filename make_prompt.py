import duckdb
from golden_set import GOLDEN

con = duckdb.connect("bank.db", read_only=True)
schema = con.execute("DESCRIBE customers").fetchdf()
cols = "\n".join(f"- {r.column_name} ({r.column_type})" for r in schema.itertuples())
questions = "\n".join(f"Q{q['id']}. {q['question']}" for q in GOLDEN)

prompt = f"""You are a SQL expert. Write DuckDB SQL for the table below.

Table: customers
Columns:
{cols}

Rules:
- Use only the table and columns above.
- Each query must be a single SELECT statement.
- Put double quotes around column names that contain spaces.
- Return only SQL, no explanations.
- Use exactly this format, one block per question:
-- Q1
SELECT ...;
-- Q2
SELECT ...;

Questions:
{questions}
"""

with open("prompt_for_ai.txt", "w", encoding="utf-8") as f:
    f.write(prompt)
print("Saved prompt_for_ai.txt")
