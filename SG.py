import PySimpleGUI as sg

# Imposta la dimensione del carattere desiderata
font_size = 16

# Crea la finestra di PySimpleGUI
layout = [[sg.Output(size=(100, 50), key='output', font=('Helvetica', font_size))]]
window = sg.Window('Finestra di Output', layout)

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break

    # Esempio di stampa con caratteri più grandi
    print('Questo è un testo di esempio con caratteri più grandi')

window.close()
