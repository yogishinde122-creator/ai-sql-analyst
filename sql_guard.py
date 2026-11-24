"""Safety checks for AI-written SQL before it is executed."""
import re

import duckdb

_FORBIDDEN = re.compile(
    r"\b(insert|update|delete|drop|alter|create|copy|attach|detach|install|load|pragma|call|export|import|set)\b",
    re.IGNORECASE,
)


class UnsafeSQL(ValueError):
    """Raised when a query is not a single, plain SELECT statement."""


def validate_select(sql: str) -> str:
    """Return the cleaned SQL if it is exactly one SELECT statement, else raise UnsafeSQL."""
    cleaned = sql.strip().rstrip(";").strip()
    if not cleaned:
        raise UnsafeSQL("empty query")
    try:
        statements = duckdb.extract_statements(cleaned)
    except duckdb.Error as e:
        raise UnsafeSQL(f"could not parse: {str(e).splitlines()[0]}") from e
    if len(statements) != 1:
        raise UnsafeSQL("only one statement is allowed")
    if statements[0].type != duckdb.StatementType.SELECT:
        raise UnsafeSQL(f"only SELECT is allowed, got {statements[0].type.name}")
    # Extra layer: DuckDB reports "SELECT" for a DELETE hidden inside a CTE, so also scan
    # for write/admin keywords (string literals and quoted names are ignored).
    unquoted = re.sub(r"'[^']*'|\"[^\"]*\"", "", cleaned)
    found = _FORBIDDEN.search(unquoted)
    if found:
        raise UnsafeSQL(f"forbidden keyword: {found.group(1).upper()}")
    return cleaned


def open_locked_connection(path: str = "bank.db") -> duckdb.DuckDBPyConnection:
    """Open the database read-only and block file/network access from SQL."""
    con = duckdb.connect(path, read_only=True)
    con.execute("SET enable_external_access = false")
    con.execute("SET lock_configuration = true")
    return con
