import glob
import duckdb

files = glob.glob("data/*.csv")
if not files:
    print("data फोल्डरमध्ये .csv फाइल सापडली नाही")
    raise SystemExit

print("फाइल:", files[0])

con = duckdb.connect("bank.db")
con.execute(
    f"CREATE OR REPLACE TABLE customers AS SELECT * FROM read_csv_auto('{files[0]}')"
)

print("एकूण ओळी:", con.execute("SELECT COUNT(*) FROM customers").fetchone()[0])
print(con.execute("DESCRIBE customers").fetchdf())