# app/profiler_duckdb.py
import duckdb
import os
from typing import Dict

def profile_csv_duckdb(path: str) -> Dict:
    """
    Profile a CSV using DuckDB for scalable aggregation. Returns a dict with rows and per-column stats.
    """
    con = duckdb.connect(database=':memory:')
    table = 'tmp_csv'
    # Use read_csv_auto which infers types and is efficient for large files
    con.execute(f"CREATE TABLE {table} AS SELECT * FROM read_csv_auto('{path}')")
    rows = con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    cols_info = []
    # Get column names
    res = con.execute(f"PRAGMA table_info('{table}')").fetchall()
    col_names = [r[1] for r in res]
    for c in col_names:
        col_stat = {'name': c}
        # null count
        nc = con.execute(f"SELECT SUM(CASE WHEN {c} IS NULL THEN 1 ELSE 0 END) FROM {table}").fetchone()[0]
        col_stat['null_count'] = int(nc)
        # unique count (could be expensive)
        try:
            uq = con.execute(f"SELECT COUNT(DISTINCT {c}) FROM {table}").fetchone()[0]
            col_stat['unique_count'] = int(uq)
        except Exception:
            col_stat['unique_count'] = None
        # top values
        try:
            tops = con.execute(f"SELECT {c} AS val, COUNT(*) as cnt FROM {table} GROUP BY {c} ORDER BY cnt DESC LIMIT 10").fetchall()
            col_stat['top_values'] = {row[0]: row[1] for row in tops}
        except Exception:
            col_stat['top_values'] = {}
        # numeric stats
        try:
            stats = con.execute(
                f"SELECT MIN({c}), MAX({c}), AVG({c}) FROM {table} WHERE {c} IS NOT NULL"
            ).fetchone()
            if stats and any(s is not None for s in stats):
                col_stat.update({'min': stats[0], 'max': stats[1], 'mean': stats[2]})
        except Exception:
            pass
        cols_info.append(col_stat)
    con.close()
    return {'rows': int(rows), 'columns': cols_info}