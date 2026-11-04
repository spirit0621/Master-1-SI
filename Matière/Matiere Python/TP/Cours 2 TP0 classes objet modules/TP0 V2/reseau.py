def valider_ip(ip):
    octets = ip.split(".")
    if len(octets) != 4:
        return False
    for o in octets:
        if int(o) < 0 or int(o) > 255:
            return False
    return True