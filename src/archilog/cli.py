import click
from datetime import date

from archilog.db import init_db
from archilog.domain import (
    create_cagnotte,
    supprimer_cagnotte,
    ajouter_depense,
    supprimer_depense,
    calculer,
    liste,
)
from archilog.domain import supprimer_depense as supprimer_depense_domain
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

from archilog.domain import liste as liste_domain

@cli.command()
@click.argument("cagnotte")
def liste(cagnotte):
    depenses = liste_domain(cagnotte)

    if not depenses:
        click.echo("Cagnotte introuvable ou aucune dépense")
        return

    click.echo(f"Dépenses pour la cagnotte '{cagnotte}':")
    for participant, montant, date_depense in depenses:
        click.echo(f"- {participant} : {montant:.2f} € le {date_depense}")

if __name__ == "__main__":
    cli()
