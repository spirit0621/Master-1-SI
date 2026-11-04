ip = input("Entrez une adresse IP : ")
octets = ip.split(".")

if len(octets) != 4:
    print("IP non valide : il faut exactement 4 nombres.")
else:
    ip_valide = True

    for o in octets:
        if int(o) < 0 or int(o) > 255:
            ip_valide = False

    if ip_valide:
        print("L'IP est bonne !")
    else:
        print("IP non valide : les nombres doivent être entre 0 et 255.")