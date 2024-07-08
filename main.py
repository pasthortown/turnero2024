import pygame
import footer
import orden_lista_side
import preparando_side
import anunciando_side
import tts
from dotenv import load_dotenv
import os
from pynput import keyboard
import requests
from datetime import datetime, timedelta

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
    "columnas": int(os.getenv("COLUMNAS")),
    "tiempo_a_listo": int(os.getenv("TIEMPO_A_LISTO")),
    "tiempo_a_entregado": int(os.getenv("TIEMPO_A_ENTREGADO")),
    "update_orders_url": str(os.getenv("UPDATE_ORDERS_URL")),
    "get_orders_from_url": str(os.getenv("GET_ORDERS_FROM_URL")),
}

pantalla = pygame.display.set_mode((ancho_pantalla, alto_pantalla), pygame.FULLSCREEN)
pygame.display.set_caption("Turnero")

ordenes_listas = []
ordenes_preparando = []
ordenes_anunciando = []
qr=""

running = True
anunciando = False

def validar_tiempo_ordenes():
    global ordenes_listas, ordenes_preparando
    now = datetime.now()
    tiempo_listo = options['tiempo_a_listo']
    tiempo_a_entregado = options['tiempo_a_entregado']
    if not (tiempo_listo == 0):
        for order in ordenes_preparando:
            fecha_cumple_condicion = order['created_at'] + timedelta(seconds=tiempo_listo)
            if  now > fecha_cumple_condicion:
                validate_order_id(order['id'])
    if not (tiempo_a_entregado == 0):
        for order in ordenes_listas:
            fecha_cumple_condicion = order['created_at'] + timedelta(seconds=tiempo_a_entregado)
            if  now > fecha_cumple_condicion:
                validate_order_id(order['id'])

def order_exists(new_order, order_list):
    for order in order_list:
        if order['id'] == new_order['id']:
            return True
    return False

def clean_orders(income_orders):
    global ordenes_preparando, ordenes_listas
    to_remove_preparando = None
    to_remove_listas = None
    
    for order in ordenes_preparando:
        exist_in_income = any(order['id'] == income_order['id'] and income_order['status'] == 'Preparando' for income_order in income_orders)
        if not exist_in_income:
            to_remove_preparando = order
            ordenes_anunciando.append(order)
    
    for order in ordenes_listas:
        exist_in_income = any(order['id'] == income_order['id'] and income_order['status'] == 'Listo' for income_order in income_orders)
        if not exist_in_income:
            to_remove_listas = order
    
    if to_remove_preparando:
        ordenes_preparando.remove(to_remove_preparando)
    
    if to_remove_listas:
        ordenes_listas.remove(to_remove_listas)

def get_orders():
    global ordenes_preparando, ordenes_listas
    try:
        response = requests.get(options['get_orders_from_url'])
        r = response.json()
        income_orders = []
        if r['str'] > 0:
            for i in range(r['str']):
                order_income = r[str(i)]
                order_income['created_at'] = datetime.now()
                order_income['texto'] = order_income['text']
                income_orders.append(order_income)
                if order_income['status'] == 'Preparando':
                    if not order_exists(order_income, ordenes_preparando):
                        ordenes_preparando.append(order_income)
                elif order_income['status'] == 'Listo':
                    if not order_exists(order_income, ordenes_listas):
                        ordenes_listas.append(order_income)
        ordenes_preparando = sanitize_orders(ordenes_preparando)
        ordenes_listas = sanitize_orders(ordenes_listas)
        clean_orders(income_orders)
    except Exception as e:
        pass

def sanitize_orders(array):
    for obj in array:
        if 'id' not in obj:
            obj['id'] = ""
        if 'texto' not in obj:
            obj['texto'] = ""
        if 'cliente' not in obj:
            obj['cliente'] = ""
        if obj['texto'] == "":
            obj['texto'] = obj['id'][-2:]
    return array

def update_order(id):
    try:
        url_to_update = options['update_orders_url'] + str(id)
        response = requests.get(url_to_update)
        if response.status_code == 200:
            get_orders()
    except:
        pass

def validate_order_id(id):
    encontrada = False
    for order in ordenes_preparando:
        if ( str(order['id']) == id ):
            ordenes_anunciando.append(order)
            update_order(id)
            encontrada = True
            break
    if not encontrada:
        for order in ordenes_listas:
            if ( str(order['id']) == id ):
                ordenes_listas.remove(order)
                update_order(id)
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
        validate_order_id(qr)
        qr = ""
        pygame.time.delay(1000)

def anunciar_orden(orden):
    numeros = int("".join([c for c in orden['texto'] if c.isdigit()]))
    texto_formateado = f"Orden {str(numeros)} Lista"
    anunciando_side.draw(pantalla, ancho_pantalla, alto_pantalla, options, orden)
    tts.say(texto_formateado)

listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

VALIDAR_ORDENES_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(VALIDAR_ORDENES_EVENT, 10000)

count = 0
while running:
    if count == 1:
        tts.say("Turnero preparado, comencemos")
        pygame.time.delay(2000)
        
    count = count + 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == VALIDAR_ORDENES_EVENT:
            validar_tiempo_ordenes()

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
