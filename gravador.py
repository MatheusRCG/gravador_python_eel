import eel
import cv2
import numpy as np
import pyautogui
import threading

eel.init('web')

recording = False
stop_recording_flag = threading.Event()

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
        
        # Verificando se a gravação deve ser interrompida
        if stop_recording_flag.is_set():
            break

    # Liberando os recursos
    out.release()
    cv2.destroyAllWindows()

@eel.expose
def start_recording(output_file, fps, width, height):
    global recording, stop_recording_flag
    if not recording:
        stop_recording_flag.clear()
        recording_thread = threading.Thread(target=record_screen, args=(output_file, fps, width, height))
        recording_thread.start()

@eel.expose
def stop_recording():
    global recording, stop_recording_flag
    recording = False
    stop_recording_flag.set()

@eel.expose
def take_screenshot(output_file):
    # Tirar um print da tela usando pyautogui
    pyautogui.screenshot(output_file)

eel.start('index.html')
