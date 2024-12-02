from flask import Flask, render_template, g
import sqlite3

app = Flask(__name__)

# Database configuration
DATABASE = "bishops.db"
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

def get_db():
    """Connect to the SQLite database."""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    """Close the database connection."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
def home():
    """Home page: list all bishops."""
    db = get_db()
    cursor = db.execute("SELECT bishop FROM bishops")
    bishops = cursor.fetchall()
    #print(bishops[30]['bishop'])
    return render_template("home.html", bishops=bishops)

@app.route("/bishop/<name>")
def bishop(name):
    """Details page for a specific bishop."""
    db = get_db()
    cursor = db.execute("SELECT * FROM bishops WHERE bishop = ?", (name,))
    bishop_data = cursor.fetchone()
    cursor = db.execute("SELECT bishop FROM bishops")
    all_bishops = cursor.fetchall()
    
    if not bishop_data:
        return f"<h1>Bishop {name} not found.</h1>", 404
    
    return render_template("bishop.html", all_bishops=all_bishops, bishop=bishop_data, bishop_codes=bishop_codes)

if __name__ == "__main__":
    app.run(debug=True)
