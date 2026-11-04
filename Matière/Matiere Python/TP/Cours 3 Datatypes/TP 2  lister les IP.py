import ipaddress
# 1. La fonction pour demander et vérifier la saisie
def get_ip(msg):
    while True:
        try:
            return ipaddress.ip_address(input(msg).strip())
        except ValueError:
            print("IP invalide, réessayez.")

# 2. Programme principal
ip_deb = get_ip("Entrez l'IP de debut :")
ip_fin = get_ip("Entrez l'IP de fin : ")

# 3.1. Boucle pour afficher les IPs
# for ip in range(int(ip_deb), int(ip_fin) + 1):
#    print(ipaddress.ip_address(ip))

# 3.2 Boucle pour afficher les IPs
def listIP(IP1, IP2):
    while IP1 <= IP2:
        print(IP1)
        IP1 = IP1 + 1

listIP(ip_deb, ip_fin)