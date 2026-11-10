# 📖 Dictionnaire Complet des Fonctions, Méthodes et Variables

> **Master 1 SI - CFA INSTA**  
> **Matière :** Programmation Python  
> **Enseignant :** M. F. Cárdenas (`f.cardenas@cfa-insta.fr`)  
> **Projet :** Application de Chat Client / Serveur Multi-utilisateurs  
> **Fichiers analysés :** `server.py`, `clientthread.py`, `client.py`

---

## 📑 Sommaire
1. [Vue d'ensemble de l'Architecture](#1-vue-densemble-de-larchitecture)
2. [Fichier `server.py` : Le Serveur Central](#2-fichier-serverpy--le-serveur-central)
   - [Méthodes de la classe `Server`](#méthodes-de-la-classe-server)
   - [Attributs et Variables de `server.py`](#attributs-et-variables-de-serverpy)
3. [Fichier `clientthread.py` : Le Gestionnaire de Thread Client](#3-fichier-clientthreadpy--le-gestionnaire-de-thread-client)
   - [Méthodes de la classe `ClientListener`](#méthodes-de-la-classe-clientlistener)
   - [Attributs et Variables de `clientthread.py`](#attributs-et-variables-de-clientthreadpy)
4. [Fichier `client.py` : Le Client Console](#4-fichier-clientpy--le-client-console)
   - [Méthodes de la classe `Client`](#méthodes-de-la-classe-client)
   - [Attributs et Variables de `client.py`](#attributs-et-variables-de-clientpy)
5. [Tableau Synoptique de Cycle de Vie des Variables Réseau](#5-tableau-synoptique-de-cycle-de-vie-des-variables-réseau)
6. [Fiche Anti-Sèche pour la Soutenance Orale](#6-fiche-anti-sèche-pour-la-soutenance-orale)

---

## 1. Vue d'ensemble de l'Architecture

Le projet s'articule autour de 3 classes interconnectées :

```
┌────────────────────────────────┐
│             Server             │  (server.py)
│  - self.listener               │  Gère le port d'écoute et la liste des clients.
│  - self.clients_sockets        │
└───────────────┬────────────────┘
                │ instancie 1 thread par client
                ▼
┌────────────────────────────────┐
│         ClientListener         │  (clientthread.py)
│  - self.socket                 │  Écoute un client spécifique en arrière-plan
│  - self.username               │  et appelle server.echo() pour diffuser.
└───────────────▲────────────────┘
                │ connexion réseau TCP
                ▼
┌────────────────────────────────┐
│             Client             │  (client.py)
│  - self.socket                 │  Gère l'interface console, la saisie clavier
│  - self.listen_thread          │  et la réception asynchrone des messages.
└────────────────────────────────┘
```

---

## 2. Fichier `server.py` : Le Serveur Central

Ce fichier gère l'écoute des connexions entrantes sur le port TCP et la diffusion centralisée (*echo/broadcast*).

### Méthodes de la classe `Server`

| Méthode | Paramètres | Type de retour | Description & Rôle Technique |
| :--- | :--- | :---: | :--- |
| **`__init__()`** | `self, port` | `None` | **Constructeur :** initialise le socket d'écoute passif `self.listener` (TCP/IPv4), effectue le `bind(('', port))`, place le socket en mode passif avec `listen(1)` et initialise la liste vide `self.clients_sockets`. |
| **`run()`** | `self` | `None` | **Boucle principale :** boucle infinie `while True` qui attend de nouveaux clients avec `self.listener.accept()`. Pour chaque arrivant, enregistre son socket et démarre un thread `ClientListener`. |
| **`remove_socket()`** | `self, socket` | `None` | **Déconnexion :** supprime le socket d'un client de la liste `self.clients_sockets` lorsque celui-ci quitte la conversation. |
| **`echo()`** | `self, data` | `None` | **Diffusion (*broadcast*) :** parcourt la liste `self.clients_sockets` et transmet le texte `data` encodé en UTF-8 à tous les clients via `sock.sendall()`. |

### Attributs et Variables de `server.py`

| Nom | Portée / Scope | Type | Rôle et Utilité |
| :--- | :--- | :---: | :--- |
| **`self.listener`** | Attribut d'instance (`Server`) | `socket.socket` | Socket passif principal du serveur, configuré avec `socket.AF_INET` (IPv4) et `socket.SOCK_STREAM` (TCP). |
| **`self.clients_sockets`** | Attribut d'instance (`Server`) | `list[socket.socket]` | Liste dynamique contenant les descripteurs de sockets de tous les clients connectés au salon. |
| **`port`** | Paramètre de `__init__` | `int` | Numéro de port sur lequel le serveur écoute (ex: `59001`). |
| **`client_socket`** | Variable locale à `run()` | `socket.socket` | Socket dédié retourné par `accept()` pour communiquer exclusivement avec le client qui vient d'arriver. |
| **`client_adress`** | Variable locale à `run()` | `tuple[str, int]` | Coordonnées réseau du client sous la forme `(adresse_IP, port_distant)`. |
| **`client_thread`** | Variable locale à `run()` | `ClientListener` | Instance de la classe `ClientListener` exécutée dans un thread parallèle pour ce client. |
| **`data`** | Paramètre de `echo()` | `str` | Message textuel reçu à diffuser à l'ensemble du salon. |
| **`sock`** | Variable locale à `echo()` | `socket.socket` | Variable d'itération représentant chaque socket client de la liste. |
| **`server`** | Variable globale (`__main__`) | `Server` | Instance unique du serveur créée et lancée au démarrage du script. |

---

## 3. Fichier `clientthread.py` : Le Gestionnaire de Thread Client

Ce fichier définit la classe **`ClientListener`**, qui hérite de `threading.Thread`. Chaque client connecté dispose de sa propre instance de thread.

### Méthodes de la classe `ClientListener`

| Méthode | Paramètres | Type de retour | Description & Rôle Technique |
| :--- | :--- | :---: | :--- |
| **`__init__()`** | `self, server, socket, address` | `None` | **Constructeur :** initialise le thread via `super().__init__()`, mémorise la référence du serveur hôte, le socket dédié et l'adresse IP du client. Définit le pseudo par défaut à `"No username"`. |
| **`run()`** | `self` | `None` | **Point d'entrée du thread :** boucle d'écoute `while self.listening` qui intercepte les paquets entrants avec `self.socket.recv(1024)`, les décode en UTF-8 et transmet le résultat à `handle_msg()`. |
| **`quit()`** | `self` | `None` | **Fermeture propre :** passe `self.listening` à `False`, ferme le socket avec `.close()`, demande au serveur de le retirer via `server.remove_socket()` et diffuse un message d'adieu. |
| **`handle_msg()`** | `self, data` | `None` | **Aiguilleur de protocole :** vérifie si le message est un enregistrement de pseudo (`USERNAME`), une commande de sortie (`QUIT` ou chaîne vide `""`), ou un message ordinaire à diffuser via `server.echo()`. |

### Attributs et Variables de `clientthread.py`

| Nom | Portée / Scope | Type | Rôle et Utilité |
| :--- | :--- | :---: | :--- |
| **`self.server`** | Attribut d'instance | `Server` | Référence vers l'instance de `Server` parent (permet d'appeler `self.server.echo()` et `self.server.remove_socket()`). |
| **`self.socket`** | Attribut d'instance | `socket.socket` | Socket TCP connecté au client surveillé par ce thread. |
| **`self.address`** | Attribut d'instance | `tuple[str, int]` | Tuple `(IP, port)` du client, utilisé pour tracer les logs dans la console. |
| **`self.listening`** | Attribut d'instance | `bool` | Drapeau de boucle (*flag*). Vaut `True` pendant la session et passe à `False` pour stopper le thread. |
| **`self.username`** | Attribut d'instance | `str` | Pseudo de l'utilisateur (initialisé à `"No username"`, puis mis à jour lors de la réception de `USERNAME <nom>`). |
| **`data`** | Variable locale à `run()` et paramètre de `handle_msg()` | `str` | Chaîne de caractères résultant du décodage UTF-8 des octets reçus du réseau. |
| **`username_result`** | Variable locale à `handle_msg()` | `re.Match \| None` | Objet résultat de l'expression régulière `^USERNAME (.*)$`. Contient le pseudo extrait dans `group(1)`. |

---

## 4. Fichier `client.py` : Le Client Console

Ce fichier permet à un utilisateur humain de dialoguer avec le serveur en envoyant ses messages au clavier et en recevant ceux des autres participants.

### Méthodes de la classe `Client`

| Méthode | Paramètres | Type de retour | Description & Rôle Technique |
| :--- | :--- | :---: | :--- |
| **`__init__()`** | `self, username, server, port` | `None` | **Constructeur :** crée le socket TCP actif, se connecte au serveur distant via `connect((server, port))`, mémorise le pseudo et envoie immédiatement la trame d'identification `"USERNAME <pseudo>"`. |
| **`listener()`** | `self` | `None` | **Boucle de réception :** boucle infinie exécutée dans un thread séparé qui attend les octets du serveur avec `self.socket.recv(1024)`, les décode et les transmet à `handle_msg()`. |
| **`listen()`** | `self` | `None` | **Lancement asynchrone :** crée l'objet `threading.Thread(target=self.listener)`, active l'attribut `daemon = True` et démarre le thread avec `.start()`. |
| **`send()`** | `self, message` | `None` | **Émission réseau :** formate le texte (ajoute le préfixe `<username>: ` si nécessaire), encode en octets UTF-8 et transmet le paquet via `self.socket.sendall()`. |
| **`tidy_up()`** | `self` | `None` | **Nettoyage :** met `self.listening` à `False` pour arrêter le thread d'écoute et ferme le socket avec `self.socket.close()`. |
| **`handle_msg()`** | `self, data` | `None` | **Traitement des messages reçus :** si le texte reçu est `"QUIT"` ou vide `""`, ferme la session avec `tidy_up()` ; sinon, affiche le message dans la console avec `print(data)`. |

### Attributs et Variables de `client.py`

| Nom | Portée / Scope | Type | Rôle et Utilité |
| :--- | :--- | :---: | :--- |
| **`self.socket`** | Attribut d'instance | `socket.socket` | Socket client connecté au serveur distant. |
| **`self.username`** | Attribut d'instance | `str` | Pseudo de l'utilisateur passé lors de l'instanciation. |
| **`self.listening`** | Attribut d'instance | `bool` | Drapeau de contrôle de la boucle d'écoute du client. |
| **`self.listen_thread`** | Attribut d'instance | `threading.Thread` | Le thread secondaire qui écoute les messages entrants sans bloquer la saisie clavier. |
| **`message`** | Paramètre de `send()` et variable locale à `__main__` | `str` | Texte saisi par l'utilisateur au clavier dans la console. |
| **`username_result`** | Variable locale à `send()` | `re.Match \| None` | Vérifie si le message à envoyer commence déjà par `USERNAME ` (évite de doubler le pseudo). |
| **`username`** | Variable globale (`__main__`) | `str` | Valeur récupérée par `input("username: ")`. |
| **`server`** | Variable globale (`__main__`) | `str` | Adresse IP ou nom d'hôte du serveur récupéré par `input("server: ")`. |
| **`port`** | Variable globale (`__main__`) | `int` | Port converti en entier via `int(input("port: "))`. |
| **`client`** | Variable globale (`__main__`) | `Client` | Instance du client instanciée et lancée dans le bloc principal. |

---

## 5. Tableau Synoptique de Cycle de Vie des Variables Réseau

| Action Réseau | Fichier émetteur | Variable manipulée | Fichier récepteur | Variable d'arrivée |
| :--- | :--- | :--- | :--- | :--- |
| **Connexion initiale** | `client.py` | `self.socket.connect((server, port))` | `server.py` | `(client_socket, client_adress) = self.listener.accept()` |
| **Envoi du Pseudo** | `client.py` | `self.send("USERNAME Alice")` | `clientthread.py` | `data = self.socket.recv(...)` $\rightarrow$ `self.username = "Alice"` |
| **Saisie d'un Message** | `client.py` | `message = input()` $\rightarrow$ `self.send(message)` | `clientthread.py` | `data = self.socket.recv(...)` |
| **Diffusion générale** | `clientthread.py` | `self.server.echo(data)` | `server.py` | `for sock in self.clients_sockets: sock.sendall(...)` |
| **Réception et affichage** | `server.py` | `sock.sendall(data.encode("UTF-8"))` | `client.py` | `data = self.socket.recv(...)` $\rightarrow$ `print(data)` |
| **Déconnexion** | `client.py` | `self.socket.close()` ou `"QUIT"` | `clientthread.py` | `if data == "": self.quit()` $\rightarrow$ `self.server.remove_socket()` |

---

## 6. Fiche Anti-Sèche pour la Soutenance Orale

Lors de votre présentation de 15 minutes avec **M. Cárdenas**, voici les 5 points techniques essentiels à maîtriser :

1. **`socket.AF_INET` vs `socket.SOCK_STREAM` :**
   - `AF_INET` = famille d'adresses **IPv4**.
   - `SOCK_STREAM` = protocole **TCP** (mode connecté, intégrité et ordre garantis).
2. **`bind()` vs `connect()` :**
   - `bind()` est réservé au **serveur** pour s'attacher à un port local et attendre des clients.
   - `connect()` est utilisé par le **client** pour initier la connexion vers le serveur.
3. **`sendall()` vs `send()` :**
   - `send()` n'envoie pas forcément tous les octets d'un coup si le tampon est plein.
   - `sendall()` boucle automatiquement jusqu'à ce que **l'intégralité** du message soit transmise.
4. **`encode("UTF-8")` et `decode("UTF-8")` :**
   - Les sockets ne transmettent que des **octets (`bytes`)**. Il est donc obligatoire de convertir le texte (`str`) en octets à l'envoi (`encode`), et de faire l'inverse à la réception (`decode`).
5. **Rôle du thread `daemon = True` dans `client.py` :**
   - Un thread classique bloque la fin d'un script Python.
   - Un thread *démon* est tué automatiquement dès que le thread principal (saisie clavier) se termine, évitant ainsi les processus zombies.
