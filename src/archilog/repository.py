from db import get_db

def get_cagnotte_id(nom):
    db = get_db()
    return db.execute("SELECT id FROM CAGNOTTE WHERE nom = ?", (nom,)).fetchone()

def inserer_cagnotte(nom):
    db = get_db()
    db.execute("INSERT INTO CAGNOTTE (nom) VALUES (?)", (nom,))
    db.commit()

def supprimer_cagnotte(cagnotte_id):
    db = get_db()
    db.execute("DELETE FROM DEPENSE WHERE cagnotte_id = ?", (cagnotte_id,))
    db.execute("DELETE FROM CAGNOTTE WHERE id = ?", (cagnotte_id,))
    db.commit()

def get_depense(cagnotte_id, participant):
    db = get_db()
    return db.execute(
        "SELECT id, participant, montant, date FROM DEPENSE WHERE cagnotte_id = ? AND participant = ?",
        (cagnotte_id, participant)
    ).fetchone()

def insert_depense(cagnotte_id, participant, montant, date_depense):
    db = get_db()
    db.execute(
        "INSERT INTO DEPENSE (cagnotte_id, participant, montant, date) VALUES (?, ?, ?, ?)",
        (cagnotte_id, participant, montant, date_depense)
    )
    db.commit()

def update_depense(depense_id, montant, date_depense):
    db = get_db()
    db.execute(
        "UPDATE DEPENSE SET montant = ?, date = ? WHERE id = ?",
        (montant, date_depense, depense_id)
    )
    db.commit()

def supprimer_depense(depense_id):
    db = get_db()
    db.execute("DELETE FROM DEPENSE WHERE id = ?", (depense_id,))
    db.commit()

def get_depenses(cagnotte_id):
    db = get_db()
    return db.execute(
        "SELECT participant, montant FROM DEPENSE WHERE cagnotte_id = ?",
        (cagnotte_id,)
    ).fetchall()

def get_depenses_detail(cagnotte_id):
    db = get_db()
    return db.execute(
        "SELECT participant, montant, date FROM DEPENSE WHERE cagnotte_id = ? ORDER BY date",
        (cagnotte_id,)
    ).fetchall()
