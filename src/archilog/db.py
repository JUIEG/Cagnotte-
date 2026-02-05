import sqlite3


def get_db():
    return sqlite3.connect("cagnotte.db")

def init_db():
    db = get_db()
    db.execute("""
    CREATE TABLE IF NOT EXISTS CAGNOTTE (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT UNIQUE
    )
    """)
    db.execute("""
    CREATE TABLE IF NOT EXISTS DEPENSE (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cagnotte_id INTEGER,
        participant TEXT,
        montant REAL CHECK (montant > 0),
        date TEXT,
        FOREIGN KEY(cagnotte_id) REFERENCES CAGNOTTE(id)
    )
    """)
    db.commit()