import socket
import json

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5005
BUFFER_SIZE = 1024
NUM_MESSAGES = 5

#creazione socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

primoNumero = float(input("inserisci il primo numero: "))
operazione = input("inserisci l'operazione (simbolo): ")
secondoNumero = float(input("inserisci il secondo numero: "))

#invio messaggio al server
messaggio = {"primoNumero":primoNumero,
                "operazione":operazione,
                "secondoNumero":secondoNumero}

messaggio = json.dumps(messaggio)

sock.sendto(messaggio.encode("UTF-8"), (SERVER_IP, SERVER_PORT))
print(f"Messaggio inviato al server: {messaggio}")

#ricezione della risposta dal server
data, addr = sock.recvfrom(BUFFER_SIZE)
print(f"Messaggio ricevuto dal server {addr}: {data.decode()}")

#chiusura socket
sock.close()