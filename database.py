import sqlite3
from flask import Flask, g


app = Flask(__name__)

DATABASE = "database.db"

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def create_table():
    with app.app_context():
        cur = get_db().cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS metadata_table( 
            identifier TEXT PRIMARY KEY,
            file_path TEXT);
            ''')