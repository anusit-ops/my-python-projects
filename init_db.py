import sqlite3

phone = "phonebook.db"

conn = sqlite3.connect(phone)
cursor = conn.cursor()

sql_command = """
CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT NOT NULL
    )
"""

cursor.execute(sql_command)

print("สร้างตารางเรียบน้อยแล้ว!")

conn.commit()
conn.close()




