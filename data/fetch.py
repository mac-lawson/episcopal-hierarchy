import pandas as pd
import wikipedia as wp
import sqlite3




html = wp.page("List_of_bishops_of_the_Episcopal_Church_in_the_United_States_of_America").html().encode("UTF-8")


for i in range (12): 
    try: 
        df = pd.read_html(html)[i]  # Try 2nd table first as most pages contain contents table first
    except IndexError:
        df = pd.read_html(html)[i-1]


    # Create a connection to the database (or create it if it doesn't exist)
    conn = sqlite3.connect('mydatabase.db')

    # Write the DataFrame to a table in the database
    df.to_sql('bishops', conn, if_exists='append', index=False)

    # Close the connection
    conn.close()
