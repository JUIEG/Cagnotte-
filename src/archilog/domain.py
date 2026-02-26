#domain.py
from archilog.repository import (
    get_cagnotte_id,
    inserer_cagnotte,
    supprimer_cagnotte as supprimer_cagnotte_repo,
    get_depense,
    insert_depense,
    update_depense,
    supprimer_depense as supprimer_depense_repo,
    get_depenses,
    get_depenses_detail,
)


from archilog.repository import get_cagnotte_id, inserer_cagnotte

def create_cagnotte(nom):
    if get_cagnotte_id(nom):
        return "Cette cagnotte existe déjà"
    inserer_cagnotte(nom)
    return f"Cagnotte '{nom}' créée"


def supprimer_cagnotte(nom):
    cagnotte = get_cagnotte_id(nom)
    if not cagnotte:
        return "Cagnotte introuvable"

    supprimer_cagnotte_repo(cagnotte[0])
    return f"La cagnotte '{nom}' est supprimée"



def ajouter_depense(cagnotte_nom, participant, montant, date_depense):
    if montant <= 0:
        return "Le montant doit être positif"

    cagnotte = get_cagnotte_id(cagnotte_nom)
    if not cagnotte:
        return "La cagnotte n'existe pas"

    cagnotte_id = cagnotte[0]
    depense_existante = get_depense(cagnotte_id, participant)

    if depense_existante:
        update_depense(depense_existante[0], montant, date_depense)
        return "Dépense mise à jour une seule dépense autorisée par personne"
    else:
        insert_depense(cagnotte_id, participant, montant, date_depense)
        return "Dépense ajoutée"

def supprimer_depense(cagnotte_nom, participant):
    cagnotte = get_cagnotte_id(cagnotte_nom)
    if not cagnotte:
        return None, "La cagnotte n'existe pas"

    depense = get_depense(cagnotte[0], participant)
    if not depense:
        return None, "Aucune dépense trouvée"

    supprimer_depense_repo(depense[0])
    return depense, "Dépense supprimée"



def calculer(cagnotte_nom):
    cagnotte = get_cagnotte_id(cagnotte_nom)
    if not cagnotte:
        return None, "Cagnotte pas trouvé"

    depenses = get_depenses(cagnotte[0])
    if not depenses:
        return None, "Aucune dépense"

    total = sum(m for _, m in depenses)
    parts = total / len(depenses)
    resultat = []

    for participant, montant in depenses:
        diff = montant - parts
        if diff > 0:
            resultat.append(f"{participant} doit recevoir {diff:.2f} €")
        elif diff < 0:
            resultat.append(f"{participant} doit payer {-diff:.2f} €")
        else:
            resultat.append(f"{participant} est à l'équilibre")

    return total, parts, resultat

def liste(cagnotte_nom):
    cagnotte = get_cagnotte_id(cagnotte_nom)
    if not cagnotte:
        return None
    return get_depenses_detail(cagnotte[0])
