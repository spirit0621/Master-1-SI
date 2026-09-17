# 📐 Normes & Conventions de Code Python TECHCORP (v3.0)

Ce guide définit les standards d'ingénierie logicielle obligatoires pour tous les projets Python au sein de TECHCORP.

## 1. Environnement & Versions
- **Interpréteur :** Python 3.11 ou 3.12 exclusivement.
- **Gestionnaire de dépendances :** Utilisation de virtualenv (`.venv`) obligatoire. Les dépendances de production sont figées dans `requirements.txt` avec numéros de version stricts (ex: `fastapi==0.115.0`).

## 2. Style & Formatage
- **Guide de style :** Respect strict de la PEP 8.
- **Formatteur automatique :** `black --line-length 100` et `isort` pour le tri des imports.
- **Typage (Type Hints) :** Typage systématique des arguments de fonctions et des valeurs de retour (utilisation de `typing` ou annotations natives Python 3.10+ `int | None`, `list[str]`).
- **Validation avec Mypy :** Exécution de `mypy --strict` dans la pipeline CI.

## 3. Architecture d'un projet FastAPI chez TECHCORP
L'arborescence standard d'un micro-service est la suivante :
```text
mon-service/
├── api/
│   ├── routes/         # Endpoints modulaires (APIRouter)
│   ├── dependencies.py # Injections de dépendances (get_db, auth)
│   └── app.py          # Point d'entrée FastAPI
├── models/             # Modèles SQLModel ou SQLAlchemy
├── schemas/            # Schémas Pydantic (In/Out)
├── services/           # Logique métier pure
├── tests/              # Tests unitaires et d'intégration (pytest)
├── Dockerfile          # Image de conteneur optimisée multi-stage
└── requirements.txt
```

## 4. Conventions Git chez TECHCORP
- **Format des messages de commit :** Norme *Conventional Commits* avec référence de ticket obligatoire :
  `feat(auth): [TCK-1020] ajout du support OAuth2 PKCE`
  `fix(api): [TCK-1035] correction de l'erreur 422 sur le payload ticket`
  `docs(readme): mise a jour des variables d'environnement`
- **Stratégie de branches :**
  - `main` : Production uniquement (protégée, déploiement automatisé par tag).
  - `develop` : Intégration continue.
  - `feature/TCK-XXX-description` : Branches de travail individuelles.
