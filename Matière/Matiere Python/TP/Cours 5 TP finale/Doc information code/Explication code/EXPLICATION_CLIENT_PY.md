# 📄 Explication Détaillée du Code : `client.py`

> **Projet :** TP Final Python - Chat Client / Serveur Multi-clients  
> **Niveau :** Master 1 SI - CFA INSTA  
> **Fichier analysé :** `client.py`  
> **Rôle dans l'architecture :** Interface en ligne de commande (CLI) côté utilisateur

---

## 📑 Sommaire

1. [Vue d'ensemble et Rôle de `client.py`](#1-vue-densemble-et-rôle-de-clientpy)
2. [Bibliothèques importées et leur utilité](#2-bibliothèques-importées-et-leur-utilité)
3. [Structure de la classe `Client`](#3-structure-de-la-classe-client)
4. [Explication détaillée méthode par méthode](#4-explication-détaillée-méthode-par-méthode)
   - [Le Constructeur : `__init__(self, username, server, port)`](#le-constructeur--__initself-username-server-port)
   - [Le Thread d'écoute : `listen(self)` et `listener(self)`](#le-thread-découte--listenself-et-listenerself)
   - [L'Envoi de messages : `send(self, message)`](#lenvoi-de-messages--sendself-message)
   - [Le Traitement des réceptions : `handle_msg(self, data)`](#le-traitement-des-réceptions--handle_msgself-data)
   - [La Fermeture propre : `tidy_up(self)`](#la-fermeture-propre--tidy_upself)
5. [Le Bloc d'Exécution Principal (`__main__`)](#5-le-bloc-dexécution-principal-__main__)
6. [Points Clés & Questions Fréquentes pour la Soutenance](#6-points-clés--questions-fréquentes-pour-la-soutenance)

---

## 1. Vue d'ensemble et Rôle de `client.py`

Le fichier `client.py` est le point d'entrée exécuté par chaque utilisateur souhaitant rejoindre le chat.

### Ses responsabilités :
- Établir une connexion réseau fiable via le protocole **TCP** vers l'adresse IP et le port du serveur.
- S'identifier auprès du serveur avec un pseudonyme (protocole `USERNAME <pseudo>`).
- **Gérer la concurrence** : être capable d'écouter et d'afficher les messages des autres participants en continu, tout en attendant que l'utilisateur tape un message au clavier sans se bloquer.

---

## 2. Bibliothèques importées et leur utilité

```python
import threading  # Gestion des threads pour l'écoute asynchrone
import socket     # Communication réseau bas niveau (TCP/IP)
import time       # Temporisation pour soulager le processeur
import re         # Expressions régulières pour analyser les formats de commande
import sys        # Gestion de l'arrêt du programme et des flux système
```

- **`socket` :** Fournit l'accès aux interfaces réseau du système d'exploitation. C'est le tunnel de communication.
- **`threading` :** Permet de créer un fil d'exécution séparé. `input()` et `recv()` sont toutes deux des fonctions **bloquantes**. Sans threads, le programme ne pourrait pas recevoir de message tant que l'utilisateur n'a pas tapé sur Entrée !
- **`re` :** Utilisé pour vérifier si le message tapé commence par la commande spéciale `USERNAME` afin d'éviter les doublons de préfixes.

---

## 3. Structure de la classe `Client`

La classe `Client` regroupe l'état et le comportement d'une session de chat pour un utilisateur :

| Attribut | Type | Rôle |
| :--- | :--- | :--- |
| `self.socket` | `socket.socket` | Le socket TCP connecté au serveur distant. |
| `self.username` | `str` | Le pseudonyme choisi par l'utilisateur (ex: `"Alice"`). |
| `self.listening` | `bool` | Drapeau booléen (*flag*) contrôlant la boucle d'écoute du thread. |
| `self.listen_thread` | `threading.Thread` | Le thread secondaire dédié à la réception des messages. |

---

## 4. Explication détaillée méthode par méthode

### Le Constructeur : `__init__(self, username, server, port)`

```python
def __init__(self, username: str, server_host: str, server_port: int):
    self.username = username
    self.listening = True

    try:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((server_host, server_port))
    except socket.error as err:
        sys.exit(f"[ERREUR] Impossible de joindre le serveur ({err}).")

    self.send(f"USERNAME {username}")
```

#### Ce qui s'y passe :
1. **Création du socket :**
   - `socket.AF_INET` : Indique l'utilisation de la famille d'adresses **IPv4**.
   - `socket.SOCK_STREAM` : Indique le protocole **TCP** (mode connecté, livraison ordonnée et garantie sans perte).
2. **Connexion au serveur (`connect`) :**
   - Déclenche la poignée de main TCP (*Three-way handshake* : SYN, SYN-ACK, ACK) avec la machine distante.
   - En cas d'échec (serveur éteint, mauvaise IP, mauvais port), l'exception est capturée et le programme s'arrête avec un message d'erreur clair.
3. **Handshake applicatif :**
   - Dès la connexion réussie, le client envoie automatiquement `USERNAME <pseudo>` au serveur pour s'enregistrer.

---

### Le Thread d'écoute : `listen(self)` et `listener(self)`

#### 1. Méthode `listen(self)` :
```python
def listen(self):
    self.listen_thread = threading.Thread(target=self.listener, daemon=True)
    self.listen_thread.start()
```
- Crée un nouveau thread avec `target=self.listener`.
- `daemon=True` : Indique que ce thread est un thread d'arrière-plan. Si le thread principal (la saisie clavier) se termine, le thread d'écoute sera automatiquement détruit par Python sans bloquer le terminal.
- `start()` : Déclenche l'exécution en parallèle de la méthode `listener`.

#### 2. Méthode `listener(self)` :
```python
def listener(self):
    while self.listening:
        data = ""
        try:
            raw_bytes = self.socket.recv(1024)
            if not raw_bytes:
                break
            data = raw_bytes.decode('UTF-8')
        except (socket.error, ConnectionResetError):
            break

        self.handle_msg(data)
        time.sleep(0.1)

    self.tidy_up()
```
- **`self.socket.recv(1024)` :** Attend de recevoir jusqu'à 1024 octets en provenance du serveur. Cette opération est bloquante pour ce thread mais **n'affecte pas** le thread principal.
- **`if not raw_bytes:` :** En programmation socket TCP, si `recv()` renvoie 0 octet (`b""`), cela indique formellement que **le serveur a fermé la connexion**.
- **`.decode('UTF-8')` :** Reconvertit les octets reçus du réseau en chaîne de caractères Unicode lisible.
- **`time.sleep(0.1)` :** Évite de saturer inutilement le CPU en cas de boucle rapide.

---

### L'Envoi de messages : `send(self, message)`

```python
def send(self, message: str):
    try:
        username_result = re.search(r'^USERNAME (.*)$', message)
        if not username_result:
            message = f"{self.username}: {message}"
        self.socket.sendall(message.encode("UTF-8"))
    except socket.error:
        print("[ERREUR] Échec de l'envoi du message au serveur.")
```

#### Ce qui s'y passe :
1. **Formatage automatique :** Si le message n'est pas une commande système interne (`USERNAME`), le script ajoute automatiquement le pseudo de l'auteur en préfixe : `Alice: Bonjour tout le monde`.
2. **`message.encode("UTF-8")` :** Les sockets ne transportent que des octets bruts (*bytes*). La chaîne texte doit donc être encodée en binaire.
3. **`sendall()` :** Contrairement à `send()` qui peut n'envoyer qu'une portion des données si le tampon réseau est plein, `sendall()` continue d'émettre jusqu'à ce que la totalité des octets ait été transmise.

---

### Le Traitement des réceptions : `handle_msg(self, data)`

```python
def handle_msg(self, data: str):
    if data.strip() == "QUIT" or data == "":
        self.tidy_up()
    else:
        print(data.strip())
```
- Si le serveur envoie un signal de fermeture (`QUIT` ou chaîne vide), le client lance la procédure de déconnexion.
- Sinon, le message formaté reçu est affiché à l'écran dans la console.

---

### La Fermeture propre : `tidy_up(self)`

```python
def tidy_up(self):
    self.listening = False
    try:
        self.socket.close()
    except socket.error:
        pass
```
- Bascule le booléen `self.listening` à `False` pour stopper la boucle `while`.
- Ferme le socket TCP avec `socket.close()` pour libérer le port côté système d'exploitation.

---

## 5. Le Bloc d'Exécution Principal (`__main__`)

```python
if __name__ == "__main__":
    username_input = input("Entrez votre pseudo : ").strip()
    server_input = input("Adresse du serveur [défaut: 127.0.0.1] : ").strip() or "127.0.0.1"
    port_num = 59001

    client = Client(username_input, server_input, port_num)
    client.listen()

    message = ""
    while message != "QUIT":
        message = input()
        if message.strip():
            client.send(message)

    client.tidy_up()
```

### Fonctionnement de la boucle utilisateur :
1. Le programme demande les paramètres de connexion à l'utilisateur.
2. L'objet `Client` est instancié et son thread d'écoute est démarré.
3. Le fil principal entre dans une boucle infinie attendant les saisies clavier (`input()`).
4. Tant que l'utilisateur n'écrit pas `QUIT`, chaque ligne tapée est envoyée au serveur via `client.send()`.
5. Si `QUIT` est tapé, la boucle se termine et la méthode `tidy_up()` ferme la session.

---

## 6. Points Clés & Questions Fréquentes pour la Soutenance

### Q1 : Pourquoi a-t-on besoin de la bibliothèque `threading` dans `client.py` ?
> **Réponse :** Dans un programme console classique à un seul fil d'exécution, la fonction `input()` bloque le programme jusqu'à ce que l'utilisateur tape sur Entrée, et la fonction `socket.recv()` bloque jusqu'à ce qu'un paquet arrive du réseau. Sans `threading`, le client serait incapable d'afficher un message envoyé par un ami tant qu'il n'a pas lui-même écrit un message ! Le thread secondaire permet une écoute réseau permanente et asynchrone.

### Q2 : Quelle est la différence entre `.encode()` et `.decode()` ?
> **Réponse :** `.encode('UTF-8')` transforme une chaîne de caractères Python (`str`) en octets (`bytes`) compréhensibles par la carte réseau. `.decode('UTF-8')` effectue l'opération inverse lorsqu'on lit les octets bruts reçus du socket pour les transformer en texte affichable.

### Q3 : Pourquoi définir le thread en mode `daemon = True` ?
> **Réponse :** Un thread standard (*non-daemon*) empêche le processus Python de se terminer tant qu'il est actif. En passant le thread en `daemon=True`, on s'assure que si l'utilisateur quitte le programme principal (ex: `Ctrl + C` ou fin de `__main__`), le thread d'écoute sera immédiatement détruit sans laisser de processus zombie en arrière-plan.

