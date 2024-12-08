import sqlite3
import re

# Connect to the SQLite database
conn = sqlite3.connect('diocese.db')
cursor = conn.cursor()

# Update query to remove content surrounded by brackets in the Diocese column
cursor.execute("""
    UPDATE diocese
    SET Diocese = REPLACE(Diocese, substr(Diocese, instr(Diocese, '['), instr(Diocese, ']') - instr(Diocese, '[') + 1), '')
""")

# Commit the changes and close the connection
conn.commit()
conn.close()
