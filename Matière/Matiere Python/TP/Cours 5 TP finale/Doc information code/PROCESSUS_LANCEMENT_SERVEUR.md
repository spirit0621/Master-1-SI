# 📘 Guide Technique : Processus de Lancement & Fonctionnement du Serveur et des Clients

> **Master 1 Systèmes d'Information - CFA INSTA**
> **Matière :** Programmation Python - Architecture Réseau
> **TP Final :** Chat Multi-clients (Sockets TCP & Multithreading)
> **Enseignant :** M. F. Cárdenas (`f.cardenas@cfa-insta.fr`)

---

## 📑 Sommaire

1. [Vue d&#39;ensemble de l&#39;Architecture](#1-vue-densemble-de-larchitecture)
2. [Arborescence et Emplacement des Scripts](#2-arborescence-et-emplacement-des-scripts)
3. [Étape 1 : Préparation de l&#39;Espace de Travail](#étape-1--préparation-de-lespace-de-travail)
4. [Étape 2 : Démarrage du Serveur (`server.py`)](#étape-2--démarrage-du-serveur-serverpy)
5. [Étape 3 : Connexion du Premier Client (`client.py`)](#étape-3--connexion-du-premier-client-clientpy)
6. [Étape 4 : Connexion d&#39;un Deuxième Client pour Tester le Chat](#étape-4--connexion-dun-deuxième-client-pour-tester-le-chat)
7. [Étape 5 : Cycle de Vie d&#39;un Message (Envoi &amp; Diffusion)](#étape-5--cycle-de-vie-dun-message-envoi--diffusion)
8. [Étape 6 : Procédure de Déconnexion Propre](#étape-6--procédure-de-déconnexion-propre)
9. [Guide de Dépannage (Troubleshooting &amp; Erreurs Fréquentes)](#guide-de-dépannage-troubleshooting--erreurs-fréquentes)
10. [Test en Réseau Local Réel (Entre plusieurs PC du CFA)](#test-en-réseau-local-réel-entre-plusieurs-pc-du-cfa)

---

## 1. Vue d'ensemble de l'Architecture

Le système repose sur un modèle **Client / Serveur en étoile** via le protocole **TCP** :

```text
       ┌────────────────────────────────────────────────────────┐
       │                   SERVEUR CENTRAL                      │
       │                   (Port TCP 59001)                     │
       │                                                        │
       │  - Accepte les nouvelles connexions (accept)           │
       │  - Crée un thread dédié par client (ClientListener)   │
       │  - Rediffuse (broadcast / echo) les messages à tous   │
       └───────────────────────────┬────────────────────────────┘
                                   │
         ┌─────────────────────────┼─────────────────────────┐
         │ Flux TCP                │ Flux TCP                │ Flux TCP
         ▼                         ▼                         ▼
┌──────────────────┐      ┌──────────────────┐      ┌──────────────────┐
│  Client 1        │      │  Client 2        │      │  Client 3        │
│  (ex: Alice)     │      │  (ex: Bob)       │      │  (ex: Charlie)   │
└──────────────────┘      └──────────────────┘      └──────────────────┘
```

- **Le Serveur** est **passif** : il écoute en permanence et centralise l'aiguillage des données.
- **Les Clients** sont **actifs** : ils initient la connexion, émettent des messages et les reçoivent en continu grâce à un thread d'écoute asynchrone.

---

## 2. Arborescence et Emplacement des Scripts

Suite à l'extraction de l'archive ZIP, les fichiers se trouvent dans le sous-dossier imbriqué suivant :

```text
C:\Users\alves\Desktop\Lycée, bts , formation, master\CFA-insta\Master SI\Master 1 SI\Matière\Matiere Python\TP\Cours 5 TP finale\
└── tp_python_clientserver_chat-main\
    └── tp_python_clientserver_chat-main\      <-- DOSSIER D'EXÉCUTION
        ├── server.py                          # Serveur TCP central
        ├── clientthread.py                    # Classe Thread de gestion d'un client
        ├── client.py                          # Client console
```

> ⚠️ **Règle essentielle sous Windows PowerShell :**
> Lorsque le chemin d'un dossier contient des espaces (ex: `Matiere Python`, `Cours 5 TP finale`), il faut **obligatoirement entourer le chemin de guillemets doubles `""`** lors de l'utilisation de la commande `cd`.

---

## Étape 1 : Préparation de l'Espace de Travail

Pour tester un chat multi-utilisateurs, vous avez besoin de faire tourner **plusieurs processus simultanément** :

- **1 terminal pour le Serveur**
- **1 terminal pour le Client 1**
- **1 terminal pour le Client 2**

### Comment ouvrir plusieurs terminaux dans VS Code :

1. Ouvrez le terminal avec **`Ctrl + ù`** (ou menu *Terminal > Nouveau terminal*).
2. Pour ouvrir un terminal supplémentaire, cliquez sur l'icône **`+`** (ou l'icône de scission de fenêtre) située en haut à droite du panneau de terminal.
3. Vous pouvez basculer d'un terminal à l'autre via la liste déroulante sur le côté droit du panneau.

---

## Étape 2 : Démarrage du Serveur (`server.py`)

Dans votre **premier terminal (Terminal 1 - Serveur)** :

### 1. Se positionner dans le dossier des scripts

```powershell
cd "C:\Users\alves\Desktop\Lycée, bts , formation, master\CFA-insta\Master SI\Master 1 SI\Matière\Matiere Python\TP\Cours 5 TP finale\tp_python_clientserver_chat-main\tp_python_clientserver_chat-main"
```

### 2. Lancer le script du serveur

```powershell
python server.py
```

*(ou `python serveur.py`)*

### 3. Résultat attendu dans la console :

```text
==================================================
   LANCEMENT DU SERVEUR DE CHAT (PYTHON)
==================================================
[SERVEUR] En écoute sur le port 59001...
[SERVEUR] En attente de nouveaux clients...
```

> 🟢 **Le serveur est prêt et actif.** Laissez cette fenêtre ouverte sans y toucher : le serveur attend les connexions entrantes.

---

## Étape 3 : Connexion du Premier Client (`client.py`)

Basculez sur votre **deuxième terminal (Terminal 2 - Client 1)** :

### 1. Se positionner dans le même dossier

```powershell
cd "C:\Users\alves\Desktop\Lycée, bts , formation, master\CFA-insta\Master SI\Master 1 SI\Matière\Matiere Python\TP\Cours 5 TP finale\tp_python_clientserver_chat-main\tp_python_clientserver_chat-main"
```

### 2. Lancer le script client

```powershell
python client.py
```

### 3. Renseigner les paramètres demandés :

```text
==================================================
        CLIENT DE CHAT (CONSOLE)
==================================================
Entrez votre pseudo : Alice
Adresse du serveur [défaut: 127.0.0.1] : [Appuyez sur Entrée]
Port du serveur [défaut: 59001] : [Appuyez sur Entrée]
```

### 4. Résultat attendu :

- **Dans le terminal d'Alice (Client 1) :**
  ```text
  [CONNEXION] Tentative de connexion à 127.0.0.1:59001...
  [SUCCÈS] Connecté au serveur avec le pseudo 'Alice'.

  --- Vous êtes dans le salon (tapez 'QUIT' pour quitter) ---
  *** Alice a rejoint le salon ! ***
  ```
- **Dans le terminal du Serveur :**
  ```text
  [CONNEXION] Nouveau client connecté depuis ('127.0.0.1', 54321)
  [SERVEUR] En attente de nouveaux clients...
  [127.0.0.1:54321 - Anonyme] : USERNAME Alice
  [DIFFUSION] *** Alice a rejoint le salon ! ***
  ```

---

## Étape 4 : Connexion d'un Deuxième Client pour Tester le Chat

Ouvrez un **troisième terminal (Terminal 3 - Client 2)** pour simuler un autre participant :

### 1. Navigation et lancement

```powershell
cd "C:\Users\alves\Desktop\Lycée, bts , formation, master\CFA-insta\Master SI\Master 1 SI\Matière\Matiere Python\TP\Cours 5 TP finale\tp_python_clientserver_chat-main\tp_python_clientserver_chat-main"
python client.py
```

### 2. Saisie des informations de Bob :

```text
Entrez votre pseudo : Bob
Adresse du serveur [défaut: 127.0.0.1] : [Entrée]
Port du serveur [défaut: 59001] : [Entrée]
```

### 3. Synchronisation immédiate :

- **Dans le terminal de Bob :** Il voit `*** Bob a rejoint le salon ! ***`.
- **Dans le terminal d'Alice :** Elle reçoit instantanément `*** Bob a rejoint le salon ! ***`.
- **Dans le terminal du Serveur :** Le serveur trace la connexion de Bob et démarre un deuxième thread `ClientListener`.

---

## Étape 5 : Cycle de Vie d'un Message (Envoi & Diffusion)

### Scénario de test :

1. Dans le **Terminal 2 (Alice)**, tapez :

   ```text
   Salut Bob, tu m'entends ?
   ```

   Puis appuyez sur **Entrée**.
2. **Que se passe-t-il techniquement ?**

   - Le client d'Alice encode le texte en UTF-8 et l'envoie sur le socket TCP :`Alice: Salut Bob, tu m'entends ?`
   - Le thread serveur dédié à Alice reçoit les octets via `socket.recv(1024)`.
   - La méthode `server.echo()` parcourt la liste `self.clients_sockets` et diffuse le message à **tous les clients connectés** (Alice et Bob).
   - Le thread d'écoute de Bob (`listen_thread`) reçoit le message et l'affiche à l'écran.
3. **Dans le Terminal 3 (Bob) :**

   ```text
   Alice: Salut Bob, tu m'entends ?
   ```
4. Bob peut répondre :

   ```text
   Oui Alice, le chat fonctionne parfaitement !
   ```

---

## Étape 6 : Procédure de Déconnexion Propre

Pour quitter le salon sans générer d'erreurs ni de sockets "fantômes" :

1. Dans le terminal du client (ex: Bob), tapez :

   ```text
   QUIT
   ```

   Puis appuyez sur **Entrée**.
2. **Actions déclenchées :**

   - Le client coupe sa boucle d'écoute et ferme son socket : `socket.close()`.
   - Le serveur intercepte la fin de connexion, retire le socket de sa liste (`self.remove_socket()`).
   - Le serveur diffuse à tous les membres restants :
     ```text
     *** Bob a quitté le salon. ***
     ```
   - Le thread serveur associé à Bob se termine proprement :
     ```text
     [THREAD] Fermeture définitive du thread pour ('127.0.0.1', ...)
     ```

---

## Guide de Dépannage (Troubleshooting & Erreurs Fréquentes)

| Erreur Constatée                                                                                      | Cause Fréquente                                                                                        | Solution Immédiate                                                                                                               |
| :----------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------ | :-------------------------------------------------------------------------------------------------------------------------------- |
| **`[Errno 2] No such file or directory`**                                                      | Le terminal n'est pas dans le bon sous-dossier contenant les scripts.                                   | Taper `cd tp_python_clientserver_chat-main` ou vérifier l'arborescence avec la commande `dir`.                               |
| **`Impossible de trouver un paramètre positionnel acceptant l'argument « Python »`**        | Commande `cd Matiere Python` tapée sans guillemets dans PowerShell.                                  | Toujours entourer le chemin de guillemets : `cd "Matiere Python"`.                                                              |
| **`[Errno 10048] Only one usage of each socket address is normally permitted`**                | Une ancienne instance de `server.py` tourne déjà en arrière-plan sur le port 59001.                | Fermer le terminal où tournait l'ancien serveur avec `Ctrl + C`, ou tuer les processus Python via le Gestionnaire des tâches. |
| **`[Errno 10061] No connection could be made because the target machine actively refused it`** | Le client essaie de se connecter alors que le serveur n'est pas encore lancé ou est sur un autre port. | Lancer d'abord `python server.py` dans le Terminal 1, puis relancer `client.py`.                                              |

---

## Test en Réseau Local Réel (Entre plusieurs PC du CFA)

Pour la démonstration demandée par M. Cárdenas (1 machine serveur-client + 2 machines clientes) :

1. **Sur la machine Serveur :**

   - Ouvrez un terminal PowerShell et trouvez l'adresse IP locale du PC sur le réseau du CFA :
     ```powershell
     ipconfig
     ```
   - Repérez la ligne **`Adresse IPv4`** (ex: `192.168.1.45` ou `10.x.x.x`).
   - Lancez le serveur : `python server.py`.
2. **Sur les deux autres machines clientes (Binômes) :**

   - Assurez-vous que les 3 PC sont connectés au **même réseau Wi-Fi / Ethernet**.
   - Lancez `python client.py`.
   - À l'invite `Adresse du serveur :`, saisissez l'adresse IPv4 de la machine Serveur (ex: `192.168.1.45`).
   - Saisissez le port : `59001`.
   - La communication s'établit à travers le réseau local !
