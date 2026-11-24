import pytest

from sql_guard import UnsafeSQL, validate_select


@pytest.mark.parametrize("sql", [
    "SELECT COUNT(*) FROM customers",
    "select * from customers;",
    "WITH t AS (SELECT 1 AS x) SELECT * FROM t",
])
def test_allows_select(sql):
    assert validate_select(sql)


@pytest.mark.parametrize("sql", [
    "DROP TABLE customers",
    "DELETE FROM customers",
    "UPDATE customers SET Exited = 0",
    "SELECT 1; DROP TABLE customers",
    "COPY customers TO 'out.csv'",
    "WITH d AS (DELETE FROM customers RETURNING *) SELECT * FROM d",
    "",
    "not sql at all",
])
def test_blocks_unsafe(sql):
    with pytest.raises(UnsafeSQL):
        validate_select(sql)


def test_keywords_inside_strings_and_quoted_names_are_fine():
    assert validate_select("SELECT 'drop table' AS note, \"Card Type\" FROM customers")
