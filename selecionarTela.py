from pynput.mouse import Listener

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

clicked_position = get_mouse_click_position()
x1, y2 = clicked_position
print("Posição guardada:", x1, "....", y2)
