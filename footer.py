import pygame

def draw(pantalla, ancho_pantalla, alto_pantalla, options):

    logo = pygame.image.load(options['logo'])
    pygame.draw.rect(pantalla, options['footer_background_color'], (0, alto_pantalla - 100, ancho_pantalla, 100))

    nuevo_ancho = logo.get_width() * (100 / logo.get_height())
    logo_escalado = pygame.transform.scale(logo, (nuevo_ancho, 90))

    posicion_logo_x = (ancho_pantalla - logo_escalado.get_width()) // 2
    posicion_logo_y = alto_pantalla - logo_escalado.get_height() - 5

    pantalla.blit(logo_escalado, (posicion_logo_x, posicion_logo_y))

    espacio = 100
    ancho_rectangulo = 120
    alto_rectangulo = 100

    posicion_rectangulo_y = alto_pantalla - alto_rectangulo

    posicion_rectangulo1_x = ancho_pantalla - espacio - ancho_rectangulo
    posicion_rectangulo2_x = posicion_rectangulo1_x - ancho_rectangulo - espacio
    posicion_rectangulo3_x = posicion_rectangulo2_x - ancho_rectangulo - espacio
    
    posicion_rectangulo4_x = espacio
    posicion_rectangulo5_x = posicion_rectangulo4_x + ancho_rectangulo + espacio
    posicion_rectangulo6_x = posicion_rectangulo5_x + ancho_rectangulo + espacio
    
    pygame.draw.rect(pantalla, options['footer_foreground_color'], (posicion_rectangulo1_x, posicion_rectangulo_y, ancho_rectangulo, alto_rectangulo))
    pygame.draw.rect(pantalla, options['footer_foreground_color'], (posicion_rectangulo2_x, posicion_rectangulo_y, ancho_rectangulo, alto_rectangulo))
    pygame.draw.rect(pantalla, options['footer_foreground_color'], (posicion_rectangulo3_x, posicion_rectangulo_y, ancho_rectangulo, alto_rectangulo))
    pygame.draw.rect(pantalla, options['footer_foreground_color'], (posicion_rectangulo4_x, posicion_rectangulo_y, ancho_rectangulo, alto_rectangulo))
    pygame.draw.rect(pantalla, options['footer_foreground_color'], (posicion_rectangulo5_x, posicion_rectangulo_y, ancho_rectangulo, alto_rectangulo))
    pygame.draw.rect(pantalla, options['footer_foreground_color'], (posicion_rectangulo6_x, posicion_rectangulo_y, ancho_rectangulo, alto_rectangulo))