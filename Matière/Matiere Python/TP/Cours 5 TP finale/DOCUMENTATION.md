# Documentation du Projet - TP Final : Client / Serveur Chat

> **Master 1 SI - CFA INSTA**  
> **Matière :** Programmation Python  
> **Enseignant :** M. F. Cárdenas (`f.cardenas@cfa-insta.fr`)  
> **Modalités :** Groupe de 3 maximum (1 machine serveur-client + 2 machines clients)  
> **Format d'évaluation :** Soutenance orale de 15 minutes avec diapositives + Démonstration en direct + Dépôt Git public

---

## 📑 Sommaire

1. [Contexte et Objectifs du Projet](#1-contexte-et-objectifs-du-projet)
2. [Architecture Technique Prévue](#2-architecture-technique-prévue)
3. [Feuille de Route & Liste des Tâches (Backlog)](#3-feuille-de-route--liste-des-tâches-backlog)
   - [Phase 1 : Initialisation & Dépôt Git](#phase-1--initialisation--dépôt-git)
   - [Phase 2 : Analyse, Compréhension & Commentaires](#phase-2--analyse-compréhension--commentaires)
   - [Phase 3 : Améliorations & Robustesse (Console)](#phase-3--améliorations--robustesse-console)
   - [Phase 4 : Interface Graphique avec Tkinter](#phase-4--interface-graphique-avec-tkinter)
   - [Phase 5 : Options Bonus Avancées](#phase-5--options-bonus-avancées)
   - [Phase 6 : Recette, Tests & Diaporama](#phase-6--recette-tests--diaporama)
4. [Spécifications du Protocole de Communication](#4-spécifications-du-protocole-de-communication)
5. [Structure Recommandée des Fichiers](#5-structure-recommandée-des-fichiers)
6. [Organisation de la Soutenance Orale (15 minutes)](#6-organisation-de-la-soutenance-orale-15-minutes)
   - [Découpage du temps (15 min chrono)](#découpage-du-temps-15-min-chrono)
   - [Trame recommandée du Diaporama (Support visuel)](#trame-recommandée-du-diaporama-support-visuel)
   - [Critères d'évaluation de M. Cárdenas](#critères-dévaluation-de-m-cárdenas)

---

## 1. Contexte et Objectifs du Projet

L'objectif de ce TP final est de concevoir, fiabiliser et enrichir une application complète de **messagerie instantanée (Chat) Client / Serveur** en Python au sein d'un environnement réseau local (LAN).

### 🎯 Principaux attendus :
- **Comprendre le code et ajouter des commentaires :** Maîtriser le fonctionnement de chaque brique (sockets, threading, encodage) et documenter le code selon la norme PEP 257.
- **Améliorer le code existant :** Gérer rigoureusement les erreurs (déconnexions inattendues, fermeture des sockets, exceptions réseau) et soigner l'ergonomie des messages/prompts.
- **Conception d'une interface graphique interactive avec `tkinter` :** Remplacer ou compléter l'interface terminal par une application fenêtrée fluide et responsive.
- **Options bonus :**
  - **Découverte automatique des serveurs :** Rechercher automatiquement les serveurs actifs sur le réseau local via broadcast UDP et permettre à l'utilisateur de choisir son serveur dans une liste.
  - **Identification du serveur :** Le serveur doit renvoyer son nom sur réception d'une commande dédiée et l'afficher dans l'interface client.
- **Démarche d'ingénierie logicielle propre :** Versionnement continu sous Git (dépôt public), structure modulaire, code PEP 8.
- **Présentation & Restitution :** Présenter le projet lors d'une soutenance orale de 15 minutes avec support de présentation (diapositives) et démonstration technique.

### 📦 Rendu final :
* **Démonstration et présentation orale (15 minutes)** devant la classe et l'enseignant.
* **Envoi de l'URL du dépôt Git public** par email à : `f.cardenas@cfa-insta.fr`.

---

## 2. Architecture Technique Prévue

```text
                  ┌───────────────────────────────────────────────┐
                  │                 SERVEUR CHAT                  │
                  │   - Écoute TCP (Port 5000, multi-clients)     │
                  │   - Diffusion des messages (Broadcast)        │
                  │   - Balise répondeur UDP (Port 5001 - Option) │
                  └───────────────────────┬───────────────────────┘
                                          │
                 ┌────────────────────────┼────────────────────────┐
                 │ (Connexion TCP)        │ (Connexion TCP)        │ (Connexion TCP)
                 ▼                        ▼                        ▼
      ┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐
      │    Client 1 (GUI)   │  │    Client 2 (GUI)   │  │    Client 3 (GUI)   │
      │ Machine Serveur/Hôte│  │   Poste Étudiant 2  │  │   Poste Étudiant 3  │
      └─────────────────────┘  └─────────────────────┘  └─────────────────────┘
```

- **Couche Réseau Principal (TCP - `socket.SOCK_STREAM`) :** Connexion orientée connexion, fiable, ordonnée et sans perte pour l'échange des messages textuels.
- **Couche Découverte Réseau (UDP - `socket.SOCK_DGRAM`) :** Mode diffusion (`SO_BROADCAST`) sur `255.255.255.255` pour localiser dynamiquement les instances de serveur sans configuration manuelle d'IP.
- **Modèle de Concurrence (`threading`) :**
  - **Serveur :** 1 thread par client connecté pour la réception des flux entrants + 1 thread d'écoute broadcast UDP.
  - **Client :** 1 thread d'écoute réseau en continu + thread principal dédié à la boucle événementielle graphique Tkinter (`mainloop`).

---

## 3. Feuille de Route & Liste des Tâches (Backlog)

### Phase 1 : Initialisation & Dépôt Git
- [x] **Tâche 1.1 :** Télécharger le code source de base fourni par l'enseignant (`https://gitlab.com/f.cardenas14/tp_python_clientserver_chat`).
- [ ] **Tâche 1.2 :** Initialiser un nouveau dépôt Git public (GitHub ou GitLab).
- [x] **Tâche 1.3 :** Créer le fichier `.gitignore` adapté à Python (ignorer `__pycache__/`, `.vscode/`, `.idea/`, etc.).
- [x] **Tâche 1.4 :** Rédiger un fichier `README.md` introductif avec prérequis, commandes de lancement et attribution des rôles.
- [x] **Tâche 1.5 :** Répartir les rôles au sein de l'équipe (1 serveur/client + 2 clients).

#### 👥 Fiches de Rôles et Répartition des Responsabilités (Trinôme)

Conformément à la consigne *(1 serveur-client + 2 clients)*, les rôles sont précisément distribués pour maximiser l'efficacité du groupe :

| Rôle & Poste | Responsable | Périmètre Technique | Rôle pendant la Soutenance (15 min) |
| :--- | :--- | :--- | :--- |
| **Poste 1 : Architecte Serveur & Hôte Réseau**<br>*(Machine Serveur-Client)* | *Étudiant 1* | • Développement et maintenance de `server.py`<br>• Gestion de la boucle d'écoute TCP `accept()` et des threads clients<br>• Gestion de la liste des connectés et diffusion (`broadcast`)<br>• Interception des exceptions réseau (`ConnectionResetError`, `BrokenPipeError`) sans crash<br>• Implémentation des commandes d'administration (`/help`, `/list`, `/name`, `/quit`) | • Présente l'architecture globale TCP et les choix de conception (3 min)<br>• Démarre le serveur et commente les logs réseau en direct pendant la démo |
| **Poste 2 : Lead Interface Graphique (Tkinter)**<br>*(Machine Client 1)* | *Étudiant 2* | • Conception de l'interface `client_gui.py` avec Tkinter<br>• Zone d'historique avec défilement automatique (`ScrolledText`)<br>• Thread-safety : écoute asynchrone sans figer la boucle `mainloop`<br>• Ergonomie : gestion des raccourcis claviers (touche `Entrée`) et styles visuels (couleurs par type de message) | • Explique la gestion du multithreading côté client (éviter le freeze d'UI)<br>• Réalise les échanges de messages en direct pendant la démo |
| **Poste 3 : Intégrateur, Options Bonus (UDP) & QA**<br>*(Machine Client 2)* | *Étudiant 3* | • Balise répondeur UDP serveur & Scanner broadcast UDP client (`255.255.255.255:5001`)<br>• Intégration de la sélection de serveur en 1 clic (`ttk.Combobox`)<br>• Recette globale et tests de charge sur le réseau local réel CFA INSTA<br>• Réalisation du diaporama de présentation (`Support_Soutenance.pptx`) | • Présente le mécanisme d'auto-découverte UDP et la commande `/name`<br>• Démontre la résilience aux pannes (simulation de crash client)<br>• Anime la conclusion et le bilan |

### Phase 2 : Analyse, Compréhension & Commentaires
- [ ] **Tâche 2.1 :** Analyser le cycle de vie du serveur (`socket()`, `bind()`, `listen()`, `accept()`).
- [ ] **Tâche 2.2 :** Analyser le cycle de vie du client (`socket()`, `connect()`, `send()`, `recv()`).
- [ ] **Tâche 2.3 :** Rédiger des docstrings claires (norme PEP 257) pour chaque fonction et classe.
- [ ] **Tâche 2.4 :** Ajouter des commentaires explicatifs détaillés sur les points critiques (encodage UTF-8, synchronisation des threads).

### Phase 3 : Améliorations & Robustesse (Console)
- [ ] **Tâche 3.1 :** Intercepter les déconnexions brutales côté serveur sans crash (`ConnectionResetError`, `BrokenPipeError`).
- [ ] **Tâche 3.2 :** Nettoyer dynamiquement la liste des clients actifs lors d'un départ et fermer proprement les sockets.
- [ ] **Tâche 3.3 :** Diffuser un message système global lorsqu'un utilisateur rejoint ou quitte la salle (`*** [Pseudo] a rejoint le salon ***`).
- [ ] **Tâche 3.4 :** Améliorer la mise en forme des messages avec horodatage automatique (`[HH:MM:SS] [Pseudo] : message`).
- [ ] **Tâche 3.5 :** Implémenter les commandes d'administration :
  - `/help` : Affiche l'aide et les commandes utilisables.
  - `/list` : Liste les pseudos actuellement connectés.
  - `/name` : Renvoie le nom officiel du serveur.
  - `/quit` : Déconnexion propre de la session.

### Phase 4 : Interface Graphique avec Tkinter
- [ ] **Tâche 4.1 :** Créer le panneau supérieur de connexion (IP, Port, Pseudo, Statut connecté/déconnecté).
- [ ] **Tâche 4.2 :** Développer la zone centrale de chat (`scrolledtext.ScrolledText`) en lecture seule avec scroll automatique.
- [ ] **Tâche 4.3 :** Mettre en place un système de styles visuels (couleurs différentes pour les messages reçus, envoyés et système).
- [ ] **Tâche 4.4 :** Concevoir la zone inférieure de saisie avec champ texte (`Entry`), bouton « Envoyer » et écoute de la touche `Entrée`.
- [ ] **Tâche 4.5 :** Sécuriser la communication entre le thread réseau et Tkinter (éviter les freezes et fermer les threads à la fermeture de la fenêtre `WM_DELETE_WINDOW`).

### Phase 5 : Options Bonus Avancées
- [ ] **Tâche 5.1 (Nom du Serveur) :** Permettre de nommer le serveur lors de son démarrage et renvoyer ce nom via la commande `/name`.
- [ ] **Tâche 5.2 (Balise UDP Serveur) :** Lancer un thread UDP sur le port 5001 répondant aux pings broadcast par `CHAT_SERVER_HERE:<NOM_SERVEUR>:<PORT_TCP>`.
- [ ] **Tâche 5.3 (Scanner UDP Client) :** Ajouter un bouton « Scanner le réseau » sur l'interface Tkinter qui liste les serveurs trouvés dans un menu déroulant (`ttk.Combobox`).
- [ ] **Tâche 5.4 (Connexion Directe) :** Remplir automatiquement les champs IP et Port lors de la sélection d'un serveur détecté.

### Phase 6 : Recette, Tests & Diaporama
- [ ] **Tâche 6.1 :** Tester le bon fonctionnement en boucle locale (`127.0.0.1` avec plusieurs clients).
- [ ] **Tâche 6.2 :** Valider le fonctionnement en réseau local réel avec 3 ordinateurs distincts (Wi-Fi/Ethernet CFA INSTA).
- [ ] **Tâche 6.3 :** Concevoir le support de présentation (diaporama `Support_Soutenance.pptx`).
- [ ] **Tâche 6.4 :** Répéter la présentation orale chronométrée (15 minutes).
- [ ] **Tâche 6.5 :** Vérifier que le dépôt Git est bien public et envoyer l'URL par mail à `f.cardenas@cfa-insta.fr`.

---

## 4. Spécifications du Protocole de Communication

| Type de Message | Format Brut / Trame | Rôle & Traitement |
| :--- | :--- | :--- |
| **Enregistrement Pseudo** | `NICK:<pseudo>` | Envoyé à la connexion pour identifier l'utilisateur. |
| **Message Standard** | `MSG:<texte>` *(ou texte direct)* | Diffusé à l'ensemble des clients connectés sous forme formatée. |
| **Commande Nom** | `/name` | Le serveur répond avec son nom d'instance officiel. |
| **Commande Utilisateurs** | `/list` | Le serveur renvoie la liste des utilisateurs connectés. |
| **Déconnexion Propre** | `/quit` | Informe le serveur pour fermeture de session sans erreur. |
| **Découverte (UDP)** | `DISCOVER_CHAT_SERVER` | Broadcast émis par le client sur `255.255.255.255:5001`. |
| **Réponse Découverte (UDP)** | `CHAT_SERVER_HERE:<Nom>:<Port>` | Réponse envoyée par le serveur pour se déclarer disponible. |

---

## 5. Structure Recommandée des Fichiers

```text
Cours TP finale/
│
├── DOCUMENTATION.md                # Référence complète du projet et suivi des tâches
├── README.md                       # Guide d'installation, lancement et documentation Git
├── .gitignore                      # Exclusion des fichiers temporaires Python/IDE
│
├── server.py                       # Serveur TCP multithreadé + Répondeur UDP (Option)
├── client_gui.py                   # Client graphique complet Tkinter + Scanner UDP (Option)
├── client_cli.py                   # (Optionnel) Client console en mode terminal
│
└── presentation/
    └── Support_Soutenance.pptx     # Diaporama pour la soutenance orale de 15 minutes
```

---

## 6. Organisation de la Soutenance Orale (15 minutes)

### ⏱️ Découpage du temps (15 min chrono)

| Durée | Phase | Contenu & Objectifs |
| :---: | :--- | :--- |
| **00:00 - 03:00** *(3 min)* | **Introduction & Architecture** | Présentation des membres du groupe, du contexte, du schéma d'architecture (TCP/UDP) et du protocole d'échange. |
| **03:00 - 08:00** *(5 min)* | **Démonstration en Direct** | • Lancement du serveur sur la machine hôte.<br>• Découverte automatique des serveurs via l'option broadcast.<br>• Connexion simultanée des 2 clients.<br>• Échanges de messages en temps réel.<br>• Test de robustesse : coupure brutale d'un client sans plantage du serveur. |
| **08:00 - 11:00** *(3 min)* | **Revue de Code & Défis** | Présentation des points techniques clés : gestion des threads, interdiction du blocage de l'UI Tkinter, gestion des exceptions réseau. |
| **11:00 - 15:00** *(4 min)* | **Questions / Réponses** | Réponses aux questions techniques posées par M. Cárdenas. |

---

### 🖥️ Trame recommandée du Diaporama (Support visuel)

Un diaporama concis de **6 à 8 diapositives** est idéal pour tenir le timing :

1. **Diapositive 1 - Titre :** Intitulé du projet, filière Master 1 SI, noms et prénoms des membres du groupe, date.
2. **Diapositive 2 - Cahier des charges & Objectifs :** Synthèse des besoins (Chat multithreadé, interface Tkinter, options bonus).
3. **Diapositive 3 - Architecture Réseau :** Schéma illustrant la communication TCP (chat) et UDP (découverte automatique).
4. **Diapositive 4 - Conception Logicielle & Threading :** Rôle des threads côté serveur (un thread par socket) et côté client (thread réseau + boucle `mainloop` Tkinter).
5. **Diapositive 5 - Gestion des Erreurs & Sécurité Réseau :** Exemples d'exceptions gérées (`ConnectionResetError`, `BrokenPipeError`) et déconnexion propre.
6. **Diapositive 6 - Interface Graphique Tkinter :** Aperçu des fonctionnalités ergonomiques (choix du serveur, chat avec styles, scroll automatique).
7. **Diapositive 7 - Démonstration :** Transition vers la démonstration en direct (scénario du test).
8. **Diapositive 8 - Conclusion & Bilan :** Retour d'expérience, difficultés rencontrées, pistes d'évolution, lien vers le dépôt Git public.

---

### 🎯 Critères d'évaluation de M. Cárdenas

1. **Qualité et clarté du code :** Clarté de la structure, rigueur des commentaires explicatifs, respect de la PEP 8.
2. **Robustesse applicative :** Résistance aux pannes réseau, absence de freeze de l'interface graphique.
3. **Ergonomie de l'interface Tkinter :** Facilité d'utilisation, clarté visuelle.
4. **Réussite des options bonus :** Fonctionnement effectif du scan UDP et de la commande `/name`.
5. **Prestation orale :** Clarté des explications, dynamisme de la démo, maîtrise des concepts réseau et respect des 15 minutes.
