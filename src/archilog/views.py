from flask import Flask, render_template, request, redirect
from db import init_db
from domain import create_cagnotte, ajouter_depense, liste, calculer

app = Flask(__name__)
init_db()

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/create", methods=["POST"])
def create():
    nom = request.form["nom"]
    create_cagnotte(nom)
    return redirect("/")


@app.route("/ajouter", methods=["POST"])
def ajouter():
    cagnotte = request.form["cagnotte"]
    nom = request.form["nom"]
    montant = float(request.form["montant"])
    ajouter_depense(cagnotte, nom, montant, "2026-02-19")
    return redirect("/")
