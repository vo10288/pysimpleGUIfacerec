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
    #image_1_rgb = cv2.cvtColor(image_1, cv2.COLOR_BGR2RGB)
    #image_2_rgb = cv2.cvtColor(image_2, cv2.COLOR_BGR2RGB)

    # Trova i volti nelle immagini
    face_locations_1 = face_recognition.face_locations(image_1)
    face_locations_2 = face_recognition.face_locations(image_2)

    if len(face_locations_1) > 0 and len(face_locations_2) > 0:
        # Calcola i landmark del viso
        face_landmarks_1 = face_recognition.face_landmarks(image_1, face_locations_1)
        face_landmarks_2 = face_recognition.face_landmarks(image_2, face_locations_2)

        # Disegna i keypoint, i landmark e il quadrato di corrispondenza sulle immagini
        draw_keypoints(image_1, face_landmarks_1[0])
        draw_keypoints(image_2, face_landmarks_2[0])
        
        first_image_encodeds = face_recognition.face_encodings(image_1, face_locations_1)
        second_image_encodeds = face_recognition.face_encodings(image_2, face_locations_2)[0]
        
        
        # Esegue il riconoscimento facciale tra le immagini non ridimensionate
        matches = face_recognition.compare_faces(first_image_encodeds, second_image_encodeds)
        distances = face_recognition.face_distance(first_image_encodeds, second_image_encodeds)

    # Restituisce il risultato del confronto e le immagini modificate
    return first_image_encodeds, second_image_encodeds, face_landmarks_1, face_landmarks_1, face_locations_1, face_locations_2, matches, distances, image_1, image_2

    
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
    [sg.Output(size=(100, 50), key='output')]
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
			#image_1 = cv2.imread(image_path_1)
			#######################################
            
			# Carica l'immagine
			resized_image1 = cv2.imread(image_path_1)

			# Ottieni la larghezza e l'altezza dell'immagine
			height, width = resized_image1.shape[:2]

			# Controlla se la larghezza o l'altezza sono superiori a 500px
			if width > 400 or height > 400:
				# Calcola il fattore di ridimensionamento in base alla dimensione massima desiderata (500px)
				scale = max(400 / width, 400 / height)

				# Calcola le nuove dimensioni mantenendo le proporzioni
				new_width = int(width * scale)
				new_height = int(height * scale)

				# Ridimensiona l'immagine utilizzando le nuove dimensioni
				image_1 = cv2.resize(resized_image1, (new_width, new_height))

				# Ora l'immagine ridimensionata è memorizzata nella variabile 'resized_image'
			else:
				# L'immagine non ha bisogno di essere ridimensionata
				image_1 = resized_image1

				# Continua ad utilizzare 'resized_image' come necessario

			
			
			
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
            #image_2 = cv2.imread(image_path_2)
            #######################################
            
			# Carica l'immagine
			resized_image = cv2.imread(image_path_2)

			# Ottieni la larghezza e l'altezza dell'immagine
			height, width = resized_image.shape[:2]

			# Controlla se la larghezza o l'altezza sono superiori a 500px
			if width > 400 or height > 400:
				# Calcola il fattore di ridimensionamento in base alla dimensione massima desiderata (500px)
				scale = max(400 / width, 400 / height)

				# Calcola le nuove dimensioni mantenendo le proporzioni
				new_width = int(width * scale)
				new_height = int(height * scale)

				# Ridimensiona l'immagine utilizzando le nuove dimensioni
				image_2 = cv2.resize(resized_image, (new_width, new_height))

				# Ora l'immagine ridimensionata è memorizzata nella variabile 'resized_image'
			else:
				# L'immagine non ha bisogno di essere ridimensionata
				image_2 = resized_image

				# Continua ad utilizzare 'resized_image' come necessario

            
            
            #######################################
            
            
			if image_2 is not None:
				image_2_rgb = cv2.cvtColor(image_2, cv2.COLOR_BGR2RGB)
				face_landmarks_2 = face_recognition.face_landmarks(image_2_rgb)
				draw_keypoints(image_2, face_landmarks_2[0])
				image_2_bytes = cv2.imencode('.png', image_2)[1].tobytes()
				window['image_right'].update(data=image_2_bytes)
	elif event == 'Face Recognition':
		if image_1 is not None and image_2 is not None:
			try:
                # Esegue il riconoscimento facciale tra le due immagini e ottiene il risultato del confronto
				first_image_encodeds, second_image_encodeds, face_landmarks_1, face_landmarks_1, face_locations_1, face_locations_2, matches, distances, image_1, image_2 = perform_face_recognition(image_1, image_2)

                # Mostra le immagini modificate
                
                #image_1_modified_bytes = cv2.imencode('.png', image_1_modified)[1].tobytes()
                #image_2_modified_bytes = cv2.imencode('.png', image_2_modified)[1].tobytes()
                #window['image_left'].update(data=image_1_modified_bytes)
                #window['image_right'].update(data=image_2_modified_bytes)

                # Mostra il risultato del confronto
				if matches is not None:
					print('Risultato del confronto facciale:')
					print(matches)
					distances = ((1-distances)*100)
					print(str(distances)+' %')
				else:
					print('Nessun volto trovato nelle immagini.')

                # Salva il risultato in un file CSV
				timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
				report_file = f'reports/{timestamp}.csv'
				with open(report_file, 'w') as file:
					file.write('Immagine 1,Immagine 2,Risultato,Percentuale di compatibilità biometrica\n')
					file.write(f'{image_path_1},{image_path_2},{matches},str({distances} %)')
#first_image_encodeds, second_image_encodeds, face_landmarks_1, face_landmarks_1, face_locations_1, face_locations_2, matches, distances, image_1, image_2                    
					file.write(f'FACE LOCATION FIRST IMAGE SX\n')
					file.write(f'str({face_locations_1})\n')
                    
					file.write(f'FACE LANDMARKS FIRST IMAGE SX\n')
					file.write(f'str({[face_landmarks_1]})\n')
                    
					file.write(f'FACE ENCODING FIRST IMAGE SX\n')
					file.write(f'str({first_image_encodeds})\n')
                    
                    ### 2 #####
                    
					file.write(f'FACE LOCATION SECOND IMAGE DX\n')
					file.write(f'str({face_locations_2})\n')
                    
					file.write(f'FACE LANDMARKS SECOND IMAGE SX\n')
					file.write(f'str({face_landmarks_2})\n')
                    
					file.write(f'FACE ENCODING SECOND IMAGE DX\n')
					file.write(f'str({[second_image_encodeds]})\n')

				print(f'Risultati salvati in {report_file}')
			except Exception as e:
				print(f"Errore durante il riconoscimento facciale: {str(e)}")
		else:
			print('Seleziona entrambe le immagini prima di eseguire il confronto facciale')

window.close()
