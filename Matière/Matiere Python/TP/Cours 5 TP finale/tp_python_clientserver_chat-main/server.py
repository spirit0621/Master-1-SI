"""
Ce module définit la classe Server qui gère les connexions entrantes et la diffusion
des messages.

La classe ClientListener (importée) gère chaque client individuellement.
"""
#Permet à deux programmes de se parler à travers un réseau comme internet et réseau local
import socket
#Sortie du programme en cas d'erreur fatale
import sys 
#Permet de mettre en pause le programme
import time
#Importation de la classe ClientListener
from clientthread import ClientListener

class Server():
# socket.AF_INET : Utilise la famille d'adresses IPv4.
# socket.SOCK_STREAM : Utilise le protocole de transport TCP (fiable, ordonné et connecté).
#self= id et port
    def __init__(self, port):
        self.listener= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listener.bind(('', port))
        self.listener.listen(1)
        print("Listening on port", port)
        self.clients_sockets= []
#on sait sur quel port le serveur écoute.

#recevoir les connexions clientes en continu.
#met le programme en pause jusqu'à ce qu'un client tente de se connecter. Dès que la connexion est établie, il retourne :
#client_socket : un nouveau socket dédié exclusivement aux échanges avec ce client.
#client_adress : un tuple (ensemble de donnée qui ne peut etre modifié) contenant (adresse_IP_client, port_éphémère).
    def run(self):
        while True:
            print("listening new customers")
            try:
                (client_socket, client_adress) = self.listener.accept()
            except socket.error:
                sys.exit("Cannot connect clients")
#Si une erreur de socket survient lors de l'acceptation, le serveur affiche "Cannot connect clients" et s'arrête avec sys.exit().
            self.clients_sockets.append(client_socket)
#Ajoute le socket du nouveau client à la liste globale self.clients_sockets pour qu'il reçoive les futurs messages diffusés.
            print("Start the thread for client:", client_adress)
            client_thread= ClientListener(self, client_socket, client_adress)
            client_thread.start()
            time.sleep(0.1)

    # Déconnexion d'un Client : remove_socket()
    def remove_socket(self, socket):
        self.clients_sockets.remove(socket)
#Déclare la méthode remove_socket, appelée par ClientListener.quit() lorsqu'un client quitte le chat.
#Retire le socket du client déconnecté de la liste self.clients_sockets pour ne plus tenter de lui envoyer de messages.

    #Diffusion des Messages
    #Affiche le message diffusé dans la console du serveur pour tracer l'activité.
    def echo(self, data):
        print("echoing:", data)
        for sock in self.clients_sockets:
            try:
                sock.sendall(data.encode("UTF-8"))
            except socket.error:
                print("Cannot send the message")

#Point d'Entrée du Script
if __name__ == "__main__":
    server= Server(59001)
    server.run()
