# Travaux Pratiques — Programmation Python (Master 1 SI)

Ce dossier rassemble l'ensemble des ateliers, scripts, modules et expérimentations pratiques réalisés dans le cadre des cours de Python en Master 1 SI.

---

## 📑 Sommaire

1. [Cartographie des Ateliers](#1-cartographie-des-ateliers)
2. [Ateliers Réalisés & Notions Clés](#2-ateliers-réalisés--notions-clés)
   * [Atelier 1 : Fondations & Boucles Interactives](#atelier-1--fondations--boucles-interactives)
   * [Atelier 2 : Programmation Orientée Objet (POO) & Héritage](#atelier-2--programmation-orientée-objet-poo--héritage)
   * [Atelier 3 : Validation IPv4 Monobloc (TP0 V1)](#atelier-3--validation-ipv4-monobloc-tp0-v1)
   * [Atelier 4 : Architecture Modulaire & SoC (TP0 V2 & TP1)](#atelier-4--architecture-modulaire--soc-tp0-v2--tp1)
3. [Synthèse Architecturale : Script, Module & Package](#3-synthèse-architecturale--script-module--package)
4. [Guide d'Exécution & Tests](#4-guide-dexécution--tests)

---

## 1. Cartographie des Ateliers

```text
Matière/Matiere Python/TP/
├── README.md               # Ce document récapitulatif
├── main.py                 # Atelier POO : classes Soldier & Archer, héritage
├── Exo1.py                 # Prototype de validation IP (version initiale)
├── TP0/
│   ├── Exo1.py             # Script direct de validation d'adresses IPv4
│   └── TP0 V2/
│       ├── README.md       # Documentation technique détaillée du TP0 V2
│       ├── reseau.py       # Module métier : fonction valider_ip(ip)
│       └── main.py         # Script client : interaction console I/O
└── TP1/
    ├── reseau.py           # Module réutilisable
    └── main.py             # Script lanceur
```

---

## 2. Ateliers Réalisés & Notions Clés

### Atelier 1 : Fondations & Boucles Interactives
* **Fichiers :** Exercices historiques, [main.py](./main.py)
* **Notions :**
  * Indentation obligatoire (4 espaces, PEP 8).
  * Portée des variables (*scope* local d'une fonction vs *scope* global).
  * Boucle infinie contrôlée (`while True`) avec saisie interactive `input()` et interruption propre via signal système (`Ctrl + C` / `KeyboardInterrupt`).

---

### Atelier 2 : Programmation Orientée Objet (POO) & Héritage
* **Fichier :** [main.py](./main.py)
* **Architecture des Classes :**
  * Classe mère `Soldier` : constructeur `__init__`, attributs d'état (`speed`, `health`, `armor`), méthodes de comportement (`attack`, `move`, `get_speed`).
  * Classe fille `Archer(Soldier)` : héritage direct, surcharge du constructeur avec appel au parent via **`super().__init__(speed, health, armor)`**, attribut spécialisé `arrows`, méthode métier `reload`.
* **Points d'attention levés :**
  * Règle du *dunder init* : `__init__` avec double tiret bas obligatoire (un simple `_init_` n'est pas reconnu par le compilateur Python comme constructeur).

---

### Atelier 3 : Validation IPv4 Monobloc (TP0 V1)
* **Fichier :** [TP0/Exo1.py](./TP0/Exo1.py)
* **Objectif :** Valider une adresse réseau saisie au clavier selon 3 règles :
  1. Séparation par les points (`ip.split(".")`).
  2. Contrôle de cardinalité : présence d'exactement 4 octets (`len(octets) == 4`).
  3. Contrôle des bornes : vérification que chaque octet est un entier compris dans $[0, 255]$.
* **Structure :** Script monolithique combinant saisie, logique algorithmique et affichage.

---

### Atelier 4 : Architecture Modulaire & SoC (TP0 V2 & TP1)
* **Dossiers :** [TP0/TP0 V2/](./TP0/TP0%20V2/) et [TP1/](./TP1/)
* **Documentation associée :** 📘 **[README TP0 V2](./TP0/TP0%20V2/README.md)**
* **Pattern appliqué :** *Separation of Concerns* (SoC).
  * **Module `reseau.py` :** Pure logique métier sans `input` ni `print`, retournant un booléen (`True`/`False`).
  * **Client `main.py` :** Interface utilisateur en ligne de commande réalisant l'import spécifique :
    ```python
    from reseau import valider_ip
    ```

---

## 3. Synthèse Architecturale : Script, Module & Package

| Concept | Nature Physique | Rôle | Mode d'Utilisation |
| :--- | :--- | :--- | :--- |
| **Script** | Fichier `.py` | Point d'entrée exécutable avec interaction I/O. | `python main.py` |
| **Module** | Fichier `.py` | Bibliothèque de fonctions ou classes réutilisables. | `import nom_module` |
| **Package** | Dossier avec `__init__.py` | Regroupement logique de plusieurs modules connexes. | `from package.module import fonction` |

---

## 4. Guide d'Exécution & Tests

### Tester l'atelier POO :
```powershell
cd "Matière\Matiere Python\TP"
python -i main.py
```
```python
>>> legolas = Archer(speed=5, arrows=15)
>>> legolas.attack()
Yes my lord !
>>> legolas.health
100
```

### Tester le validateur modulaire (TP0 V2) :
```powershell
cd "Matière\Matiere Python\TP\TP0\TP0 V2"
python main.py
```
