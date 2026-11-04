import speedtest

st = speedtest.Speedtest()

# Configuration et informations du client
config = st.get_config()
client = config["client"]

# Selection du serveur
serveur = st.get_best_server()

# Informations du reseau
ip = client["ip"]
fai = client["isp"]

# Mesures de connexion
ping = st.results.ping
download = st.download() / 1_000_000
upload = st.upload() / 1_000_000

# Affichage du rapport
print("========================================")
print("             RAPPORT D'AUDIT")
print("========================================")

print("Operateur / FAI :", fai)
print("Adresse IP publique :", ip)

print("\nINFORMATIONS DU SERVEUR")
print("Nom :", serveur["name"])
print("Fournisseur :", serveur["sponsor"])
print("Pays :", serveur["country"])
print("Latence :", round(serveur["latency"], 2), "ms")

print("\nRESULTATS DU TEST")
print("Ping :", round(ping, 2), "ms")
print("Download :", round(download, 2), "Mbit/s")
print("Upload :", round(upload, 2), "Mbit/s")

print("========================================")
print("             TEST TERMINE")
print("========================================")