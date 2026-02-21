from flask import Flask, render_template, request, redirect, jsonify
import sqlite3
from mylibrary.library import Library

app = Flask(__name__)
library = Library("My Library")  


def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS books (
            title TEXT PRIMARY KEY,
            author TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()


def load_books():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT title, author FROM books")
    rows = c.fetchall()
    library.books = {title: author for title, author in rows}
    conn.close()

load_books()

@app.route("/")
def index():
    load_books()  
    return render_template("index.html", books=library.books)

@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title", "").strip()
    author = request.form.get("author", "").strip()
    if title and author:
        library.add_book(title, author)
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("INSERT OR IGNORE INTO books (title, author) VALUES (?, ?)", (title, author))
        conn.commit()
        conn.close()
    return redirect("/")

@app.route("/remove/<title>")
def remove(title):
    library.remove_book(title)
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("DELETE FROM books WHERE title=?", (title,))
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
