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
from sqlalchemy import UniqueConstraint

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
    Column("date", String),
    UniqueConstraint("cagnotte_id", "participant")
)

def init_db():
    metadata.create_all(engine)
