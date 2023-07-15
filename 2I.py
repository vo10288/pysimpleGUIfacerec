import os
import cv2
import numpy as np
import face_recognition
import PySimpleGUI as sg
from datetime import datetime
from io import BytesIO

# Funzione per il riconoscimento facciale tra due immagini
def perform_face_recognition(image_1, image_2):
    # Converte le immagini in RGB (per il riconoscimento facciale di face_recognition)
    image_1_rgb = cv2.cvtColor(image_1, cv2.COLOR_BGR2RGB)
    image_2_rgb = cv2.cvtColor(image_2, cv2.COLOR_BGR2RGB)

    # Trova i volti nelle immagini
    face_locations_1 = face_recognition.face_locations(image_1_rgb)
    face_locations_2 = face_recognition.face_locations(image_2_rgb)

    if len(face_locations_1) > 0 and len(face_locations_2) > 0:
        # Calcola i landmark del viso
        face_landmarks_1 = face_recognition.face_landmarks(image_1_rgb, face_locations_1)
        face_landmarks_2 = face_recognition.face_landmarks(image_2_rgb, face_locations_2)

        # Disegna i keypoint, i landmark e il quadrato di corrispondenza sulle immagini
        draw_keypoints(image_1, face_landmarks_1[0])
        draw_keypoints(image_2, face_landmarks_2[0])

        # Disegna il quadrato di corrispondenza solo se ci sono volti trovati
        draw_match_rectangle(image_1, face_locations_1[0], image_2, face_locations_2[0])

    # Restituisce le immagini modificate
    return image_1, image_2

# Funzione per disegnare i keypoint e i landmark sulle immagini
def draw_keypoints(image, landmarks):
    for keypoint in landmarks:
        for point in landmarks[keypoint]:
            cv2.circle(image, point, 2, (255, 0, 0), -1)

# Funzione per disegnare il quadrato di corrispondenza tra i volti sulle immagini
def draw_match_rectangle(image_1, face_location_1, image_2, face_location_2):
    top_1, right_1, bottom_1, left_1 = face_location_1
    top_2, right_2, bottom_2, left_2 = face_location_2

    cv2.rectangle(image_1, (left_1, top_1), (right_1, bottom_1), (0, 255, 255), 2)
    cv2.rectangle(image_2, (left_2, top_2), (right_2, bottom_2), (0, 255, 255), 2)

# Crea una cartella "reports" se non esiste già
if not os.path.exists("reports"):
    os.makedirs("reports")

# Crea una cartella "temp" per le immagini modificate temporanee
if not os.path.exists("temp"):
    os.makedirs("temp")

# Crea l'interfaccia grafica
layout = [
    [sg.Image(key='image_left'), sg.Image(key='image_right')],
    [sg.Button('Seleziona immagine sinistra'), sg.Button('Seleziona immagine destra'), sg.Button('Face Recognition')],
    [sg.Output(size=(60, 10), key='output')]
]

window = sg.Window('Face Recognition', layout)

image_1 = None
image_2 = None

# Ciclo dell'interfaccia grafica
while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        break
    elif event == 'Seleziona immagine sinistra':
        image_path_1 = sg.popup_get_file('Seleziona l\'immagine sinistra')
        if image_path_1:
            # Carica l'immagine
            image_1 = cv2.imread(image_path_1)
            if image_1 is not None:
                image_1_rgb = cv2.cvtColor(image_1, cv2.COLOR_BGR2RGB)
                face_landmarks_1 = face_recognition.face_landmarks(image_1_rgb)
                draw_keypoints(image_1, face_landmarks_1[0])
                image_1_bytes = cv2.imencode('.png', image_1)[1].tobytes()
                window['image_left'].update(data=image_1_bytes)
    elif event == 'Seleziona immagine destra':
        image_path_2 = sg.popup_get_file('Seleziona l\'immagine destra')
        if image_path_2:
            # Carica l'immagine
            image_2 = cv2.imread(image_path_2)
            if image_2 is not None:
                image_2_rgb = cv2.cvtColor(image_2, cv2.COLOR_BGR2RGB)
                face_landmarks_2 = face_recognition.face_landmarks(image_2_rgb)
                draw_keypoints(image_2, face_landmarks_2[0])
                image_2_bytes = cv2.imencode('.png', image_2)[1].tobytes()
                window['image_right'].update(data=image_2_bytes)
    elif event == 'Face Recognition':
        if image_1 is not None and image_2 is not None:
            try:
                # Esegue il riconoscimento facciale tra le due immagini e ottiene le immagini modificate
                image_1_modified, image_2_modified = perform_face_recognition(image_1, image_2)

                # Mostra le immagini modificate
                image_1_modified_bytes = cv2.imencode('.png', image_1_modified)[1].tobytes()
                image_2_modified_bytes = cv2.imencode('.png', image_2_modified)[1].tobytes()
                window['image_left'].update(data=image_1_modified_bytes)
                window['image_right'].update(data=image_2_modified_bytes)

                # Esegue il confronto facciale
                matches = face_recognition.compare_faces([image_1_modified], image_2_modified)[0]

                # Mostra il risultato
                print('Risultato del confronto facciale:')
                print(matches)

                # Salva il risultato in un file CSV
                timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
                report_file = f'reports/{timestamp}.csv'
                with open(report_file, 'w') as file:
                    file.write('Immagine 1,Immagine 2,Risultato\n')
                    file.write(f'{image_path_1},{image_path_2},{matches}')

                print(f'Results salvato in {report_file}')
            except Exception as e:
                print(f"Errore durante il riconoscimento facciale: {str(e)}")
        else:
            print('Seleziona entrambe le immagini prima di eseguire il confronto facciale')

window.close()
