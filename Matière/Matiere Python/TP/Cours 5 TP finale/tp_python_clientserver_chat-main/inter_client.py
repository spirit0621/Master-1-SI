"""
Interface Graphique du Chat (Tkinter)
Fichier : inter_client.py
Ce fichier gère UNIQUEMENT l'affichage et l'interface utilisateur.
Il utilise la classe Client (définie dans client.py) pour la partie réseau.
"""

import tkinter as tk
from tkinter import scrolledtext
from client import Client

# Variable globale pour stocker l'objet client connecté
client = None


def action_connecter():
    """Se connecte au serveur et prépare l'affichage."""
    global client
    pseudo = champ_pseudo.get().strip() or "Alice"

    try:
        # On crée le Client en lui donnant notre fonction 'afficher_message' en callback
        client = Client(pseudo, "127.0.0.1", 59001, callback=afficher_message)
        client.listen()

        # Met à jour l'interface
        bouton_connecter.config(state=tk.DISABLED, text="Connecté ✅")
        champ_pseudo.config(state=tk.DISABLED)
        afficher_message(f"=== Vous êtes connecté en tant que {pseudo} ===")
    except Exception as err:
        afficher_message(f"❌ Erreur de connexion : {err}\n👉 Vérifiez que 'python server.py' est bien lancé !")


def action_envoyer():
    """Envoie le message saisi au serveur."""
    if client:
        texte = champ_saisie.get().strip()
        if texte:
            client.send(texte)
            champ_saisie.delete(0, tk.END)  # Vide la case de saisie


def afficher_message(texte):
    """Insère un message dans la zone de texte déroulante."""
    zone_chat.insert(tk.END, texte.strip() + "\n")
    zone_chat.see(tk.END)  # Fait défiler automatiquement vers le bas


def fermer_fenetre():
    """Ferme la connexion et détruit la fenêtre proprement."""
    if client:
        client.tidy_up()
    fenetre.destroy()


# =============================================================================
# CRÉATION DE L'INTERFACE GRAPHIQUE
# =============================================================================

fenetre = tk.Tk()
fenetre.title("Chat Client - Master 1 SI")
fenetre.geometry("420x520")
fenetre.protocol("WM_DELETE_WINDOW", fermer_fenetre)

# 1. Zone du haut : Pseudo et bouton Connexion
cadre_haut = tk.Frame(fenetre)
cadre_haut.pack(fill=tk.X, padx=5, pady=5)

tk.Label(cadre_haut, text="Pseudo :", font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT)
champ_pseudo = tk.Entry(cadre_haut, width=15)
champ_pseudo.insert(0, "Alice")
champ_pseudo.pack(side=tk.LEFT, padx=5)

bouton_connecter = tk.Button(cadre_haut, text="Se Connecter", bg="#4CAF50", fg="white",
                             font=("Segoe UI", 9, "bold"), command=action_connecter)
bouton_connecter.pack(side=tk.LEFT, padx=5)

# 2. Zone du milieu : Grande boîte de discussion
zone_chat = scrolledtext.ScrolledText(fenetre, font=("Segoe UI", 10), bg="#FAFAFA")
zone_chat.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

# 3. Zone du bas : Case pour taper et bouton Envoyer
champ_saisie = tk.Entry(fenetre, font=("Segoe UI", 10))
champ_saisie.pack(fill=tk.X, padx=5, pady=2)
champ_saisie.bind("<Return>", lambda e: action_envoyer())  # Envoi avec la touche Entrée
champ_saisie.focus()

bouton_envoyer = tk.Button(fenetre, text="Envoyer 📨", bg="#2196F3", fg="white",
                           font=("Segoe UI", 10, "bold"), command=action_envoyer)
bouton_envoyer.pack(fill=tk.X, padx=5, pady=2)

# Lancement de la boucle d'affichage
if __name__ == "__main__":
    fenetre.mainloop()
