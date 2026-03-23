import socket
import json

#config server
IP = "127.0.0.1"
PORTA = 65432
DIM_BUFFER = 1024

#creazione della socket del server con il costrutto with
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock_server:
    sock_server.bind((IP, PORTA))

    #metto la socket in ascolto per le connessioni in ingresso
    sock_server.listen()

    print(f"Server in ascolto su {IP}:{PORTA}")

    #loop principale del server
    while True:
        #accetta le connessioni
        sock_service, address_client = sock_server.accept()
        with sock_service as sock_client:

            #leggi i dati inviati dal client
            dati = sock_client.recv(DIM_BUFFER).decode()
            dati = json.loads(dati)

            primoNumero = dati["primoNumero"]
            operazione = dati["operazione"]
            secondoNumero = dati["secondoNumero"]

            #invio di una risposta al client
            reply = ""

            if operazione == "+":
                reply = int((primoNumero + secondoNumero))
            elif operazione == "-":
                reply = int((primoNumero - secondoNumero))
            elif operazione == "*":
                reply = int((primoNumero * secondoNumero))
            elif operazione == "/":
                if secondoNumero == 0:
                    reply = "Errore: divisione per zero"
                else:
                    reply = primoNumero / secondoNumero

            #stampa il messaggio ricevuto e invia una risposta al client
            print(f"Ricevuto messaggio dal client {sock_client}: {dati}")
            sock_client.sendall(str(reply).encode())