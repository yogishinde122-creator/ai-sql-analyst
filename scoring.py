"""Shared scoring logic: run AI-written SQL safely and compare with the golden set."""
import re
from numbers import Real

import pandas as pd

from golden_set import GOLDEN
from sql_guard import UnsafeSQL, open_locked_connection, validate_select


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


def parse_answers(text: str) -> dict[int, str]:
    text = text.replace("```sql", "").replace("```", "")
    parts = re.findall(r"--\s*Q(\d+)[^\n]*\n(.*?)(?=--\s*Q\d+|\Z)", text, flags=re.S)
    return {int(n): sql.strip() for n, sql in parts}


def score_answers(text: str, db_path: str = "bank.db", verbose: bool = True):
    """Score AI SQL text against the golden set. Returns (correct, total, per_question)."""
    con = open_locked_connection(db_path)
    answers = parse_answers(text)
    results, correct = {}, 0
    for item in GOLDEN:
        qid = item["id"]
        sql = answers.get(qid)
        if not sql:
            status = "MISSING"
        else:
            try:
                safe_sql = validate_select(sql)
                got = normalize(con.execute(safe_sql).fetchdf())
                expected = normalize(con.execute(item["sql"]).fetchdf())
                status = "CORRECT" if got == expected else "WRONG"
            except UnsafeSQL as e:
                status = f"BLOCKED ({e})"
            except Exception as e:
                status = f"ERROR - {str(e).splitlines()[0]}"
        if status == "CORRECT":
            correct += 1
        results[qid] = status
        if verbose:
            print(f"Q{qid}: {status}")
    total = len(GOLDEN)
    if verbose:
        print(f"\nScore: {correct}/{total} = {100 * correct / total:.0f}%")
    return correct, total, results
