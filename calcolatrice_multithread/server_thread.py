import socket           #per la comunicazione di rete
import json             #per la gestione dei dati in formato JSON
from threading import Thread  #per gestire le connessioni in parallelo (multithreading)

#funzione eseguita in un thread per ogni client connesso
def ricevi_comandi(sock_client, addr_client):
    with sock_client:
        print(f"Client connesso: {addr_client}")

        #loop principale del server
        while True:
            dati = sock_client.recv(DIM_BUFFER).decode()
            if not dati:
                break
            
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


#funzione che accetta una nuova connessione e lancia un thread per gestirla
def ricevi_connessioni(sock_listen):
    sock_service, address_client = sock_listen.accept() #accetta la connessione da un client
    try:
        #avvia un nuovo thread per gestire i comandi del client
        Thread(target=ricevi_comandi, args=(sock_service, address_client)).start()
    except Exception as e:
        print(e) #stampa eventuali errori nella creazione del thread


#funzione principale che avvia il server e resta in ascolto di nuove connessioni
def avvia_server(indirizzo, porta):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock_server:
        #imposta l'opzione per riutilizzare subito la porta dopo un riavvio del server
        sock_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        #associa il server all'indirizzo e alla porta specificati
        sock_server.bind((indirizzo, porta))
        
        #mette il server in ascolto con una coda massima di 5 connessioni pendenti
        sock_server.listen(5)
        
        #ciclo infinito per accettare e gestire connessioni multiple
        while True:
            ricevi_connessioni(sock_server)
            print(f" ---- Server in ascolto su {indirizzo}:{porta} ----")


# --- MAIN ---
#configurazione del server
IP = "127.0.0.1"       #indirizzo locale
PORTA = 65432          #porta di ascolto
DIM_BUFFER = 1024      #dimensione del buffer per la ricezione dati

#avvio del server
avvia_server(IP, PORTA)