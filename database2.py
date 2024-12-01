import sqlite3
from bs4 import BeautifulSoup
import re

# File containing the HTML content
html_file = "data/data.html"  # Replace with your actual file name

# Read the HTML file
with open(html_file, "r", encoding="utf-8") as file:
    html_content = file.read()

# Parse HTML
soup = BeautifulSoup(html_content, "html.parser")
tables = soup.find_all("table", class_="wikitable")

# Connect to SQLite database
conn = sqlite3.connect("bishops.db")
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS bishops (
    id INTEGER PRIMARY KEY,
    number INTEGER,
    bishop TEXT,
    consecrators TEXT,
    year INTEGER,
    diocese TEXT,
    notes TEXT
)
""")

# Function to format consecrators
def extract_consecrators(cell):
    # Extract all <a> text, preserving their original order
    consecrators = [a.get_text(strip=True) for a in cell.find_all("a")]
    # Join them with commas
    return ", ".join(consecrators)

# Extract and insert data
for table in tables:
    rows = table.find_all("tr")[1:]  # Skip header row
    for row in rows:
        cols = row.find_all(["td", "th"])
        data = [col.get_text(strip=True) for col in cols]
        
        # Process the consecrators column (index 2 in your example)
        if len(cols) > 2 and cols[2]:
            data[2] = extract_consecrators(cols[2])
        
        # Ensure only 6 columns are used
        data = data[:6]  # Truncate if more than 6 columns
        data += [None] * (6 - len(data))  # Pad with None if less than 6
        
        # Insert data into SQLite
        cursor.execute("""
        INSERT INTO bishops (number, bishop, consecrators, year, diocese, notes)
        VALUES (?, ?, ?, ?, ?, ?)
        """, data)

# Commit changes and close connection
conn.commit()
conn.close()

print("Data has been successfully imported into bishops.db")