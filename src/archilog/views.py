from flask import Flask, render_template, request, redirect
from datetime import date

from archilog.db import init_db
from archilog.domain import create_cagnotte, ajouter_depense, supprimer_depense, supprimer_cagnotte, calculer
from archilog.repository import (
    get_cagnottes,
    get_cagnotte_id,
    get_depenses_detail,
)
app = Flask(__name__)
init_db()
@app.route("/cagnotte/<nom>")
def voir_cagnotte(nom):
    row = get_cagnotte_id(nom)
    if not row:
        return redirect("/")

    depenses = get_depenses_detail(row[0])
    today = date.today().isoformat()

    return render_template(
        "cagnotte.html",
        cagnotte={"nom": nom},
        depenses=depenses,
        today=today
    )
@app.route("/")
def home():
    cagnottes = get_cagnottes()
    today = date.today().isoformat()
    return render_template("home.html", cagnottes=cagnottes, today=today)

@app.route("/create", methods=["POST"])
def create():
    nom = request.form["nom"]

    msg = create_cagnotte(nom)

    cagnottes = get_cagnottes()
    today = date.today().isoformat()

    return render_template(
        "home.html",
        cagnottes=cagnottes,
        today=today,
        message=msg
    )

@app.route("/ajouter", methods=["POST"])
def ajouter():
    cagnotte_nom = request.form["cagnotte"]
    participant = request.form["nom"]
    montant = float(request.form["montant"])
    date_depense = request.form["date_depense"]

    msg = ajouter_depense(
        cagnotte_nom,
        participant,
        montant,
        date_depense
    )

    row = get_cagnotte_id(cagnotte_nom)

    if not row:
        return redirect("/")

    depenses = get_depenses_detail(row[0])
    today = date.today().isoformat()

    return render_template(
        "cagnotte.html",
        cagnotte={"nom": cagnotte_nom},
        depenses=depenses,
        today=today,
        message=msg
    )
@app.route("/supprimer_depense", methods=["POST"])
def supprimer_depense_view():
    cagnotte = request.form["cagnotte"]
    participant = request.form["nom"]

    supprimer_depense(cagnotte, participant)

    return redirect(f"/cagnotte/{cagnotte}")

@app.route("/supprimer_cagnotte", methods=["POST"])
def supprimer_cagnotte_view():
    cagnotte = request.form["cagnotte"]

    supprimer_cagnotte(cagnotte)

    return redirect("/")

@app.route("/calcul/<nom>")
def calcul_view(nom):
    total, parts, resultat = calculer(nom)

    if resultat is None:
        return redirect("/")

    return render_template(
        "calcul.html",
        cagnotte={"nom": nom},
        total=total,
        parts=parts,
        resultat=resultat
    )