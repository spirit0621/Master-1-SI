# 📄 Explication Détaillée du Code : `clientthread.py`

> **Projet :** TP Final Python - Chat Client / Serveur Multi-clients  
> **Niveau :** Master 1 SI - CFA INSTA  
> **Fichier analysé :** `clientthread.py`  
> **Rôle dans l'architecture :** Gestionnaire de flux asynchrone côté serveur (1 instance par client connecté)

---

## 📑 Sommaire

1. [Vue d'ensemble et Rôle de `clientthread.py`](#1-vue-densemble-et-rôle-de-clientthreadpy)
2. [Bibliothèques importées et leur utilité](#2-bibliothèques-importées-et-leur-utilité)
3. [Structure de la classe `ClientListener`](#3-structure-de-la-classe-clientlistener)
4. [Explication détaillée méthode par méthode](#4-explication-détaillée-méthode-par-méthode)
   - [Le Constructeur : `__init__(self, server, socket, address)`](#le-constructeur--__initself-server-socket-address)
   - [La Boucle de réception : `run(self)`](#la-boucle-de-réception--runself)
   - [L'Analyse des messages : `handle_msg(self, data)`](#lanalyse-des-messages--handle_msgself-data)
   - [La Fermeture de session : `quit(self)`](#la-fermeture-de-session--quitself)
5. [Le Pattern de Communication Thread-Serveur](#5-le-pattern-de-communication-thread-serveur)
6. [Points Clés & Questions Fréquentes pour la Soutenance](#6-points-clés--questions-fréquentes-pour-la-soutenance)

---

## 1. Vue d'ensemble et Rôle de `clientthread.py`

Le fichier `clientthread.py` contient la classe `ClientListener`.

Dans une architecture multi-utilisateurs, le serveur ne peut pas écouter les messages de chaque client dans sa boucle principale sans se bloquer. Dès qu'un nouveau client se connecte, le serveur instancie un `ClientListener` qui va vivre de manière **autonome dans son propre thread système**.

### Ses responsabilités :
- Écouter en continu les données envoyées par **un** client particulier.
- Parser (analyser) les commandes protocolaires (`USERNAME <nom>`, `QUIT`, messages normaux).
- Stocker l'identité de l'utilisateur (`self.username`).
- Prévenir le serveur lorsqu'un message doit être diffusé ou lorsqu'un client quitte la salle.

---

## 2. Bibliothèques importées et leur utilité

```python
from socket import socket as SocketType # Type hinting pour les sockets
import socket                           # Gestion des exceptions réseau
import threading                        # Module de threading Python
import re                               # Expressions régulières
import time                             # Temporisation pour le thread
```

- **`threading.Thread` :** `ClientListener` hérite directement de cette classe pour devenir un thread personnalisable avec sa propre méthode `run()`.
- **`re` :** Permet d'extraire le pseudo envoyé lors du handshake via l'expression régulière `^USERNAME (.*)$`.

---

## 3. Structure de la classe `ClientListener`

```python
class ClientListener(threading.Thread):
```

| Attribut | Type | Rôle |
| :--- | :--- | :--- |
| `self.server` | `Server` | Référence vers l'instance du serveur parent (permet d'invoquer `echo` et `remove_socket`). |
| `self.socket` | `socket.socket` | Le socket TCP dédié à ce client particulier. |
| `self.address` | `tuple` | Tuple contenant l'IP et le port éphémère du client (ex: `('127.0.0.1', 54321)`). |
| `self.listening` | `bool` | Booléen de contrôle pour maintenir ou stopper la boucle d'écoute. |
| `self.username` | `str` | Nom d'affichage de l'utilisateur (initialisé à `"Anonyme"`). |

---

## 4. Explication détaillée méthode par méthode

### Le Constructeur : `__init__(self, server, socket, address)`

```python
def __init__(self, server, client_socket: SocketType, address):
    super(ClientListener, self).__init__()
    self.server = server
    self.socket = client_socket
    self.address = address
    self.listening = True
    self.username = "Anonyme"
```

#### Ce qui s'y passe :
1. **`super().__init__()` :** Initialise la classe de base `threading.Thread` (étape obligatoire en Python quand on hérite de `Thread`).
2. **Conservation des références :** Stocke le lien vers le serveur parent (`self.server`) et le socket client.

---

### La Boucle de réception : `run(self)`

```python
def run(self):
    while self.listening:
        data = ""
        try:
            raw_bytes = self.socket.recv(1024)
            if not raw_bytes:
                break
            data = raw_bytes.decode('UTF-8')
        except (socket.error, ConnectionResetError):
            print(f"[AVERTISSEMENT] Perte de connexion inattendue avec {self.address}")
            break

        self.handle_msg(data)
        time.sleep(0.1)

    self.quit()
    print(f"[THREAD] Fermeture définitive du thread pour {self.address}")
```

#### Fonctionnement de la boucle :
1. **`self.socket.recv(1024)` :** Bloque le thread jusqu'à la réception de données réseau envoyées par ce client.
2. **Détection de fin de connexion (`if not raw_bytes:`) :**
   - En protocole TCP, si le socket distant ferme sa connexion, `recv()` retourne immédiatement un objet vide `b""`. C'est le signal universel de déconnexion. Le `break` permet de sortir de la boucle.
3. **Tolérance aux pannes (`except ConnectionResetError`) :**
   - Si l'utilisateur tue brutalement son terminal (fermeture brutale sans `QUIT`), Windows lève l'exception `ConnectionResetError: [WinError 10054] Une connexion existante a dû être fermée par l’hôte distant`.
   - Grâce au bloc `try / except`, le serveur **ne crashe pas** : l'erreur est interceptée et la session est nettoyée proprement.
4. **Sortie et nettoyage :** En sortant de la boucle, la méthode `self.quit()` est appelée pour libérer les ressources.

---

### L'Analyse des messages : `handle_msg(self, data)`

```python
def handle_msg(self, data: str):
    data_clean = data.strip()
    print(f"[{self.address} - {self.username}] : {data_clean}")

    username_result = re.search(r'^USERNAME (.*)$', data_clean)
    if username_result:
        self.username = username_result.group(1).strip()
        self.server.echo(f"*** {self.username} a rejoint le salon ! ***\n")
    elif data_clean == "QUIT" or data == "":
        self.quit()
    else:
        self.server.echo(data)
```

#### Traitement selon le contenu reçu :
1. **Enregistrement du pseudo (`USERNAME <pseudo>`) :**
   - Utilise une regex `^USERNAME (.*)$`.
   - Le groupe capturant `(1)` contient le pseudo.
   - Met à jour `self.username` et diffuse une alerte générale d'arrivée : `*** Alice a rejoint le salon ! ***`.
2. **Demande de déconnexion (`QUIT`) :**
   - Invoque immédiatement la méthode `self.quit()`.
3. **Message de chat ordinaire :**
   - Transmet le message à la méthode `self.server.echo()` pour qu'il soit diffusé à tous les autres utilisateurs.

---

### La Fermeture de session : `quit(self)`

```python
def quit(self):
    if not self.listening:
        return
    self.listening = False

    try:
        self.socket.close()
    except socket.error:
        pass

    self.server.remove_socket(self.socket)
    self.server.echo(f"*** {self.username} a quitté le salon. ***\n")
```

#### Actions réalisées :
1. **Anti-rebond :** Si `self.listening` est déjà à `False`, la fonction s'arrête (évite d'envoyer deux fois l'alerte de départ).
2. **Fermeture du socket :** Coupe la liaison réseau avec `self.socket.close()`.
3. **Retrait de la liste serveur :** Invoque `self.server.remove_socket(self.socket)` pour que le serveur ne tente plus de lui envoyer des données.
4. **Diffusion du départ :** Avertit tout le salon : `*** Alice a quitté le salon. ***`.

---

## 5. Le Pattern de Communication Thread-Serveur

Le fichier `clientthread.py` applique le patron de conception de **délégation bidirectionnelle** :

```text
       ┌──────────────────────────────────────────────┐
       │                 Server                       │
       │                                              │
       │  - Possède la liste des sockets              │
       │  - Possède la méthode echo()                 │
       │  - Possède la méthode remove_socket()        │
       └───────────────▲───────────────┬──────────────┘
                       │               │ Instancie et démarre
         Appelle       │               │ ClientListener(self, ...)
         echo() et     │               ▼
         remove_socket() ┌────────────────────────────┐
                       │       ClientListener         │
                       │       (Thread enfant)        │
                       │                              │
                       │  - Écoute ce client précis   │
                       │  - Gère l'état du client     │
                       └──────────────────────────────┘
```

Chaque thread enfant possède une référence directe vers le serveur (`self.server`), ce qui lui permet d'ordonner une diffusion globale (`self.server.echo`) dès qu'un message arrive.

---

## 6. Points Clés & Questions Fréquentes pour la Soutenance

### Q1 : Pourquoi faire hériter `ClientListener` de `threading.Thread` plutôt que d'utiliser `threading.Thread(target=...)` ?
> **Réponse :** L'approche par héritage orientée objet permet d'encapsuler l'état propre à chaque client (son socket, son adresse IP, son pseudonyme, son statut actif/inactif) et ses méthodes associées (`handle_msg`, `quit`) au sein d'une seule et même classe. C'est plus propre, plus modulaire et plus facile à maintenir que de multiples variables globales.

### Q2 : Que se passe-t-il si un client ferme brutalement son PC sans taper `QUIT` ?
> **Réponse :** Le socket TCP est rompu inopinément. Dès que le thread tente d'exécuter `recv()`, le système d'exploitation lève une exception `ConnectionResetError`. Si cette exception n'était pas gérée, le serveur ou le thread crasherait avec une trace d'erreur. Ici, le bloc `try / except` intercepte l'erreur, sort de la boucle d'écoute et exécute automatiquement la méthode `quit()` qui retire le socket de la liste et avertit les autres utilisateurs.

### Q3 : Pourquoi le thread se termine-t-il lorsque la méthode `run()` se termine ?
> **Réponse :** En Python, le cycle de vie d'un objet `threading.Thread` est directement lié à l'exécution de sa méthode `run()`. Dès que le flux d'instructions sort de la boucle `while self.listening` et atteint la fin du code de `run()`, le thread passe à l'état inactif (*dead*) et le ramasse-miettes (*Garbage Collector*) de Python libère la mémoire.

