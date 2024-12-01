import sqlite3
import re

# Connect to SQLite database
conn = sqlite3.connect("bishops.db")
cursor = conn.cursor()

# Function to clean annotations like [N 106]
def clean_annotations(text):
    if text:
        return re.sub(r"\[N \d+\]", "", text).strip()
    return text

# Fetch all rows
cursor.execute("SELECT id, consecrators, notes FROM bishops")
rows = cursor.fetchall()

# Clean and update rows
for row in rows:
    id = row[0]
    consecrators = clean_annotations(row[1])
    notes = clean_annotations(row[2])
    
    # Update the database with cleaned data
    cursor.execute("""
    UPDATE bishops
    SET consecrators = ?, notes = ?
    WHERE id = ?
    """, (consecrators, notes, id))

# Commit changes and close connection
conn.commit()
conn.close()

print("Annotations have been removed from the database.")