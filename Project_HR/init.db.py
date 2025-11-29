import sqlite3

hr = "hr_system.db"

conn = sqlite3.connect(hr)
cursor = conn.cursor()

sql_command = """
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fullname TEXT NOT NULL,
    position TEXT NOT NULL
    )
"""
cursor.execute(sql_command)
print("สร้างแล้ว...")

conn.commit()
conn.close