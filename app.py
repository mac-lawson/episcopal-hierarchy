from flask import Flask, render_template, request, g
import sqlite3
from bs4 import BeautifulSoup
from markupsafe import Markup
from requests import get

import wikidata

import wptools



app = Flask(__name__)

# CONSTANTS

# Database configuration
DATABASE_BISHOPS = "bishops.db"
DATABASE_DIOCESE = "diocese.db"

# Current Presiding Bishop
current_pb = "Sean W. Rowe"

# Mapping of bishop codes to actual bishop names

bishop_codes = {
    "BAK": "Gilbert Baker, Bishop of Hong Kong and Macao",
    "BAN": "Chiu Ban It, Bishop of Singapore",
    "BOY": "Laish Boyd, Bishop of the Bahamas, Turks and Caicos",
    "BRT": "Tony Burton, Bishop of Saskatchewan",
    "CAB": "Daniel Pina Cabral, Bishop of Lebombo",
    "CAS": "William Cassels, Bishop of Western China",
    "CAR": "George Carey, Archbishop of Canterbury",
    "COR": "Nigel Cornwall, Bishop of Borneo",
    "DAL": "John Daly, Bishop in Korea",
    "DAR": "Frederick Darwent, Bishop of Aberdeen and Orkney",
    "ELA": "Riah El-Assal, Bishop of Jerusalem",
    "FYF": "Rollestone Fyffe, Bishop of Rangoon",
    "GOM": "Ricardo Gomez Osnaya, Bishop of Western Mexico",
    "HAL": "Ronald Hall, Bishop of Victoria, Hong Kong (1932–1951) & Bishop of Hong Kong and Macao (1951–1966)",
    "HIL": "Fred Hiltz, Primate of the Anglican Church of Canada (2007-2019)",
    "HIN": "John Hinchliffe, Bishop of Peterborough (1769–1794)",
    "HOL": "John Holder, Archbishop of the West Indies (2009-2018)",
    "ISO": "Andrew Haruhisa Iso, Bishop of Osaka",
    "KER": "Greg Kerr-Wilson, Archbishop of Calgary and Metropolitan of Rupert's Land",
    "KIL": "Robert Kilgour, Primus and Bishop of Aberdeen",
    "LEA": "Arthur Lea, Bishop of Kyushu",
    "LYO": "Frank Lyons, Bishop of Bolivia",
    "MAR": "William Markham, Archbishop of York",
    "MAT": "Carlos Matsinhe, Bishop of Lebombo",
    "MIL": "Harold Miller, Bishop of Down and Dromore",
    "MMS": "Melissa M. Skelton, IX Bishop of New Westminster",
    "MOL": "Herbert Molony, Bishop of Chekiang",
    "MOO": "John Moore, Archbishop of Canterbury",
    "MOS": "Charles Moss, Bishop of Bath and Wells",
    "MOU": "George Moule, Bishop of Mid-China",
    "NOR": "Frank Norris, Bishop of North China",
    "PET": "Arthur Petrie, Bishop of Moray and Ross",
    "POR": "Beilby Porteus, Bishop of London",
    "ROB": "Basil Roberts, Bishop of Singapore",
    "ROW": "Francis Rowinski, Polish National Catholic bishop",
    "SCO": "Charles Scott, Bishop of North China",
    "SHE": "Victor George Shearburn, Bishop of Rangoon",
    "SHO": "David Shoji Tani, Bishop of Okinawa",
    "SKI": "John Skinner, bishop coadjutor of Aberdeen",
    "STE": "Krister Stendahl, Bishop of Stockholm",
    "THO": "John Thomas, Bishop of Rochester",
    "TSE": "Lindel Tsen, Bishop of Honan",
    "UEM": "Nathaniel Makoto Uematsu, Primate of The Nippon Sei Ko Kai and Bishop of Hokkaido",
    "VER": "Joris Vercammen, Archbishop of Utrecht",
    "VIC": "Victoria Matthews, Bishop of Christchurch, retired",
    "WIL": "Cornelius Wilson, Bishop of Costa Rica",
    "ZIE": "Thaddeus F. Zielinski, Polish National Catholic bishop"
}


@app.route('/events')
def events():
    """Fetch and display lectionary information from lectionarypage.net."""
    url = "https://lectionarypage.net/"
    response = get(url)
    response.raise_for_status()  # Ensure we got a successful response
    
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract lectionary sections (adjust selectors based on the site structure)
    events = []
    for item in soup.select(".mainContent a"):  # Replace `.mainContent a` with the correct class or tag
        text = item.get_text(strip=True)
        link = item["href"]

        events.append({"text": text, "link": link})

    return render_template("events.html", events=events)


