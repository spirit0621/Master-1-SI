from reseau import valider_ip

ip = input("Entrez une IP : ")
if valider_ip(ip):
    print("IP valide !")
else:
    print("IP invalide !")