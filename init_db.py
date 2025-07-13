import sqlite3

conn = sqlite3.connect('database.db')
conn.execute('CREATE TABLE IF NOT EXISTS cars (id INTEGER PRIMARY KEY, brand TEXT NOT NULL, model TEXT NOT NULL)')
conn.commit()
conn.close()