import os
import cv2
import numpy as np
import face_recognition
import PySimpleGUI as sg
from datetime import datetime
from io import BytesIO
import time


# Funzione per il riconoscimento facciale tra due immagini
def perform_face_recognition(image_path_1, image_path_2):
    # Carica le immagini
    image_1 = face_recognition.load_image_file(image_path_1)
    image_2 = face_recognition.load_image_file(image_path_2)

    # Esegui il riconoscimento facciale
    face_encodings_1 = face_recognition.face_encodings(image_1)
    face_encodings_2 = face_recognition.face_encodings(image_2)

    # Confronta i volti
    matches = face_recognition.compare_faces(face_encodings_1, face_encodings_2)
    distances = face_recognition.face_distance(face_encodings_1,face_encodings_2)
    print(distances)
    print(matches)

    # Restituisce il risultato del confronto facciale
    return matches, distances


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

global image_1
image_1 = None
global image_2
image_2 = None

# Ciclo dell'interfaccia grafica
while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        break
    elif event == 'Seleziona immagine sinistra':
        image_path_1 = sg.popup_get_file('Seleziona l\'immagine sinistra')
        if image_path_1:
            # Carica l'immagine e applica le modifiche
            
            image_1 = cv2.imread(image_path_1)
            
            if image_1 is not None:
                image_1_rgb = cv2.cvtColor(image_1, cv2.COLOR_BGR2RGB)
                face_landmarks_1 = face_recognition.face_landmarks(image_1)
                draw_keypoints(image_1, face_landmarks_1[0])
                image_1_bytes = cv2.imencode('.png', image_1)[1].tobytes()
                window['image_left'].update(data=image_1_bytes)
    elif event == 'Seleziona immagine destra':
        image_path_2 = sg.popup_get_file('Seleziona l\'immagine destra')
        if image_path_2:
            # Carica l'immagine e applica le modifiche
            
            image_2 = cv2.imread(image_path_2)
            
            if image_2 is not None:
                image_2_rgb = cv2.cvtColor(image_2, cv2.COLOR_BGR2RGB)
                face_landmarks_2 = face_recognition.face_landmarks(image_2)
                draw_keypoints(image_2, face_landmarks_2[0])
                image_2_bytes = cv2.imencode('.png', image_2)[1].tobytes()
                window['image_right'].update(data=image_2_bytes)
    elif event == 'Face Recognition':
        if image_1 is not None and image_2 is not None:
            # Esegue il riconoscimento facciale tra le due immagini e ottiene le immagini modificate
            matches, image_1_modified, image_2_modified = perform_face_recognition(image_1, image_2)
#            perform_face_recognition(image_1, image_2)


            # Mostra il risultato
            print('Risultato del confronto facciale:')
            #window['output'].update(str(matches)+'\n'+str(distances))
            #sg.OutputString(matches+'\n'+distances)
            print(str(matches))
            print(str(distances))

            # Salva il risultato in un file CSV
            timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            report_file = f'reports/{timestamp}.csv'
            with open(report_file, 'w') as file:
                file.write('Immagine 1,Immagine 2,Risultato\n')
                file.write(f'{image_path_1},{image_path_2},{matches}')
                

            print(f'Results salvato in {report_file}')
            time.sleep(5)
            #window['image_left'].update(data=image_1_bytes)
            #window['image_right'].update(data=image_2_bytes)
        else:
            print('Seleziona entrambe le immagini prima di eseguire il confronto facciale')

window.close()
