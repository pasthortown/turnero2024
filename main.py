import pygame
import footer
import orden_lista_side
import preparando_side
import anunciando_side
import tts
from dotenv import load_dotenv
import os
from pynput import keyboard

load_dotenv()

pygame.init()
info = pygame.display.Info()
ancho_pantalla = info.current_w
alto_pantalla = info.current_h

options = {
    "background_image": os.getenv("BACKGROUND_IMAGE"),
    "logo": os.getenv("LOGO"),
    "orientacion": os.getenv("ORIENTACION"),
    "orden_lista": os.getenv("ORDEN_LISTA", default=True),
    "title_size": int(os.getenv("TITLE_SIZE")),
    "line_width": int(os.getenv("LINE_WIDTH")),
    "line_color": tuple(map(int, os.getenv("LINE_COLOR").split(","))),
    "order_text_size": int(os.getenv("ORDER_TEXT_SIZE")),
    "client_text_size": int(os.getenv("CLIENT_TEXT_SIZE")),
    "background_order_preparando_color": tuple(map(int, os.getenv("BACKGROUND_ORDER_PREPARANDO_COLOR").split(","))),
    "background_order_lista_color": tuple(map(int, os.getenv("BACKGROUND_ORDER_LISTA_COLOR").split(","))),
    "background_order_anunciando_color": tuple(map(int, os.getenv("BACKGROUND_ORDER_ANUNCIANDO_COLOR").split(","))),
    "footer_background_color": tuple(map(int, os.getenv("FOOTER_BACKGROUND_COLOR").split(","))),
    "footer_foreground_color": tuple(map(int, os.getenv("FOOTER_FOREGROUND_COLOR").split(","))),
    "foreground_order_color": tuple(map(int, os.getenv("FOREGROUND_ORDER_COLOR").split(","))),
    "preparando_side_foreground_color": tuple(map(int, os.getenv("PREPARANDO_SIDE_FOREGROUND_COLOR").split(","))),
    "orden_lista_side_foreground_color": tuple(map(int, os.getenv("ORDEN_LISTA_SIDE_FOREGROUND_COLOR").split(","))),
    "filas": int(os.getenv("FILAS")),
    "columnas": int(os.getenv("COLUMNAS"))
}

pantalla = pygame.display.set_mode((ancho_pantalla, alto_pantalla), pygame.FULLSCREEN)
pygame.display.set_caption("Turnero")

ordenes_listas = []
ordenes_preparando = []
ordenes_anunciando = []
qr=""

running = True
anunciando = False

def get_orders():
    global ordenes_preparando, ordenes_listas
    ordenes_preparando = []
    pass

def update_order():
    pass

def validate_qr(qr):
    encontrada = False
    for order in ordenes_preparando:
        if ( str(order['id']) == qr ):
            ordenes_preparando.remove(order)
            ordenes_anunciando.append(order)
            ordenes_listas.append(order)
            encontrada = True
            break
    if not encontrada:
        for order in ordenes_listas:
            if ( str(order['id']) == qr ):
                ordenes_listas.remove(order)
                break

def on_press(key):
    global qr
    try:
        if key == keyboard.Key.space:
            qr += " "
        elif key.char:
            qr += key.char
    except AttributeError:
        pass

def on_release(key):
    global qr
    if key == keyboard.Key.enter:
        validate_qr(qr)
        qr = ""

def anunciar_orden(orden):
    numeros = int("".join([c for c in orden['texto'] if c.isdigit()]))
    texto_formateado = f"Orden {str(numeros)} Lista"
    anunciando_side.draw(pantalla, ancho_pantalla, alto_pantalla, options, orden)
    tts.say(texto_formateado)

listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

count = 0
while running:
    if count == 1:
        tts.say("Turnero preparado, comencemos")
        pygame.time.delay(2000)

    count = count + 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    imagen_fondo = pygame.image.load(options['background_image'])
    imagen_fondo_escalada = pygame.transform.scale(imagen_fondo, (ancho_pantalla, alto_pantalla))
    pantalla.blit(imagen_fondo_escalada, (0, 0))
    
    footer.draw(pantalla, ancho_pantalla, alto_pantalla, options)
    if options['orden_lista']:
        orden_lista_side.draw(pantalla, ancho_pantalla, alto_pantalla, options, ordenes_listas)
    preparando_side.draw(pantalla, ancho_pantalla, alto_pantalla, options, ordenes_preparando)
    
    if len(ordenes_anunciando) > 0 and count > 10:
        anunciando = True
        orden_anunciar = ordenes_anunciando.pop(0)
        anunciar_orden(orden_anunciar)
    else:
        anunciando = False
    
    pygame.display.flip()
    if anunciando:
        pygame.time.delay(4000)

    get_orders()
    pygame.time.delay(1000)

pygame.quit()
