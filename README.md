# Archilog

Une application Python pour gérer des cagnottes et partager les dépenses entre participants.  
Projet éducatif pour mettre en œuvre une **architecture n-tier** avec interface CLI et web.

---

## Installation & lancement

Installer les dépendances et lancer le projet :

```bash
$ uv sync           # installer les dépendances du projet
$ uv run archilog   # lancer l'application CLI
Usage: archilog [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  display


Course & examples : [https://kathode.neocities.org](https://kathode.neocities.org)

$ env PYTHONPATH="src"
$ python -m flask --app archilog.views --debug run
# puis ouvrir l'url donné http://127.0.0.1:5000
# utiliser le localhost dans l'url http://localhost:5000/
