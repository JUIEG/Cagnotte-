# ---------------------------
# ANCIENNE VERSION (sqlite3)
# ---------------------------
# from db import get_db
#
# def get_cagnotte_id(nom):
#     db = get_db()
#     return db.execute("SELECT id FROM CAGNOTTE WHERE nom = ?", (nom,)).fetchone()
#
# def inserer_cagnotte(nom):
#     db = get_db()
#     db.execute("INSERT INTO CAGNOTTE (nom) VALUES (?)", (nom,))
#     db.commit()
#
# def supprimer_cagnotte(cagnotte_id):
#     db = get_db()
#     db.execute("DELETE FROM DEPENSE WHERE cagnotte_id = ?", (cagnotte_id,))
#     db.execute("DELETE FROM CAGNOTTE WHERE id = ?", (cagnotte_id,))
#     db.commit()
#
# def get_depense(cagnotte_id, participant):
#     db = get_db()
#     return db.execute(
#         "SELECT id, participant, montant, date FROM DEPENSE WHERE cagnotte_id = ? AND participant = ?",
#         (cagnotte_id, participant)
#     ).fetchone()
#
# def insert_depense(cagnotte_id, participant, montant, date_depense):
#     db = get_db()
#     db.execute(
#         "INSERT INTO DEPENSE (cagnotte_id, participant, montant, date) VALUES (?, ?, ?, ?)",
#         (cagnotte_id, participant, montant, date_depense)
#     )
#     db.commit()
#
# def update_depense(depense_id, montant, date_depense):
#     db = get_db()
#     db.execute(
#         "UPDATE DEPENSE SET montant = ?, date = ? WHERE id = ?",
#         (montant, date_depense, depense_id)
#     )
#     db.commit()
#
# def supprimer_depense(depense_id):
#     db = get_db()
#     db.execute("DELETE FROM DEPENSE WHERE id = ?", (depense_id,))
#     db.commit()
#
# def get_depenses(cagnotte_id):
#     db = get_db()
#     return db.execute(
#         "SELECT participant, montant FROM DEPENSE WHERE cagnotte_id = ?",
#         (cagnotte_id,)
#     ).fetchall()
#
# def get_depenses_detail(cagnotte_id):
#     db = get_db()
#     return db.execute(
#         "SELECT participant, montant, date FROM DEPENSE WHERE cagnotte_id = ? ORDER BY date",
#         (cagnotte_id,)
#     ).fetchall()


# ---------------------------
# NOUVELLE VERSION (SQLAlchemy Core)
# ---------------------------

from sqlalchemy import select, insert, update, delete
from archilog.db import engine, cagnotte_table, depense_table
from db import engine, cagnotte_table
from sqlalchemy import select

 # repository.py
def get_cagnotte_id(nom):
    stmt = select(cagnotte_table.c.id).where(
        cagnotte_table.c.nom == nom
    )

    with engine.connect() as conn:
        return conn.execute(stmt).fetchone()


from sqlalchemy import select, insert
from archilog.db import engine, cagnotte_table, depense_table

def get_cagnottes():
    stmt = select(cagnotte_table)
    with engine.begin() as conn:
        result = conn.execute(stmt).fetchall()
        return [{"id": r.id, "nom": r.nom} for r in result]


def inserer_cagnotte(nom):
    stmt = insert(cagnotte_table).values(nom=nom)
    with engine.begin() as conn:
        conn.execute(stmt)



def supprimer_cagnotte(cagnotte_id):
    with engine.begin() as conn:
        conn.execute(
            delete(depense_table).where(
                depense_table.c.cagnotte_id == cagnotte_id
            )
        )
        conn.execute(
            delete(cagnotte_table).where(
                cagnotte_table.c.id == cagnotte_id
            )
        )


def get_depense(cagnotte_id, participant):
    stmt = select(
        depense_table.c.id,
        depense_table.c.participant,
        depense_table.c.montant,
        depense_table.c.date
    ).where(
        depense_table.c.cagnotte_id == cagnotte_id,
        depense_table.c.participant == participant
    )

    with engine.connect() as conn:
        return conn.execute(stmt).fetchone()




def insert_depense(cagnotte_id, participant, montant, date_depense):
    stmt = insert(depense_table).values(
        cagnotte_id=cagnotte_id,
        participant=participant,
        montant=montant,
        date=date_depense
    )

    with engine.begin() as conn:
        conn.execute(stmt)


def update_depense(depense_id, montant, date_depense):
    stmt = update(depense_table).where(
        depense_table.c.id == depense_id
    ).values(
        montant=montant,
        date=date_depense
    )

    with engine.begin() as conn:
        conn.execute(stmt)


def supprimer_depense(depense_id):
    stmt = delete(depense_table).where(
        depense_table.c.id == depense_id
    )

    with engine.begin() as conn:
        conn.execute(stmt)


def get_depenses(cagnotte_id):
    stmt = select(
        depense_table.c.participant,
        depense_table.c.montant
    ).where(
        depense_table.c.cagnotte_id == cagnotte_id
    )

    with engine.connect() as conn:
        return conn.execute(stmt).fetchall()


def get_depenses_detail(cagnotte_id):
    stmt = select(
        depense_table.c.participant,
        depense_table.c.montant,
        depense_table.c.date
    ).where(
        depense_table.c.cagnotte_id == cagnotte_id
    ).order_by(depense_table.c.date)

    with engine.connect() as conn:
        return conn.execute(stmt).fetchall()
