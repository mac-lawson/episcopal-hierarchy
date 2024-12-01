import sqlite3
import re

# Database configuration
DATABASE = "bishops.db"

# Function to clean consecrators
def clean_consecrators():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Select consecrators with their ID
    cursor.execute("SELECT id, consecrators FROM bishops")
    rows = cursor.fetchall()

    # Regex to match brackets with numbers, e.g., [1]
    bracket_pattern = r"\[\d+\]"

    for row in rows:
        bishop_id, consecrators = row

        if consecrators:
            # Remove brackets with numbers
            cleaned_consecrators = re.sub(bracket_pattern, "", consecrators).strip()

            # Update the database with the cleaned data
            cursor.execute("""
                UPDATE bishops
                SET consecrators = ?
                WHERE id = ?
            """, (cleaned_consecrators, bishop_id))

    # Commit changes and close connection
    conn.commit()
    conn.close()

    print("Cleaned consecrators field in the database.")

# Execute the cleaning function
if __name__ == "__main__":
    clean_consecrators()
