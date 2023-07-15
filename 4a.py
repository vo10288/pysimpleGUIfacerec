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

    # Calcola i landmark del viso
    face_landmarks_1 = face_recognition.face_landmarks(image_1_rgb, face_locations_1)
    face_landmarks_2 = face_recognition.face_landmarks(image_2_rgb, face_locations_2)

    # Restituisce i risultati del riconoscimento facciale
    return face_locations_1, face_landmarks_1, face_locations_2, face_landmarks_2


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
                # Disegna i keypoint e i landmark sulla copia dell'immagine
                image_1_copy = image_1.copy()
                face_locations_1, face_landmarks_1, _, _ = perform_face_recognition(image_1, image_2)
                for landmarks in face_landmarks_1:
                    draw_keypoints(image_1_copy, landmarks)
                    draw_match_rectangle(image_1_copy, face_locations_1[0], image_2, face_locations_2[0])

                # Aggiorna l'immagine nella GUI
                image_1_bytes = cv2.imencode('.png', image_1_copy)[1].tobytes()
                window['image_left'].update(data=image_1_bytes)

    elif event == 'Seleziona immagine destra':
        image_path_2 = sg.popup_get_file('Seleziona l\'immagine destra')
        if image_path_2:
            # Carica l'immagine
            image_2 = cv2.imread(image_path_2)

            if image_2 is not None:
                # Disegna i keypoint e i landmark sulla copia dell'immagine
                image_2_copy = image_2.copy()
                _, _, face_locations_2, face_landmarks_2 = perform_face_recognition(image_1, image_2)
                for landmarks in face_landmarks_2:
                    draw_keypoints(image_2_copy, landmarks)
                    draw_match_rectangle(image_1, face_locations_1[0], image_2_copy, face_locations_2[0])

                # Aggiorna l'immagine nella GUI
                image_2_bytes = cv2.imencode('.png', image_2_copy)[1].tobytes()
                window['image_right'].update(data=image_2_bytes)

    elif event == 'Face Recognition':
        if image_1 is not None and image_2 is not None:
            # Esegue il riconoscimento facciale tra le due immagini
            face_locations_1, _, face_locations_2, _ = perform_face_recognition(image_1, image_2)

            # Disegna il quadrato di corrispondenza sulla copia dell'immagine
            image_1_copy = image_1.copy()
            image_2_copy = image_2.copy()
            draw_match_rectangle(image_1_copy, face_locations_1[0], image_2_copy, face_locations_2[0])

            # Aggiorna le immagini nella GUI
            image_1_bytes = cv2.imencode('.png', image_1_copy)[1].tobytes()
            image_2_bytes = cv2.imencode('.png', image_2_copy)[1].tobytes()
            window['image_left'].update(data=image_1_bytes)
            window['image_right'].update(data=image_2_bytes)

        else:
            print('Seleziona entrambe le immagini prima di eseguire il confronto facciale')

window.close()
