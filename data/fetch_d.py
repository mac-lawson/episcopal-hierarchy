import pandas as pd
import wikipedia as wp
import sqlite3




html = wp.page("Ecclesiastical_provinces_and_dioceses_of_the_Episcopal_Church").html().encode("UTF-8")



try: 
    df = pd.read_html(html)[1]  # Try 2nd table first as most pages contain contents table first
except IndexError:
    df = pd.read_html(html)[0]

print(df.to_string())
# Create a connection to the database (or create it if it doesn't exist)
conn = sqlite3.connect('diocese.db')

# Write the DataFrame to a table in the database
df.to_sql('diocese', conn, if_exists='append', index=False)


# Close the connection
conn.close()
