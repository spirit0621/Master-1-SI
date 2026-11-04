materials = [
    {"name": "Switch-1", "status": "online"},
    {"name": "Switch-2", "status": "offline"},
    {"name": "Firewall", "status": "online"},
    {"name": "Server-dev", "status": "online"},
    {"name": "Server-Prod-1", "status": "online"},
    {"name": "Server-Prod-2", "status": "offline"},
    {"name": "Access-Point", "status": "offline"}
]

# Codes ANSI de couleur pour le terminal
VERT = "\033[32m"
FOND_ROUGE = "\033[41m"
RESET = "\033[0m"


def verifier_statut_equipements(equipements):
    print("Online machines :")
    for machine in equipements:
        nom = machine["name"]
        statut = machine["status"]
        
        # Choix de la couleur selon le statut
        if statut == "online":
            statut_affiche = f"{VERT}online{RESET}"
        else:
            statut_affiche = f"{FOND_ROUGE}offline{RESET}"
        print(f"- {nom} :  {statut_affiche}")
        
# Appel de la fonction avec la liste en paramètre
verifier_statut_equipements(materials)