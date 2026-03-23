import socket
import json

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5005
BUFFER_SIZE = 1024

#creazione socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((SERVER_IP, SERVER_PORT))

print("Server in attesa di messaggi...")

while True:
    #ricezione dei dati dal client
    data, addr = sock.recvfrom(BUFFER_SIZE)
    if not data:
        break

    data = data.decode() #perchè sono in binario
    data = json.loads(data)

    primoNumero = data["primoNumero"]
    operazione = data["operazione"]
    secondoNumero = data["secondoNumero"]

    print(f"Messaggio ricevuto dal client: ", primoNumero, operazione, secondoNumero)

    #invio di una risposta al client
    reply = ""

    if operazione == "+":
        reply = int((primoNumero + secondoNumero))
    if operazione == "-":
        reply = int((primoNumero - secondoNumero))
    if operazione == "*":
        reply = int((primoNumero * secondoNumero))
    if operazione == "/":
        reply = int((primoNumero / secondoNumero))

    sock.sendto(str(reply).encode(), addr)