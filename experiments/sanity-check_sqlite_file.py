import sqlite3, pathlib

db_path = pathlib.Path("data/memory.sqlite")
with sqlite3.connect(db_path) as db:
    rows = db.execute(
        "SELECT rowid AS id, role, content FROM turns ORDER BY rowid"
    ).fetchall()

for rid, role, content in rows:
    print(f"{rid:3} | {role:<9} | {content}")