# Documentation du Projet - TP Final : Client / Serveur Chat

> **Master 1 SI - CFA INSTA**  
> **Matière :** Python  
> **Enseignant :** M. F. Cárdenas (`f.cardenas@cfa-insta.fr`)  
> **Modalités :** Groupe de 3 maximum (1 machine serveur-client + 2 machines clients)

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
   - [Phase 6 : Recette, Tests & Rendu](#phase-6--recette-tests--rendu)
4. [Spécifications du Protocole de Communication](#4-spécifications-du-protocole-de-communication)
5. [Structure Recommandée des Fichiers](#5-structure-recommandée-des-fichiers)
6. [Critères d'Évaluation & Préparation de la Soutenance](#6-critères-dévaluation--préparation-de-la-soutenance)

---

## 1. Contexte et Objectifs du Projet

L'objectif de ce TP final est de concevoir et réaliser une application complète de **messagerie instantanée (Chat) Client / Serveur** en Python.

Le système doit permettre à plusieurs utilisateurs de communiquer en temps réel au travers d'un réseau local (LAN).

### Principaux attendus :
- Maîtrise des communications réseau bas niveau avec le module standard **`socket`** (TCP/IP).
- Gestion de la concurrence et du multithreading avec le module **`threading`**.
- Conception d'une interface graphique interactive avec **`tkinter`**.
- Ajout de fonctionnalités avancées de découverte réseau automatique et de commandes serveur.
- Démarche de développement propre : versionnement Git, code documenté, gestion stricte des erreurs.

---

## 2. Architecture Technique Prévue

```
                  ┌───────────────────────────────┐
                  │        SERVEUR CHAT           │
                  │   - Écoute TCP (Port 5000)    │
                  │   - Diffusion (Broadcast)     │
                  │   - Répondeur UDP (Port 5001) │
                  └───────────────┬───────────────┘
                                  │
         ┌────────────────────────┼────────────────────────┐
         │ (Connexion TCP)        │ (Connexion TCP)        │ (Connexion TCP)
         ▼                        ▼                        ▼
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│  Client 1 (GUI) │      │  Client 2 (GUI) │      │  Client 3 (GUI) │
│  Machine Hôte   │      │ Machine Distante│      │ Machine Distante│
└─────────────────┘      └─────────────────┘      └─────────────────┘
```

- **Protocole de transport :** **TCP** (`SOCK_STREAM`) pour garantir la fiabilité de la transmission des messages sans perte de paquets.
- **Protocole de découverte (Bonus) :** **UDP** (`SOCK_DGRAM`) en mode diffusion (`SO_BROADCAST`) pour localiser automatiquement les serveurs actifs sur le sous-réseau sans avoir à saisir l'adresse IP manuellement.
- **Gestion multithreadée :**
  - **Côté Serveur :** Un thread dédié par client connecté pour écouter ses messages sans bloquer les autres utilisateurs.
  - **Côté Client :** Un thread d'écoute réseau en arrière-plan pour recevoir les messages en continu sans figer l'interface graphique Tkinter (qui tourne sur la boucle `mainloop`).

---

## 3. Feuille de Route & Liste des Tâches (Backlog)

### Phase 1 : Initialisation & Dépôt Git
- [ ] **Tâche 1.1 :** Récupérer le code source de base fourni par l'enseignant : `https://gitlab.com/f.cardenas14/tp_python_clientserver_chat`.
- [ ] **Tâche 1.2 :** Initialiser un nouveau dépôt Git public (sur GitHub ou GitLab).
- [ ] **Tâche 1.3 :** Mettre en place un fichier `.gitignore` adapté à Python (ignorer `__pycache__/`, `.vscode/`, `.idea/`, etc.).
- [ ] **Tâche 1.4 :** Rédiger un fichier `README.md` introductif avec les prérequis et les instructions d'installation/lancement.
- [ ] **Tâche 1.5 :** Répartir les rôles au sein du groupe (1 binôme/trinôme).

### Phase 2 : Analyse, Compréhension & Commentaires
- [ ] **Tâche 2.1 :** Analyser le fonctionnement des sockets côté serveur (`socket()`, `bind()`, `listen()`, `accept()`).
- [ ] **Tâche 2.2 :** Analyser le fonctionnement des sockets côté client (`socket()`, `connect()`, `send()`, `recv()`).
- [ ] **Tâche 2.3 :** Documenter chaque fonction et classe selon les standards Python (docstrings PEP 257).
- [ ] **Tâche 2.4 :** Ajouter des commentaires précis sur les passages critiques (encodage/décodage UTF-8, synchronisation des threads).

### Phase 3 : Améliorations & Robustesse (Console)
- [ ] **Tâche 3.1 :** Gérer les déconnexions brutales des clients sans faire crasher le serveur (`ConnectionResetError`, `BrokenPipeError`).
- [ ] **Tâche 3.2 :** Nettoyer la liste des clients actifs lors d'un départ et fermer proprement les sockets (`client.close()`).
- [ ] **Tâche 3.3 :** Informer tous les membres du chat lorsqu'un utilisateur rejoint ou quitte la salle (`*** Alice a rejoint le salon ***`).
- [ ] **Tâche 3.4 :** Améliorer les messages de saisie (prompt) et ajouter un horodatage `[HH:MM:SS]` sur chaque message.
- [ ] **Tâche 3.5 :** Implémenter des commandes d'administration :
  - `/help` : Affiche la liste des commandes disponibles.
  - `/list` : Affiche la liste des utilisateurs actuellement connectés.
  - `/quit` : Déconnecte proprement le client.

### Phase 4 : Interface Graphique avec Tkinter
- [ ] **Tâche 4.1 :** Concevoir une fenêtre de dialogue initiale (ou un panneau supérieur) pour configurer :
  - L'adresse IP du serveur.
  - Le port d'écoute.
  - Le pseudo de l'utilisateur.
- [ ] **Tâche 4.2 :** Concevoir la zone centrale de discussion :
  - Zone de texte avec défilement automatique (`scrolledtext.ScrolledText`).
  - Zone lecture seule pour empêcher la modification manuelle de l'historique par l'utilisateur.
  - Couleurs et balises textuelles (ex: messages système en gris/italique, pseudos en gras, alertes en rouge).
- [ ] **Tâche 4.3 :** Concevoir la zone inférieure de saisie :
  - Champ de texte (`Entry`).
  - Bouton « Envoyer ».
  - Liaison de la touche `Entrée` (`<Return>`) pour envoyer le message directement.
- [ ] **Tâche 4.4 :** Intégrer la communication multithread :
  - Thread d'écoute qui met à jour l'interface via des appels sécurisés.
  - Gestion propre de la fermeture de la fenêtre Tkinter (`WM_DELETE_WINDOW`) pour avertir le serveur et couper la connexion réseau sans thread zombie.

### Phase 5 : Options Bonus Avancées
- [ ] **Tâche 5.1 (Option Nom de Serveur) :**
  - Configurer un nom d'instance personnalisable sur le serveur (ex: `"Serveur Salle TP 204"`).
  - Créer la commande `/name` côté client pour interroger le serveur et afficher son nom.
- [ ] **Tâche 5.2 (Option Découverte Réseau Automatique) :**
  - **Côté Serveur :** Lancer un thread d'écoute UDP (ex: port 5001) qui attend les messages de broadcast `"DISCOVER_CHAT_SERVER"` et répond immédiatement avec son nom, son adresse IP et son port TCP.
  - **Côté Client :** Ajouter un bouton « Rechercher les serveurs » dans la fenêtre de connexion Tkinter qui émet un paquet UDP broadcast, écoute les réponses reçues pendant 1 à 2 secondes, et remplit une liste déroulante (`ttk.Combobox`) avec les serveurs trouvés.
- [ ] **Tâche 5.3 :** Connexion en un clic via la sélection d'un serveur dans la liste.

### Phase 6 : Recette, Tests & Rendu
- [ ] **Tâche 6.1 :** Tester le fonctionnement en local (`127.0.0.1` avec plusieurs fenêtres clientes simultanées).
- [ ] **Tâche 6.2 :** Tester le fonctionnement sur le réseau local réel entre plusieurs ordinateurs distincts (Wi-Fi ou Ethernet CFA-INSTA).
- [ ] **Tâche 6.3 :** Vérifier l'absence d'erreurs dans la console lors des cas limites (serveur coupé en premier, client fermé sans `/quit`, message vide).
- [ ] **Tâche 6.4 :** Vérifier que le dépôt Git est bien **public** et contient l'intégralité du code et de la documentation.
- [ ] **Tâche 6.5 :** Préparer le support de présentation orale (diaporama court, répartition de la parole, scénario de démo en direct).
- [ ] **Tâche 6.6 :** Envoyer l'URL du dépôt par email à `f.cardenas@cfa-insta.fr`.

---

## 4. Spécifications du Protocole de Communication

Afin d'assurer la cohérence des échanges entre le client et le serveur :

| Type de Message | Format Brut / Payload | Description |
| :--- | :--- | :--- |
| **Identification** | `NICK:<pseudo>` | Premier message envoyé par le client après la connexion TCP. |
| **Message standard** | `MSG:<texte>` ou texte direct | Message diffusé à l'ensemble du salon sous le format `[HH:MM] [Pseudo] : texte`. |
| **Commande Nom** | `/name` | Requête client pour obtenir le nom d'affichage du serveur. |
| **Commande Liste** | `/list` | Requête client pour recevoir la liste des utilisateurs en ligne. |
| **Déconnexion** | `/quit` | Signal de sortie propre envoyé par le client avant fermeture du socket. |
| **Broadcast Découverte (UDP)** | `DISCOVER_CHAT_SERVER` | Message UDP broadcast émis par le client sur `255.255.255.255`. |
| **Réponse Découverte (UDP)** | `SERVER_INFO:<Nom>:<Port>` | Réponse envoyée par le serveur au client demandeur. |

---

## 5. Structure Recommandée des Fichiers

```text
Cours TP finale/
│
├── DOCUMENTATION.md                # Le présent document de référence et suivi
├── README.md                       # Guide d'installation et d'utilisation pour le correcteur
├── .gitignore                      # Fichiers et dossiers à exclure de Git
│
├── server.py                       # Serveur TCP multithreadé + Répondeur UDP
├── client_gui.py                   # Client graphique principal (Tkinter)
├── client_cli.py                   # (Optionnel) Client console en mode texte
│
└── presentation/
    └── Support_Soutenance.pptx     # Support pour la présentation orale du groupe
```

---

## 6. Critères d'Évaluation & Préparation de la Soutenance

### Critères techniques (Code & Git) :
1. **Dépôt Git :** Historique des commits régulier, messages de commit explicites, contributions visibles des membres du groupe.
2. **Commentaires & Clarté :** Qualité pédagogique des commentaires, respect de la PEP 8.
3. **Robustesse :** Absence de blocage d'interface (UI freeze) et gestion sans crash des erreurs réseau.
4. **Interface Tkinter :** Ergonomie, clarté visuelle, gestion du scroll et des touches claviers.
5. **Options :** Bon fonctionnement du scan automatique et des commandes.

### Déroulé recommandé de la démonstration orale :
- **Introduction (2 min) :** Présentation du groupe, des choix d'architecture et du protocole choisi.
- **Démonstration en direct (5 min) :**
  - Lancement du serveur sur une machine.
  - Lancement de 2 clients sur d'autres postes.
  - Découverte automatique des serveurs via l'option broadcast.
  - Échange de messages en temps réel.
  - Démonstration de la gestion d'erreur (ex: coupure brutale d'un client et reconnexion).
- **Revue de code (3 min) :** Explication des parties clés (threads, boucle d'écoute, synchronisation Tkinter).
- **Questions / Réponses (3-5 min) :** Réponses aux questions de l'enseignant.

