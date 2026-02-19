from flask import Flask, render_template, request, redirect
from datetime import date
from archilog.db import init_db
from archilog.domain import create_cagnotte, ajouter_depense,
from archilog.repository import get_cagnottes

app = Flask(__name__)
init_db()

@app.route("/")
def home():
    cagnottes = get_cagnottes()
    today = date.today().isoformat()
    return render_template("home.html", cagnottes=cagnottes, today=today)

@app.route("/create", methods=["POST"])
def create():
    nom = request.form["nom"]
    create_cagnotte(nom)
    return redirect("/")

@app.route("/ajouter", methods=["POST"])
def ajouter():
    cagnotte_nom = request.form["cagnotte"]
    participant = request.form["nom"]
    montant = float(request.form["montant"])
    ajouter_depense(cagnotte_nom, participant, montant, date.today().isoformat())
    return redirect("/")
