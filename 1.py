import os
import cv2
import face_recognition
import PySimpleGUI as sg
from datetime import datetime
import csv

# Funzione per il riconoscimento facciale tra due immagini
def perform_face_recognition(image_path_1, image_path_2):
    # Carica le immagini
    image_1 = face_recognition.load_image_file(image_path_1)
    image_2 = face_recognition.load_image_file(image_path_2)

    # Converte le immagini in RGB (per il riconoscimento facciale di face_recognition)
    image_1_rgb = cv2.cvtColor(image_1, cv2.COLOR_BGR2RGB)
    image_2_rgb = cv2.cvtColor(image_2, cv2.COLOR_BGR2RGB)

    # Esegue il riconoscimento facciale
    face_encodings_1 = face_recognition.face_encodings(image_1_rgb)
    face_encodings_2 = face_recognition.face_encodings(image_2_rgb)

    # Confronta i volti
    matches = face_recognition.compare_faces(face_encodings_1, face_encodings_2)

    # Restituisce il risultato del confronto facciale
    return matches

# Crea una cartella "reports" se non esiste già
if not os.path.exists("reports"):
    os.makedirs("reports")

# Crea l'interfaccia grafica
layout = [
    [sg.Image(key='image_left'), sg.Image(key='image_right')],
    [sg.Button('Seleziona immagine sinistra'), sg.Button('Seleziona immagine destra'), sg.Button('Face Recognition')],
    [sg.Output(size=(60, 10))]
]

window = sg.Window('Face Recognition', layout)

image_path_1 = None
image_path_2 = None

# Ciclo dell'interfaccia grafica
while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        break
    elif event == 'Seleziona immagine sinistra':
        image_path_1 = sg.popup_get_file('Seleziona l\'immagine sinistra')
        if image_path_1:
            window['image_left'].update(filename=image_path_1)
    elif event == 'Seleziona immagine destra':
        image_path_2 = sg.popup_get_file('Seleziona l\'immagine destra')
        if image_path_2:
            window['image_right'].update(filename=image_path_2)
    elif event == 'Face Recognition':
        if image_path_1 and image_path_2:
            # Esegue il confronto facciale tra le due immagini
            matches = perform_face_recognition(image_path_1, image_path_2)

            # Mostra il risultato
            print('Risultato del confronto facciale:')
            print(matches)

            # Salva il risultato in un file CSV
            timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            report_file = f'reports/{timestamp}.csv'

            with open(report_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Immagine 1', 'Immagine 2', 'Risultato'])
                writer.writerow([image_path_1, image_path_2, matches])

            print(f'Results salvato in {report_file}')
        else:
            print('Seleziona entrambe le immagini prima di eseguire il confronto facciale')

window.close()
