import click
from datetime import date
from db import init_db
from domain import (
    create_cagnotte, supprimer_cagnotte,
    ajouter_depense, supprimer_depense,
    calculer, liste
)
from domain import supprimer_depense as supprimer_depense_domain

@click.group()
def cli():
    init_db()

@cli.command()
@click.argument("nom")
def create(nom):
    click.echo(create_cagnotte(nom))

@cli.command()
@click.argument("nom")
def delete(nom):
    click.echo(supprimer_cagnotte(nom))

@cli.command()
@click.argument("cagnotte")
@click.option("--nom", prompt="Nom du participant")
@click.option("--montant", prompt="Montant", type=float)
@click.option("--date_depense", default=str(date.today()), help="Date de la dépense (YYYY-MM-DD)")
def ajouter(cagnotte, nom, montant, date_depense):
    click.echo(ajouter_depense(cagnotte, nom, montant, date_depense))


@cli.command(name="supprimer_depense")
@click.argument("cagnotte")
@click.option("--nom", prompt="Nom du participant")
def supprimer_depense_cli(cagnotte, nom):
    """Supprimer une dépense d'un participant dans une cagnotte"""
    depense, message = supprimer_depense_domain(cagnotte, nom)
    if depense:
        click.echo(f"Dépense trouvée : ID: {depense[0]} | Participant: {depense[1]} | Montant: {depense[2]} | Date: {depense[3]}")
    click.echo(message)

@cli.command()
@click.argument("cagnotte")
def calcul(cagnotte):
    total, parts, resultat = calculer(cagnotte)
    if resultat is None:
        click.echo(parts)  # message d'erreur
        return
    click.echo(f"Total : {total:.2f} €")
    click.echo(f"Part par personne : {parts:.2f} €\n")
    for ligne in resultat:
        click.echo(ligne)

@cli.command()
@click.argument("cagnotte")

def liste(cagnotte):
    """Lister toutes les dépenses d'une cagnotte"""
    from repository import get_cagnotte_id, get_depenses_detail

    row = get_cagnotte_id(cagnotte)
    if not row:
        click.echo("Cagnotte introuvable")
        return

    depenses = get_depenses_detail(row[0])
    if not depenses:
        click.echo("Aucune dépense pour cette cagnotte")
        return

    click.echo(f"Dépenses pour la cagnotte '{cagnotte}':")
    for participant, montant, date_depense in depenses:
        click.echo(f"- {participant} : {montant:.2f} € le {date_depense}")

if __name__ == "__main__":
    cli()
