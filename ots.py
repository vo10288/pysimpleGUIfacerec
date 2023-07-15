import opentimestamps.client as otsclient
import hashlib

# Funzione per calcolare l'hash del file
def calculate_hash(file_path):
    with open(file_path, 'rb') as file:
        data = file.read()
        file_hash = hashlib.sha256(data).digest()
        return file_hash

# Percorso del file da stampare sulla blockchain
file_path = 'path/to/your/file'

# Calcola l'hash del file
file_hash = calculate_hash(file_path)

# Crea un oggetto `OpentimestampsClient`
client = otsclient.create_client()

try:
    # Creazione di un timestamp
    timestamp = client.stamp(file_hash)

    # Stampa l'hash originale e l'hash del timestamp sulla blockchain
    print("Hash originale: ", file_hash.hex())
    print("Hash del timestamp: ", timestamp.msg.hex())

    # Verifica che il timestamp sia valido
    verification = client.verify(timestamp)
    if verification:
        print("Il timestamp è valido!")
    else:
        print("Il timestamp non è valido.")
except otsclient.exceptions.TimeoutError:
    print("Timeout durante la creazione del timestamp.")
except otsclient.exceptions.Error as e:
    print("Errore durante la creazione del timestamp:", str(e))
