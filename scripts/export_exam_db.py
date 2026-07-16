import sqlite3
from pathlib import Path

base_dir = Path(__file__).resolve().parent.parent
results_dir = base_dir / 'results'
results_dir.mkdir(parents=True, exist_ok=True)
conn = sqlite3.connect(str(base_dir / 'database' / 'exam.db'))
cur = conn.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables = [row[0] for row in cur.fetchall()]
export_path = results_dir / 'exam_db_export.txt'
with open(export_path, 'w', encoding='utf-8') as f:
    f.write('Database export for database/exam.db\n')
    f.write('=' * 80 + '\n\n')
    for table in tables:
        f.write(f'Table: {table}\n')
        f.write('-' * 80 + '\n')
        cur.execute(f'PRAGMA table_info({table})')
        cols = [row[1] for row in cur.fetchall()]
        f.write(' | '.join(cols) + '\n')
        f.write('-' * 80 + '\n')
        cur.execute(f'SELECT * FROM {table}')
        rows = cur.fetchall()
        if not rows:
            f.write('(no rows)\n')
        else:
            for row in rows:
                f.write(' | '.join(str(x) if x is not None else 'NULL' for x in row) + '\n')
        f.write('\n')
conn.close()
print(f'Export complete: {export_path}')
