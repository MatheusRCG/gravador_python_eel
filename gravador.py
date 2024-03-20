import eel
import cv2
import numpy as np
import pyautogui
import threading

eel.init('web')

recording = False
recording_thread = None

@eel.expose
def record_screen(output_file, fps, width, height):
    global recording
    recording = True
    # Definindo o codec e criando um objeto VideoWriter
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter((output_file + '.avi'), fourcc, fps, (width, height))

    while recording:
        # Captura de tela usando pyautogui
        img = pyautogui.screenshot()

        # Convertendo a imagem para um array numpy
        frame = np.array(img)

        # Convertendo RGB para BGR
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # Escrevendo o frame no arquivo de vídeo
        out.write(frame)

    # Liberando os recursos
    out.release()

@eel.expose
def stop_recording():
    global recording, recording_thread
    recording = False
    # Aguardar até que a gravação termine
    if recording_thread is not None:
        recording_thread.join()

@eel.expose
def start_recording(output_file, fps, width, height):
    global recording, recording_thread
    if not recording:
        recording_thread = threading.Thread(target=record_screen, args=(output_file, fps, width, height))
        recording_thread.start()

@eel.expose
def take_screenshot(output_file):
    # Tirar um print da tela usando pyautogui
    pyautogui.screenshot(output_file + '.png')

eel.start('index.html')
