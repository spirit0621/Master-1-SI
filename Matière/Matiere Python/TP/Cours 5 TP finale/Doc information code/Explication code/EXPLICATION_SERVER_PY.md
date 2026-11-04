# 📄 Explication Détaillée du Code : `server.py`

> **Projet :** TP Final Python - Chat Client / Serveur Multi-clients  
> **Niveau :** Master 1 SI - CFA INSTA  
> **Fichier analysé :** `server.py`  
> **Rôle dans l'architecture :** Nœud central (Hôte), gestionnaire d'écoute TCP et aiguilleur de messages

---

## 📑 Sommaire

1. [Vue d'ensemble et Rôle de `server.py`](#1-vue-densemble-et-rôle-de-serverpy)
2. [Bibliothèques importées et leur utilité](#2-bibliothèques-importées-et-leur-utilité)
3. [Structure de la classe `Server`](#3-structure-de-la-classe-server)
4. [Explication détaillée méthode par méthode](#4-explication-détaillée-méthode-par-méthode)
   - [Le Constructeur : `__init__(self, port)`](#le-constructeur--__initself-port)
   - [La Boucle d'acceptation : `run(self)`](#la-boucle-dacceptation--runself)
   - [La Gestion des départs : `remove_socket(self, sock)`](#la-gestion-des-départs--remove_socketself-sock)
   - [La Diffusion collective : `echo(self, data)`](#la-diffusion-collective--echoself-data)
5. [Le Bloc d'Exécution Principal (`__main__`)](#5-le-bloc-dexécution-principal-__main__)
6. [Points Clés & Questions Fréquentes pour la Soutenance](#6-points-clés--questions-fréquentes-pour-la-soutenance)

---

## 1. Vue d'ensemble et Rôle de `server.py`

Le fichier `server.py` constitue le cœur névralgique de l'application de messagerie.

### Ses responsabilités :
- Ouvrir un port d'écoute TCP sur la machine hôte et attendre les demandes de connexion des clients.
- Accepter chaque client entrant et lui allouer immédiatement un **thread dédié** (`ClientListener`) pour ne pas bloquer l'arrivée d'autres clients.
- Maintenir le registre des clients actuellement en ligne (`self.clients_sockets`).
- Diffuser chaque message reçu à **l'ensemble des clients connectés** (mécanisme de *Broadcast* / *Echo*).

---

## 2. Bibliothèques importées et leur utilité

```python
import socket                         # Gestion des sockets TCP/IP
import sys                            # Sortie du programme en cas d'erreur fatale
import time                           # Temporisation de boucle
from clientthread import ClientListener # Import de la classe gérant chaque client dans un thread
```

- **`socket` :** Permet de créer la prise d'écoute réseau serveur (`socket.socket`) et d'interagir avec la couche transport TCP.
- **`sys` :** Fournit `sys.exit()` pour stopper proprement le script si le port est inaccessible ou si une erreur critique survient.
- **`ClientListener` :** Classe fille de `threading.Thread` définie dans `clientthread.py`. Le serveur délègue à cette classe la gestion de chaque client dès qu'il est accepté.

---

## 3. Structure de la classe `Server`

| Attribut | Type | Rôle |
| :--- | :--- | :--- |
| `self.listener` | `socket.socket` | Le socket serveur principal configuré en mode écoute passive (*Passive Socket*). |
| `self.clients_sockets` | `list[socket.socket]` | Liste dynamique contenant les sockets de tous les clients connectés en temps réel. |

---

## 4. Explication détaillée méthode par méthode

### Le Constructeur : `__init__(self, port)`

```python
def __init__(self, port: int):
    self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self.listener.bind(('', port))
    self.listener.listen(5)
    print(f"[SERVEUR] En écoute sur le port {port}...")
    self.clients_sockets = []
```

#### Ce qui s'y passe étape par étape :
1. **Création du socket :**
   - `AF_INET` : Famille d'adresses IPv4.
   - `SOCK_STREAM` : Protocole orienté connexion **TCP**.
2. **`setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)` :**
   - **Crucial en production :** Cette option ordonne au système d'exploitation de libérer immédiatement l'adresse et le port dès l'arrêt du script, évitant l'erreur courante `Address already in use` (état `TIME_WAIT` de TCP).
3. **`bind(('', port))` :**
   - Associe le socket à une interface réseau et un port.
   - La chaîne vide `''` (équivalente à `0.0.0.0`) signifie que le serveur écoute sur **toutes les cartes réseau de la machine** (boucle locale `127.0.0.1`, Wi-Fi, Ethernet).
4. **`listen(5)` :**
   - Fait basculer le socket de l'état actif vers l'état passif (*Listening*).
   - Le paramètre `5` définit la taille du *backlog*, c'est-à-dire le nombre maximum de connexions clientes simultanées en attente d'être traitées par `accept()`.
5. **Initialisation de la liste des clients :**
   - `self.clients_sockets = []` initialise la mémoire partagée des utilisateurs actifs.

---

### La Boucle d'acceptation : `run(self)`

```python
def run(self):
    while True:
        print("[SERVEUR] En attente de nouveaux clients...")
        try:
            (client_socket, client_address) = self.listener.accept()
        except socket.error as err:
            sys.exit(f"[ERREUR CRITIQUE] Impossible d'accepter la connexion : {err}")

        self.clients_sockets.append(client_socket)
        print(f"[CONNEXION] Nouveau client connecté depuis {client_address}")

        client_thread = ClientListener(self, client_socket, client_address)
        client_thread.start()
        time.sleep(0.1)
```

#### Fonctionnement de la boucle :
1. **`self.listener.accept()` :**
   - C'est un appel **bloquant** : le programme s'arrête sur cette ligne tant qu'aucun client ne demande de connexion.
   - Lorsqu'un client arrive, `accept()` retourne un tuple composé de :
     - `client_socket` : un **nouveau socket dédié** à la communication avec ce client particulier (laissant `self.listener` libre pour continuer à écouter).
     - `client_address` : l'adresse IP et le port éphémère du client (ex: `('192.168.1.15', 54210)`).
2. **Enregistrement :** Le nouveau socket est ajouté à la liste `self.clients_sockets`.
3. **Délégation multithread :**
   - Un objet `ClientListener` est créé en lui passant la référence du serveur (`self`), le socket du client et son adresse.
   - `client_thread.start()` lance immédiatement le nouveau thread en parallèle.
4. **Reprise de l'écoute :** Le serveur revient immédiatement au début de la boucle `while True` pour accueillir le client suivant sans faire la queue.

---

### La Gestion des départs : `remove_socket(self, sock)`

```python
def remove_socket(self, sock: socket.socket):
    if sock in self.clients_sockets:
        self.clients_sockets.remove(sock)
```
- Appelée par `ClientListener` lorsqu'un utilisateur tape `QUIT` ou coupe sa fenêtre.
- Retire le socket de la liste pour ne plus tenter de lui envoyer des messages à l'avenir.

---

### La Diffusion collective : `echo(self, data)`

```python
def echo(self, data: str):
    print(f"[DIFFUSION] {data.strip()}")
    for sock in list(self.clients_sockets):
        try:
            sock.sendall(data.encode("UTF-8"))
        except socket.error:
            print("[ERREUR] Échec de l'envoi du message à un client déconnecté.")
            self.remove_socket(sock)
```

#### Ce qui s'y passe :
1. **Diffusion générale :** Parcourt tous les sockets clients actifs et leur transmet le message encodé en UTF-8 via `sendall()`.
2. **Robustesse & copie de liste (`list(...)`) :**
   - On itère sur une copie `list(self.clients_sockets)`. En Python, modifier une liste (ex: faire un `.remove()`) pendant qu'on boucle dessus provoque des comportements imprévisibles. La copie sécurise l'opération.
3. **Nettoyage automatique :** Si `sock.sendall()` échoue (ex: client qui a coupé son câble réseau), le socket défaillant est immédiatement supprimé de la liste.

---

## 5. Le Bloc d'Exécution Principal (`__main__`)

```python
if __name__ == "__main__":
    PORT_PAR_DEFAUT = 59001
    server = Server(PORT_PAR_DEFAUT)
    server.run()
```
- Définit le port standard d'écoute (`59001`).
- Instancie l'objet `Server` et démarre sa boucle infinie avec `run()`.

---

## 6. Points Clés & Questions Fréquentes pour la Soutenance

### Q1 : Pourquoi `accept()` retourne-t-il un nouveau socket au lieu d'utiliser le socket `listener` ?
> **Réponse :** Le socket `listener` est configuré pour écouter passivement sur le port 59001. Si le serveur utilisait ce même socket pour discuter avec un client, il ne pourrait plus recevoir d'autres connexions. `accept()` crée donc un socket dédié avec une liaison unique (IP serveur, Port serveur, IP client, Port client), ce qui permet à `listener` de rester disponible pour de futurs clients.

### Q2 : Que signifie l'adresse IP `''` passée à la méthode `bind()` ?
> **Réponse :** Passer une chaîne vide `''` correspond à l'adresse générique `INADDR_ANY` (`0.0.0.0`). Cela indique au système d'exploitation que le serveur accepte les connexions entrantes sur **toutes les interfaces réseau de la machine** (boucle locale `127.0.0.1` ainsi que l'adresse IP locale Wi-Fi/Ethernet).

### Q3 : Pourquoi itérer sur `list(self.clients_sockets)` dans `echo()` au lieu de `self.clients_sockets` directement ?
> **Réponse :** Si un client vient de se déconnecter brusquement, la méthode `sendall()` va lever une exception et appeler `self.remove_socket(sock)`. En Python, modifier la taille d'une liste pendant qu'on la parcourt engendre des sauts d'index ou des erreurs d'itération. Créer une copie avec `list(...)` permet de parcourir la liste en toute sécurité.