def get_db_b():
    """Connect to the SQLite database."""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE_BISHOPS)
    db.row_factory = sqlite3.Row
    return db

def get_db_d():
    with sqlite3.connect(DATABASE_DIOCESE) as db:
        db.row_factory = sqlite3.Row
        return db

@app.teardown_appcontext
def close_connection(exception):
    """Close the database connection."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
def new_home():
    """Homepage with two columns but no bishops/diocese data."""
    return render_template("home.html")



@app.route('/bishops/<op>')
def bishops(op):
    """Route to display bishops only."""
    db = get_db_b()

    match op:
        case "all":
            cursor = db.execute("SELECT * FROM bishops")
        case "az":
            cursor = db.execute("SELECT * FROM bishops ORDER BY Bishop;")
        case "za":
            cursor = db.execute("SELECT * FROM bishops ORDER BY Bishop DESC;")
        case "daz":
            cursor = db.execute("SELECT * FROM bishops ORDER BY Diocese;")
        case "dza":
            cursor = db.execute("SELECT * FROM bishops ORDER BY Diocese DESC;")
        case "yrlh":
            cursor = db.execute("SELECT * FROM bishops ORDER BY Year;")
        case "yrhl":
            cursor = db.execute("SELECT * FROM bishops ORDER BY Year DESC;")
    bishops = cursor.fetchall()
    return render_template("bishops.html", bishops=bishops)


@app.route('/dioceses')
def dioceses():
    """Route to display dioceses only."""
    db_1 = get_db_d()
    cursor = db_1.execute("SELECT Diocese FROM diocese")
    diocese = cursor.fetchall()
    return render_template("dioceses.html", diocese=diocese)


@app.route("/bishop/<name>")
def bishop(name):
    """Details page for a specific bishop."""
    db = get_db_b()


    
    # Fetch all bishops for navigation or reference
    cursor = db.execute("SELECT Bishop FROM bishops")
    all_bishops = [row["Bishop"] for row in cursor.fetchall()]  # Extract Bishop names into a list

    # Find the index of the requested bishop
    try:
        bishop_index = all_bishops.index(name)
    except ValueError:
        return f"<h1>{name} not found in the prelate database.</h1><br><p>Email mlawson07@tutanota.com</p>", 404

    # Fetch details of the specific bishop
    cursor = db.execute("SELECT * FROM bishops WHERE Bishop = ?", (name,))
    bishop_data = cursor.fetchone()
    cursor = db.execute("SELECT * FROM bishops")
    bishops = cursor.fetchall() 
    return render_template(
        "bishop.html",
        all_bishops=bishops,
        bishop=bishop_data,
        bishop_index=bishop_index+1,
        bishop_codes=bishop_codes,
        ordination_date=Markup(wikidata.holy_orders(name))
    )

@app.route("/diocese/<diocese>")
def diocese(diocese):
     """Details page for a diocese."""
     print("diocese")  # Debug print

     # Fetch diocese details
     db = get_db_d()
     cursor = db.execute("SELECT * FROM diocese WHERE Diocese = ?", (diocese,))
     diocese_data = cursor.fetchone()

     # Fetch connected bishops (assuming a 'Diocese' column in the bishops table)
     db1 = get_db_b()
     cursor1 = db1.execute(
      "SELECT * FROM bishops WHERE Diocese LIKE ?",
      (f"%{diocese.replace('Diocese of ', '')}%",)
     )
     connected_bishops = cursor1.fetchall()

     if not diocese_data:
         return (
             f"<h1>{diocese} not found in the diocese database.</h1><br><p>Email mlawson07@tutanota.com</p>",
             404,
         )

     return render_template(
         "diocese.html", diocese_data=diocese_data, connected_bishops=connected_bishops
     )

@app.route("/pb")
def presiding_bishop():
    """Presiding Bishop Page"""
    db = get_db_b()
    # Fetch details of the specific bishop
    cursor = db.execute("SELECT * FROM bishops WHERE Notes IS NOT NULL AND Notes != '';")
    bishop_data = cursor.fetchall()

    return render_template(
        "pb.html",
        all_bishops=bishop_data,

    )



if __name__ == "__main__":
    app.run(debug=True)
