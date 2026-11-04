# 💬 Application de Chat Client / Serveur Multi-utilisateurs

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg?logo=python)](https://www.python.org/)
[![GUI](https://img.shields.io/badge/GUI-Tkinter-brightgreen.svg)](https://docs.python.org/3/library/tkinter.html)
[![Réseau](https://img.shields.io/badge/Protocole-TCP%20%2F%20UDP-orange.svg)](https://docs.python.org/3/library/socket.html)
[![Formation](https://img.shields.io/badge/Master-1%20SI%20%7C%20CFA%20INSTA-red.svg)](https://www.cfa-insta.fr/)

> **Projet Final Python - Master 1 Systèmes d'Information (CFA INSTA)**  
> **Enseignant :** M. F. Cárdenas (`f.cardenas@cfa-insta.fr`)  
> **Dépôt source initial :** [tp_python_clientserver_chat](https://gitlab.com/f.cardenas14/tp_python_clientserver_chat)

---

## 📌 Présentation du Projet

Ce projet implémente une solution de messagerie instantanée en réseau local (LAN) basée sur une architecture **Client / Serveur multithreadée** en Python.

L'application permet à plusieurs utilisateurs d'échanger des messages en temps réel, soit via une **interface graphique moderne (Tkinter)**, soit en **ligne de commande**.

### ✨ Fonctionnalités Clés
- **Diffusion centralisée (Broadcast TCP) :** Tout message envoyé par un client est instantanément retransmis à l'ensemble des participants connectés.
- **Concurrence & Multithreading :** Gestion asynchrone des flux sans blocage ni latence.
- **Robustesse & Tolérance aux pannes :** Gestion des déconnexions brutales et libération immédiate des ressources réseau.
- **Interface Graphique Tkinter :** Affichage soigné des messages, historique déroulant avec auto-scroll, personnalisation des couleurs et envoi rapide par la touche `Entrée`.
- **Commandes serveur intégrées :**
  - `/help` : Affiche la liste des commandes.
  - `/list` : Affiche la liste des utilisateurs en ligne.
  - `/name` : Renvoie le nom officiel de l'instance du serveur.
  - `/quit` : Déconnexion propre de la session.

### 🌟 Options Bonus Réalisées
1. **🔍 Découverte automatique des serveurs sur le réseau (Broadcast UDP) :**
   Le client peut scanner le réseau local en un clic. Le serveur répond automatiquement via une balise UDP sur le port dédié (`5001`), éliminant le besoin de saisir l'adresse IP manuellement.
2. **🏷️ Identification dynamique du serveur :**
   Le serveur diffuse et renvoie son nom personnalisé (ex: *« Serveur INSTA Salle 204 »*) lors de la découverte et via la commande `/name`.

---

## 🏗️ Architecture Technique

```text
                  ┌───────────────────────────────────────────────┐
                  │                 SERVEUR CHAT                  │
                  │   - Écoute TCP (Port 5000)                    │
                  │   - Diffusion (Broadcast des messages)        │
                  │   - Balise d'annonce UDP (Port 5001)          │
                  └───────────────────────┬───────────────────────┘
                                          │
                 ┌────────────────────────┼────────────────────────┐
                 │ (Connexion TCP)        │ (Connexion TCP)        │ (Connexion TCP)
                 ▼                        ▼                        ▼
      ┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐
      │    Client 1 (GUI)   │  │    Client 2 (GUI)   │  │    Client 3 (GUI)   │
      │ Machine Hôte        │  │ Poste Étudiant 2    │  │ Poste Étudiant 3    │
      └─────────────────────┘  └─────────────────────┘  └─────────────────────┘
```

- **Couche Réseau :**
  - **TCP (`socket.AF_INET`, `socket.SOCK_STREAM`) :** Assure l'intégrité et l'ordre d'arrivée des messages.
  - **UDP (`socket.AF_INET`, `socket.SOCK_DGRAM`) avec `SO_BROADCAST` :** Utilisé pour la détection dynamique des serveurs sur le sous-réseau `255.255.255.255`.
- **Gestion des Threads (`threading`) :**
  - Un thread d'écoute par client côté serveur.
  - Un thread de réception dédié côté client pour ne jamais figer la boucle événementielle `mainloop` de Tkinter.

---

## 📂 Structure du Répertoire

```text
.
├── DOCUMENTATION.md        # Suivi détaillé des tâches, backlog et guide d'évaluation
├── README.md               # Le présent fichier d'accueil et guide de lancement
├── .gitignore              # Règles d'exclusion des fichiers temporaires Git
│
├── server.py               # Serveur TCP multithreadé + Répondeur de découverte UDP
├── client_gui.py           # Client avec interface graphique Tkinter + Scan UDP
├── client_cli.py           # (Optionnel) Client interactif en invite de commande
│
└── presentation/
    └── Support_Soutenance.pptx # Diaporama de présentation pour la soutenance orale
```

---

## ⚙️ Prérequis & Installation

- **Python 3.8 ou supérieur** installé sur votre machine.
- Aucun paquet tiers lourd n'est requis : le projet s'appuie exclusivement sur la **bibliothèque standard Python** (`socket`, `threading`, `tkinter`, `datetime`).

Vérifiez votre version de Python :
```bash
python --version
```

---

## 🚀 Guide de Démarrage Rapide

### 1. Démarrer le Serveur
Sur la machine faisant office de serveur (ou dans un premier terminal) :
```bash
python server.py
```
> Par défaut, le serveur écoute sur toutes les interfaces (`0.0.0.0`) sur le port TCP **5000** et répond aux annonces UDP sur le port **5001**.

### 2. Démarrer un Client Graphique (Tkinter)
Dans un nouveau terminal (ou sur une autre machine du même réseau) :
```bash
python client_gui.py
```
1. Saisissez votre **Pseudo**.
2. Cliquez sur **« Scanner le réseau »** pour détecter automatiquement le serveur, ou renseignez directement son adresse IP (ex: `127.0.0.1` en local).
3. Cliquez sur **« Connexion »**.
4. Vous pouvez commencer à échanger !

### 3. (Optionnel) Démarrer un Client Console
Pour tester sans interface graphique :
```bash
python client_cli.py
```

---

## 👥 Organisation de l'Équipe & Attribution des Rôles

Le projet est conçu pour un groupe de **3 étudiants maximum** (1 machine serveur-client + 2 machines clients) :

| Poste & Rôle | Responsable | Tâches Principales |
| :--- | :--- | :--- |
| **Poste 1 : Architecte Serveur & Réseau**<br>*(Machine Serveur-Client)* | *[Étudiant 1]* | Développement de `server.py`, sockets TCP, multi-clients, broadcast, gestion des erreurs et commandes serveur |
| **Poste 2 : Lead Interface Graphique (Tkinter)**<br>*(Machine Client 1)* | *[Étudiant 2]* | Conception de l'interface `client_gui.py`, liaison d'événements, styles et synchronisation thread-safe |
| **Poste 3 : Intégrateur & Options Bonus (UDP)**<br>*(Machine Client 2)* | *[Étudiant 3]* | Découverte automatique UDP (scan & balise), sélection 1 clic, tests réseau LAN CFA INSTA & diaporama |

---

## 🎤 Soutenance Orale (15 minutes)

La soutenance orale dure **15 minutes** et est découpée de la façon suivante :
- **00:00 - 03:00 (3 min) :** Présentation du projet, des membres et de l'architecture (TCP/UDP, Multithreading).
- **03:00 - 08:00 (5 min) :** Démonstration en direct avec 3 machines connectées en LAN (détection automatique, chat en temps réel, déconnexion propre).
- **08:00 - 11:00 (3 min) :** Revue de code (explication des points techniques clés).
- **11:00 - 15:00 (4 min) :** Questions / Réponses avec M. Cárdenas.

