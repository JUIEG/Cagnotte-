from .db import init_db


"""
import click
import sqlite3
from datetime import date

# Base de données

# db_conn = None
# def get_db():
#     return sqlite3.connect("cagnotte.db")

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

# @click.group()
# def cli():
#     init_db()

# # CAGNOTTE

# @cli.command()
# @click.argument("nom")
# def create(nom):
#     """Créer une cagnotte"""
#     db = get_db()
#     try:
#         db.execute("INSERT INTO CAGNOTTE (nom) VALUES (?)", (nom,))
#         db.commit()
#         click.echo(f" Cagnotte '{nom}' créée")
#     except sqlite3.IntegrityError:
#         click.echo(" Cette cagnotte existe déjà")

# @cli.command()
# @click.argument("nom")
# def delete(nom):
#     """Supprimer une cagnotte"""
#     db = get_db()
#     row = db.execute(
#         "SELECT id FROM CAGNOTTE WHERE nom = ?",
#         (nom,)
#     ).fetchone()
#     if not row:
#         click.echo("Cagnotte introuvable")
#         return
#     if not click.confirm(f"Voulez-vous vraiment supprimer la cagnotte  '{nom}' ?", default=False):
#         click.echo("Cagnotte non suprimée ")
#         return
#     db.execute("DELETE FROM DEPENSE WHERE cagnotte_id = ?", (row[0],))
#     db.execute("DELETE FROM CAGNOTTE WHERE id = ?", (row[0],))
#     db.commit()
#     click.echo(f"La cagnotte '{nom}' est supprimée")

# # DEPENSE

# @cli.command()
# @click.argument("cagnotte")
# @click.option("--nom", prompt="Nom du participant")
# @click.option("--montant", prompt="Montant", type=float)
# @click.option("--date_depense", default=str(date.today()), help="Date de la dépense (YYYY-MM-DD)")
# def ajouter(cagnotte, nom, montant, date_depense):
#     """Ajouter ou remplacer une dépense"""
#     if montant <= 0:
#         click.echo("Le montant doit être positif")
#         return
#     db = get_db()
#     row = db.execute(
#         "SELECT id FROM CAGNOTTE WHERE nom = ?",
#         (cagnotte,)
#     ).fetchone()
#     if not row:
#         click.echo("La cagnotte n'existe pas")
#         return
#     cagnotte_id = row[0]
#     depense_existante = db.execute(
#         "SELECT id FROM DEPENSE WHERE cagnotte_id = ? AND participant = ?",
#         (cagnotte_id, nom)
#     ).fetchone()
#     if depense_existante:
#         db.execute(
#             "UPDATE DEPENSE SET montant = ?, date = ? WHERE id = ?",
#             (montant, date_depense, depense_existante[0])
#         )
#         click.echo("Dépense mise à jour une seule dépense autorisée par personne ")
#     else:
#         db.execute(
#             "INSERT INTO DEPENSE (cagnotte_id, participant, montant, date) VALUES (?, ?, ?, ?)",
#             (cagnotte_id, nom, montant, date_depense)
#         )
#         click.echo("Dépense ajoutée")
#     db.commit()

# @cli.command()
# @click.argument("cagnotte")
# @click.option("--nom", prompt="Nom du participant")
# def supprimer_depense(cagnotte, nom):
#     """Supprimer la dépense d'un participant dans une cagnotte"""
#     db = get_db()
#     row = db.execute("SELECT id FROM CAGNOTTE WHERE nom = ?", (cagnotte,)).fetchone()
#     if not row:
#         click.echo("La cagnotte n'existe pas")
#         return
#     depense = db.execute(
#         "SELECT id, participant, montant, date FROM DEPENSE WHERE cagnotte_id = ? AND participant = ?",
#         (row[0], nom)
#     ).fetchone()
#     if not depense:
#         click.echo("Aucune dépense trouvée pour ce participant")
#         return
#     click.echo(f"Dépense trouvée : ID: {depense[0]} | Participant: {depense[1]} | Montant: {depense[2]} | Date: {depense[3]}")
#     if click.confirm("Supprimer cette dépense ?", default=False):
#         db.execute("DELETE FROM DEPENSE WHERE id = ?", (depense[0],))
#         db.commit()
#         click.echo("Dépense supprimée")
#     else:
#         click.echo("Suppression annulée")

# @cli.command()
# @click.argument("cagnotte")
# def calcul(cagnotte):
#     """Afficher qui doit de l'argent à qui """
#     db = get_db()
#     row = db.execute(
#         "SELECT id FROM CAGNOTTE WHERE nom = ?",
#         (cagnotte,)
#     ).fetchone()
#     if not row:
#         click.echo("Cagnotte pas trouvé ")
#         return
#     depenses = db.execute(
#         "SELECT participant, montant FROM DEPENSE WHERE cagnotte_id = ?",
#         (row[0],)
#     ).fetchall()
#     if not depenses:
#         click.echo("Aucune dépense")
#         return
#     total = sum(m for _, m in depenses)
#     parts = total / len(depenses)
#     click.echo(f"Total : {total:.2f} €")
#     click.echo(f"Part par personne : {parts:.2f} €\n")
#     for participant, montant in depenses:
#         diff = montant - parts
#         if diff > 0:
#             click.echo(f"{participant} doit recevoir {diff:.2f} €")
#         elif diff < 0:
#             click.echo(f"{participant} doit payer {-diff:.2f} €")
#         else:
#             click.echo(f"{participant} est à l'équilibre")

# @cli.command()
# @click.argument("cagnotte")
# def liste(cagnotte):
#     """Lister toutes les dépenses d'une cagnotte"""
#     db = get_db()
#     row = db.execute("SELECT id FROM CAGNOTTE WHERE nom = ?", (cagnotte,)).fetchone()
#     if not row:
#         click.echo("Cagnotte introuvable")
#         return
#     depenses = db.execute(
#         "SELECT participant, montant, date FROM DEPENSE WHERE cagnotte_id = ? ORDER BY date",
#         (row[0],)
#     ).fetchall()
#     if not depenses:
#         click.echo("Aucune dépense pour cette cagnotte")
#         return
#     click.echo(f"Dépenses pour la cagnotte '{cagnotte}':")
#     for participant, montant, date_depense in depenses:
#         click.echo(f"- {participant} : {montant:.2f} € le {date_depense}")

# if __name__ == "__main__":
#     cli()
""
