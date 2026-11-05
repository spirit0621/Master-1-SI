"""
Ce module gère la réception et l'analyse des messages envoyés par un client.
"""
from socket import socket
import threading 
#Il fournit la classe Thread dont hérite ClientListener pour s'exécuter en tâche de fond en parallèle du serveur.
import re 
import time

#Thread, chaque instance devient un thread à part entière, dont le code s'exécutera lors de l'appel à .start().
#server : L'objet Server parent (pour pouvoir appeler ses méthodes echo et remove_socket).
#socket : Le socket TCP dédié à ce client.
#address : Le tuple (IP, Port) du client.
class ClientListener(threading.Thread):

    def __init__(self, server, socket, address):
        super(ClientListener, self).__init__()
        self.server= server
        self.socket= socket
        self.address= address
        self.listening= True
        self.username= "No username"

#Boucle d'Écoute du Thread
    def run(self):
        while self.listening:
            data= ""
            try:
                data = self.socket.recv(1024).decode('UTF-8')
            except socket.error:
                print("Unable to receive data")
            self.handle_msg(data)
            time.sleep(0.1)
        print("Ending client thread for", self.address)
 
 #Procédure de Déconnexion Propre : quit()
    def quit(self):
        self.listening = False
        self.socket.close()
        self.server.remove_socket(self.socket)
        self.server.echo("{0} has quit\n".format(self.username))

#Analyse et Routage du Message :
#Diffuse à tout le chat l'annonce d'arrivée
    def handle_msg(self, data):
        print(self.address, "sent :", data)
        username_result = re.search('^USERNAME (.*)$', data)
        if username_result:
            self.username = username_result.group(1)
            self.server.echo("{0} has joined.\n".format(self.username))
        elif data == "QUIT":
            self.quit()
        elif data == "":
            self.quit()
        else:
            self.server.echo(data)
