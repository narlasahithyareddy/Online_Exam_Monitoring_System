import sqlite3
import os

os.makedirs('results', exist_ok=True)
conn = sqlite3.connect('database/exam.db')
cur = conn.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables = [row[0] for row in cur.fetchall()]
with open('results/exam_db_export.txt', 'w', encoding='utf-8') as f:
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
print('Export complete: results/exam_db_export.txt')
