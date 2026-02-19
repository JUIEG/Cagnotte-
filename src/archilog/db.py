# ---------------------------
# ANCIENNE VERSION (sqlite3)
# ---------------------------
# import sqlite3
#
# def get_db():
#     return sqlite3.connect("cagnotte.db")
#
# def init_db():
#     db = get_db()
#     db.execute("""
#     CREATE TABLE IF NOT EXISTS CAGNOTTE (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         nom TEXT UNIQUE
#     )
#     """)
#     db.execute("""
#     CREATE TABLE IF NOT EXISTS DEPENSE (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         cagnotte_id INTEGER,
#         participant TEXT,
#         montant REAL CHECK (montant > 0),
#         date TEXT,
#         FOREIGN KEY(cagnotte_id) REFERENCES CAGNOTTE(id)
#     )
#     """)
#     db.commit()


# ---------------------------
# NOUVELLE VERSION (SQLAlchemy Core)
# ---------------------------

from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    Float,
    ForeignKey
)

engine = create_engine("sqlite:///cagnotte.db", echo=True)
metadata = MetaData()

cagnotte_table = Table(
    "CAGNOTTE",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("nom", String, unique=True)
)

depense_table = Table(
    "DEPENSE",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("cagnotte_id", Integer, ForeignKey("CAGNOTTE.id")),
    Column("participant", String),
    Column("montant", Float),
    Column("date", String)
)

def init_db():
    metadata.create_all(engine)
