import pygame

def draw(pantalla, ancho_pantalla, alto_pantalla, options, orden):
    if options['orientacion'] == 'horizontal':
        alto_orden = (alto_pantalla - 200 - 10 - 10 - (10 * (options['filas']) - 1)) / options['filas']
        ancho_orden = ((ancho_pantalla // 2) - 10 - 10 - (10 * (options['columnas']) - 1)) / options['columnas']
    
    if options['orientacion'] == 'vertical':
        ancho_orden = (ancho_pantalla - 10 - 10 - (10 * (options['columnas']) - 1)) / options['columnas']
        alto_orden = ((alto_pantalla // 2) - 200 - 10 - 10 - (10 * (options['filas']) - 1)) / options['filas']
    
    posicion_x = (ancho_pantalla - ancho_orden) // 2
    posicion_y = (alto_pantalla - alto_orden) // 2
    pygame.draw.rect(pantalla, options['background_order_anunciando_color'], (posicion_x, posicion_y, ancho_orden, alto_orden))
    fuente_orden = pygame.font.Font(None, options['order_text_size'])
    fuente_cliente = pygame.font.Font(None, options['client_text_size'])
    texto_oden_renderizado = fuente_orden.render(orden['texto'].upper(), True, options['foreground_order_color'])
    cliente_oden_renderizado = fuente_cliente.render(orden['cliente'].upper(), True, options['foreground_order_color'])
    posicion_texto_orden_x = posicion_x + ((ancho_orden // 2) - (texto_oden_renderizado.get_width() // 2))
    posicion_texto_orden_y = posicion_y + ((alto_orden // 2) - (texto_oden_renderizado.get_height() // 2) - (cliente_oden_renderizado.get_height() // 2))
    pantalla.blit(texto_oden_renderizado, (posicion_texto_orden_x, posicion_texto_orden_y))
    posicion_cliente_orden_x = posicion_x + ((ancho_orden // 2) - (cliente_oden_renderizado.get_width() // 2))
    posicion_cliente_orden_y = posicion_y + ((alto_orden // 2) - (cliente_oden_renderizado.get_height() // 2) + (texto_oden_renderizado.get_height() // 2))
    pantalla.blit(cliente_oden_renderizado, (posicion_cliente_orden_x, posicion_cliente_orden_y))