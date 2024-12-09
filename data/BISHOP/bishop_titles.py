import sqlite3
import titles

# Connect to the database
with sqlite3.connect('mydatabase.db') as conn:
    cursor = conn.cursor()

    # Select the data you want to iterate over
    cursor.execute('SELECT [No.], Diocese FROM bishops')

    # Iterate over the results and update as needed
    for row in cursor.fetchall():
        no, original_value = row
        if original_value:  # Ensure `original_value` is not None
            # Split the original value, process it, and join it back into a string
            transformed_value = ",".join(titles.transform_titles(original_value.split(",")))
            # Update the row in the database
            cursor.execute(
                'UPDATE bishops SET Diocese = ? WHERE [No.] = ?',
                (transformed_value, no)
            )

    # Commit the changes (automatic with `with`)

