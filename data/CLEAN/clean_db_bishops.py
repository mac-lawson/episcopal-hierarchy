import sqlite3
import re

# Connect to the SQLite database
conn = sqlite3.connect('../../bishops.db')
cursor = conn.cursor()

# Update query to remove content surrounded by brackets in all three columns
cursor.execute("""
    UPDATE bishops
    SET diocese = REPLACE(diocese, substr(diocese, instr(diocese, '['), instr(diocese, ']') - instr(diocese, '[') + 1), ''),
        consecrators = REPLACE(consecrators, substr(consecrators, instr(consecrators, '['), instr(consecrators, ']') - instr(consecrators, '[') + 1), ''),
        notes = REPLACE(notes, substr(notes, instr(notes, '['), instr(notes, ']') - instr(notes, '[') + 1), '')
""")

# Commit the changes and close the connection
conn.commit()
conn.close()
