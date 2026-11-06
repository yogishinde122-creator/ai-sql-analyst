import re
from numbers import Real

import duckdb
import pandas as pd
from golden_set import GOLDEN

con = duckdb.connect("bank.db", read_only=True)


def normalize(df):
    rows = []
    for row in df.itertuples(index=False):
        vals = []
        for v in row:
            if pd.isna(v):
                vals.append("NULL")
            elif isinstance(v, Real) and not isinstance(v, bool):
                vals.append(round(float(v), 2))
            else:
                vals.append(str(v))
        rows.append(tuple(vals))
    return sorted(rows, key=lambda r: [str(x) for x in r])


text = open("ai_answers.sql", encoding="utf-8").read()
text = text.replace("```sql", "").replace("```", "")
parts = re.findall(r"--\s*Q(\d+)[^\n]*\n(.*?)(?=--\s*Q\d+|\Z)", text, flags=re.S)
answers = {int(n): sql.strip().rstrip(";").strip() for n, sql in parts}

correct = 0
for item in GOLDEN:
    qid = item["id"]
    sql = answers.get(qid)
    if not sql:
        print(f"Q{qid}: MISSING")
        continue
    if not sql.lower().startswith(("select", "with")):
        print(f"Q{qid}: BLOCKED (only SELECT is allowed)")
        continue
    try:
        got = normalize(con.execute(sql).fetchdf())
    except Exception as e:
        print(f"Q{qid}: ERROR - {str(e).splitlines()[0]}")
        continue
    expected = normalize(con.execute(item["sql"]).fetchdf())
    if got == expected:
        correct += 1
        print(f"Q{qid}: CORRECT")
    else:
        print(f"Q{qid}: WRONG")

total = len(GOLDEN)
print(f"\nScore: {correct}/{total} = {100 * correct / total:.0f}%")
