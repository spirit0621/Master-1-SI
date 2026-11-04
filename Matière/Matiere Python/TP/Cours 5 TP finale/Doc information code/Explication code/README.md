# 📚 Documentation Technique & Explication Détaillée du Code

> **Master 1 SI - CFA INSTA**  
> **TP Final Python :** Chat Client / Serveur Multi-utilisateurs  
> **Dossier :** Explications détaillées des composants du projet

---

Ce dossier contient les fiches d'explication complètes et pédagogiques pour chacun des fichiers sources du projet. Chaque fiche détaille le rôle du fichier, les bibliothèques utilisées, les classes, les attributs, l'explication méthode par méthode et les questions types pour la soutenance orale de 15 minutes avec M. Cárdenas.

---

### 📑 Fiches d'Explication Disponibles :

1. **[EXPLICATION_SERVER_PY.md](file:///c:/Users/alves/Desktop/Lyc%C3%A9e,%20bts%20,%20formation,%20master/CFA-insta/Master%20SI/Master%201%20SI/Mati%C3%A8re/Matiere%20Python/TP/Cours%205%20TP%20finale/Doc%20information%20code/Explication%20code/EXPLICATION_SERVER_PY.md)**
   - Rôle du serveur central TCP.
   - Sockets passifs (`listen`), attachement (`bind`), boucle d'acceptation (`accept`).
   - Gestion de la mémoire partagée des clients et mécanisme d'echo / broadcast.

2. **[EXPLICATION_CLIENTTHREAD_PY.md](file:///c:/Users/alves/Desktop/Lyc%C3%A9e,%20bts%20,%20formation,%20master/CFA-insta/Master%20SI/Master%201%20SI/Mati%C3%A8re/Matiere%20Python/TP/Cours%205%20TP%20finale/Doc%20information%20code/Explication%20code/EXPLICATION_CLIENTTHREAD_PY.md)**
   - Classe `ClientListener` héritant de `threading.Thread`.
   - Écoute asynchrone dédiée par client connecté.
   - Analyse des trames (`USERNAME`, `QUIT`) et tolérance aux déconnexions brutales (`ConnectionResetError`).

3. **[EXPLICATION_CLIENT_PY.md](file:///c:/Users/alves/Desktop/Lyc%C3%A9e,%20bts%20,%20formation,%20master/CFA-insta/Master%20SI/Master%201%20SI/Mati%C3%A8re/Matiere%20Python/TP/Cours%205%20TP%20finale/Doc%20information%20code/Explication%20code/EXPLICATION_CLIENT_PY.md)**
   - Client console interactif.
   - Connexion TCP active (`connect`).
   - Concurrence multithreadée : saisie clavier synchrone (`input`) et réception réseau asynchrone (`recv`).

