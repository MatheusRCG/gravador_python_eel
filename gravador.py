import eel
import cv2
import numpy as np
import pyautogui
import threading
from pynput.mouse import Listener

eel.init('web')

recording = False
recording_thread = None
start_x, start_y, end_x, end_y = None, None, None, None

@eel.expose
def record_screen(output_file, fps, width, height):
    print("gravando")
    global recording, x1, y1, x2, y2
    recording = True
    # Definindo o codec e criando um objeto VideoWriter
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter((output_file + '.avi'), fourcc, fps, (width, height))

    while recording:
        # Captura de tela usando pyautogui - region=(x1, y1, x2-x1, y2-y1)
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
def onMouseDown(x, y):
    global recording, start_x, start_y
    recording = True
    start_x = x
    start_y = y

@eel.expose
def onMouseUp(x, y):
    global recording, end_x, end_y
    recording = False
    end_x = x
    end_y = y


@eel.expose
def take_screenshot(output_file):
    # Tirar um print da tela usando pyautogui
    pyautogui.screenshot(output_file + '.png')



#################################################################################
#################################################################################
@eel.expose
def selecionar_pontos():
  """
  Função para selecionar dois pontos na tela e salvar suas posições.

  Retorna:
    Uma tupla com as posições dos dois pontos (x1, y1, x2, y2).
  """
  print("func exec")

  global x1, y1, x2, y2

  # Obter a resolução da tela
  largura, altura = pyautogui.size()

  # Obter a posição do primeiro ponto
  print("Clique no primeiro ponto.")
  x1, y1 = get_mouse_click_position()


  # Obter a posição do segundo ponto
  print("Clique no segundo ponto.")
  x2, y2 = get_mouse_click_position()


  # Salvar as posições dos pontos
  with open("pontos.txt", "a") as f:
    f.write(f"{largura}x{altura} {x1} {y1} {x2} {y2}\n")

  # Mostrar mensagem de sucesso
  print("Pontos salvos com sucesso!")


def on_click(x, y, button, pressed):
    if pressed:
        print(f"Você clicou na posição: x={x}, y={y}")
        global clicked_position
        clicked_position = (x, y)
        # Parar de escutar eventos do mouse após o clique
        return False

def get_mouse_click_position():
    global clicked_position
    clicked_position = None
    print("Clique em qualquer lugar da tela...")
    with Listener(on_click=on_click) as listener:
        listener.join()
    return clicked_position


#################################################################################
#################################################################################



eel.start('index.html')
