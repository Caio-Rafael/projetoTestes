import sqlite3
from flask import g, current_app

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(current_app.config['DATABASE'])
    return g.db

def init_db(app):
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS carros (
            id INTEGER PRIMARY KEY,
            marca TEXT,
            modelo TEXT,
            ano INTEGER
        )
        ''')
        db.commit()

def add_initial_data(app):
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('INSERT INTO carros (marca, modelo, ano) VALUES (?, ?, ?)', ('Toyota', 'Corolla', 2020))
        cursor.execute('INSERT INTO carros (marca, modelo, ano) VALUES (?, ?, ?)', ('Honda', 'Civic', 2019))
        cursor.execute('INSERT INTO carros (marca, modelo, ano) VALUES (?, ?, ?)', ('Ford', 'Fiesta', 2022))
        cursor.execute('INSERT INTO carros (marca, modelo, ano) VALUES (?, ?, ?)', ('Ford', 'Focus', 2023))
        db.commit()

def close_connection(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()
