# Flowwork

Dépôt de test pour Codex 🚀

## Application Flowwork Oncologie

Cette application fournit un moteur de gestion de flux pour suivre le parcours de soins de patients atteints de tumeurs solides.
Elle repose sur un plan de soins prédéfini couvrant les étapes clés d'une prise en charge oncologique :
triage initial, diagnostic, traitement et surveillance.

### Installation

1. Créez un environnement virtuel et installez les dépendances de test (optionnel) :

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install pytest
   ```

2. Aucune autre dépendance n'est requise pour exécuter l'application.

### Utilisation en ligne de commande

Les commandes suivantes sont disponibles via `python -m flowwork_app.cli` :

- `inscrire <identifiant> <nom_complet> <age>` : crée un patient et initialise son parcours.
- `patients` : liste l'ensemble des patients et leur progression.
- `suivi <identifiant>` : affiche un rapport synthétique pour le patient.
- `terminer <identifiant> <tache>` : marque une tâche comme réalisée et fait progresser le patient si nécessaire.

Un exemple d'inscription de patient :

```bash
python -m flowwork_app.cli inscrire P001 "Alice Martin" 54
```

Le stockage utilise un fichier JSON `data/patients.json` par défaut, qui sera créé automatiquement.

### Tests

Exécutez l'ensemble des tests avec :

```bash
pytest
```

