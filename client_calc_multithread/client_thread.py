#client TCP multithread che invia NUM_WORKERS richieste contemporanee al server
#ogni richiesta contiene un'operazione aritmetica da eseguire

import socket         # Per la comunicazione di rete
import json           # Per la codifica/decodifica JSON
import random         # Per generare numeri casuali
import time           # Per misurare i tempi di esecuzione
import threading      # Per gestire l'esecuzione parallela (multithreading)

# --- Configurazione ---
HOST = "127.0.0.1" #ip del server
PORT = 22224 #porta del server 
NUM_WORKERS = 15 #numero di richieste (thread) da inviare in parallelo
OPERAZIONI = ["+", "-", "*", "/", "%"]  #lista delle operazioni consentite

#definizione della funzione che ogni thread eseguirà singolarmente
def genera_richieste(address, port):
    #apertura del socket TCP. Il costrutto 'with' garantisce la chiusura automatica del socket.
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock_service:
        sock_service.connect((address, port))  #tentativo di connessione all'indirizzo e alla porta specificati

        #dichiarazione variabili random dei due numeri e dell'operazione da eseguire
        primoNumero = random.randint(0, 100) #numeri da 0 a 100
        operazione = OPERAZIONI[random.randint(0, 3)]  #operazione random (tra le prime 4)
        secondoNumero = random.randint(0, 100)

        #reazione del dizionario Python e conversione in stringa formato JSON
        messaggio = {
            "primoNumero": primoNumero,
            "operazione": operazione,
            "secondoNumero": secondoNumero
        }
        messaggio = json.dumps(messaggio)

        #invio del messaggio al server codificato in byte (UTF-8)
        sock_service.sendall(messaggio.encode("UTF-8"))

        #registrazione del tempo di inizio subito dopo l'invio 
        start_time_thread = time.time()

        #attesa della risposta dal server
        data = sock_service.recv(1024)

    #chiusura del blocco 'with'. Calcolo e stampa dei tempi.
    end_time_thread = time.time()
    print("Received: ", data.decode())
    print(f"{threading.current_thread().name} exec time = ", end_time_thread - start_time_thread)

# --- Punto di ingresso del programma ---
if __name__ == "__main__":
    start_time = time.time()  #tempo di inizio totale

    #creazione della lista di oggetti Thread. Ogni thread punta alla funzione 'genera_richieste'
    threads = [
        threading.Thread(target=genera_richieste, args=(HOST, PORT))
        for _ in range(NUM_WORKERS)
    ]

    #avvio di tutti i thread (le richieste partono quasi contemporaneamente)
    [thread.start() for thread in threads]

    #attesa che tutti i thread finiscano prima di proseguire con il thread principale
    [thread.join() for thread in threads]

    end_time = time.time()  #tempo totale dalla partenza del primo thread alla fine dell'ultimo

    #stampa il tempo complessivo impiegato per eseguire tutte le richieste
    print("Tempo totale impiegato = ", end_time - start_time)