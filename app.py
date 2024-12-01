from flask import Flask, render_template, g
import sqlite3

app = Flask(__name__)

# Database configuration
DATABASE = "bishops.db"

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
    return render_template("home.html", bishops=bishops)

@app.route("/bishop/<name>")
def bishop(name):
    """Details page for a specific bishop."""
    db = get_db()
    cursor = db.execute("SELECT * FROM bishops WHERE bishop = ?", (name,))
    bishop_data = cursor.fetchone()
    
    if not bishop_data:
        return f"<h1>Bishop {name} not found.</h1>", 404
    
    return render_template("bishop.html", bishop=bishop_data)

if __name__ == "__main__":
    app.run(debug=True)
