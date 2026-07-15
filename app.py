from flask import Flask, render_template, jsonify
import sqlite3
import requests

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("quotes.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS quotes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        quote TEXT,
        author TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/quote")
def get_quote():

    response = requests.get("https://api.quotable.io/random")
    data = response.json()

    quote = data["content"]
    author = data["author"]

    conn = sqlite3.connect("quotes.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO quotes(quote,author) VALUES(?,?)",
        (quote, author)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "quote": quote,
        "author": author
    })

@app.route("/history")
def history():

    conn = sqlite3.connect("quotes.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT quote,author FROM quotes ORDER BY id DESC"
    )

    data = cursor.fetchall()

    conn.close()

    history=[]

    for row in data:
        history.append({
            "quote":row[0],
            "author":row[1]
        })

    return jsonify(history)

if __name__=="__main__":
    app.run(debug=True)