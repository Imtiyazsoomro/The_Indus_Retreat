from fastapi import FastAPI, HTTPException
import sqlite3
import os

app = FastAPI(title="The Indus Retreat Operations API")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "indus_retreat.db")

def query_db(query, args=(), one=False):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute(query, args)
        rv = cursor.fetchall()
        
        # Converts the SQLite rows into clean JSON dictionaries
        if rv:
            columns = [column[0] for column in cursor.description]
            results = [dict(zip(columns, row)) for row in rv]
            return (results[0] if results else None) if one else results
        return None

@app.get("/")
def read_root():
    return {"message": "Welcome to The Indus Retreat API"}

@app.get("/menu")
def get_menu():
    """Returns the full restaurant menu."""
    items = query_db("SELECT * FROM menu")
    if not items:
        return {"menu_items": []}
    return {"menu_items": items}

@app.get("/suites")
def get_suites():
    """Returns all hotel rooms and their availability."""
    suites = query_db("SELECT * FROM suites")
    if not suites:
        return {"suites": []}
    return {"suites": suites}