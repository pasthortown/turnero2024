import pygame

def draw(pantalla, ancho_pantalla, alto_pantalla, options, ordenes):
    ancho_linea = options['line_width']
    color_texto = options['preparando_side_foreground_color']
    fuente = pygame.font.Font(None, options['title_size'])
    texto = "PREPARANDO"
    texto_renderizado = fuente.render(texto, True, color_texto)

    if options['orientacion'] == 'horizontal':
        if options['orden_lista']:
            posicion_texto_x = (ancho_pantalla // 4) - (texto_renderizado.get_width() // 2)
        else:
            posicion_texto_x = (ancho_pantalla // 2) - (texto_renderizado.get_width() // 2)
        posicion_texto_y = 10
        alto_orden = (alto_pantalla - 200 - 10 - 10 - (10 * (options['filas']) - 1)) / options['filas']
        if options['orden_lista']:
            ancho_orden = ((ancho_pantalla // 2) - 10 - 10 - (10 * (options['columnas']) - 1)) / options['columnas']
        else:
            ancho_orden = (ancho_pantalla - 10 - 10 - (10 * (options['columnas']) - 1)) / options['columnas']
        if options['orden_lista']:
            pygame.draw.rect(pantalla, options['line_color'], (ancho_pantalla // 2 - ancho_linea, 0, ancho_linea, alto_pantalla - 100))
        pantalla.blit(texto_renderizado, (posicion_texto_x, posicion_texto_y))

    if options['orientacion'] == 'vertical':
        posicion_texto_x = (ancho_pantalla // 2) - (texto_renderizado.get_width() // 2)
        posicion_texto_y = 10
        ancho_orden = (ancho_pantalla - 10 - 10 - (10 * (options['columnas']) - 1)) / options['columnas']
        if options['orden_lista']:
            alto_orden = ((alto_pantalla // 2) - 200 - 10 - 10 - (10 * (options['filas']) - 1)) / options['filas']
        else:
            alto_orden = (alto_pantalla - 200 - 10 - 10 - (10 * (options['filas']) - 1)) / options['filas']
        if options['orden_lista']:
            pygame.draw.rect(pantalla, options['line_color'], (0, (alto_pantalla // 2) - 100 - ancho_linea, ancho_pantalla, ancho_linea))
        pantalla.blit(texto_renderizado, (posicion_texto_x, posicion_texto_y))
    
    fila = 0
    columna = 0
    count = 0
    for orden in ordenes:
        if options['orientacion'] == 'horizontal':
            posicion_x = 10 + (columna * 10) + (columna * ancho_orden)
            posicion_y = 100 + (10 * fila) + (alto_orden * fila)
        else:
            posicion_x = 10 + (columna * 10) + (columna * ancho_orden)
            posicion_y = 100 + 10 + (fila * 10) + (fila * alto_orden)
        pygame.draw.rect(pantalla, options['background_order_preparando_color'], (posicion_x, posicion_y, ancho_orden, alto_orden))
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
        columna += 1
        count += 1
        if columna == options['columnas']:
            columna = 0
            fila += 1
        if options['filas'] * options['columnas'] == count:
            break