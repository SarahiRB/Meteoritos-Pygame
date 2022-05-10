import pygame
import sys
from pygame.locals import *
from random import randint
from time import process_time

# clases que cree
from clases import jugador
from clases import asteroide


# variables
ANCHO = 480
ALTO = 700
listaAsteroides = []
puntos = 0


# booleano para que se ejecute el juego
jugando = True


def cargarAsteroides(x, y):
    meteoro = asteroide.Asteroide(x, y)
    listaAsteroides.append(meteoro)

def gameOver():
    global jugando
    jugando = False
    for meteorito in listaAsteroides:
        listaAsteroides.remove(meteorito)

# funcion principal
def meteoritos():
    pygame.init()
    ventana = pygame.display.set_mode((ANCHO, ALTO))
    contador = 0
    # imagen de fondo
    fondo = pygame.image.load('images/fondo.png')
    # titulo
    pygame.display.set_caption('Meteoritos')
    # crear objeto jugador
    nave = jugador.Nave()
    # sonidos
    # pygame.mixer.music.load('sounds/fondo.wav')
    # pygame.mixer.music.play(-1)
    # sonidoColision = pygame.mixer.Sound('sounds/colision.aiff')
    # fuente del marcador
    global puntos
    fuenteMarcador = pygame.font.SysFont('Arial', 25)
    # ciclo
    while True:
        ventana.blit(fondo, (0, 0))
        nave.dibujar(ventana)
        # tiempo
        tiempo = process_time()
        # Marcador
        textoMarcador = fuenteMarcador.render('Puntos: '+str(puntos), True, (120, 240, 12))
        ventana.blit(textoMarcador, (0, 0))

        if tiempo - contador > 1:
            contador = tiempo
            posX = randint(2, 478)
            cargarAsteroides(posX, 0)

        if len(listaAsteroides) > 0:
            for x in listaAsteroides:
                if jugando:
                    x.dibujar(ventana)
                    x.recorrido()
                    if x.rect.top > 700:
                        listaAsteroides.remove(x)
                    else:
                        if x.rect.colliderect(nave.rect):
                            listaAsteroides.remove(x)
                            # sonidoColision.play()
                            nave.vida = False
                            gameOver()

        if len(nave.listaDisparo) > 0:  # la listaDisparo es para cuando hay mas de un disparo proyectandose a la vez
            for x in nave.listaDisparo:
                x.dibujar(ventana)  # lo dibujamos
                x.recorrido()  # hacemos que haga el recorrido
                if x.rect.top < -10:  # para cuando salga de la ventana, se lo elimina de la lista
                    nave.listaDisparo.remove(x)
                else:
                    for meteorito in listaAsteroides:
                        if x.rect.colliderect(meteorito.rect):
                            listaAsteroides.remove(meteorito)
                            nave.listaDisparo.remove(x)
                            puntos += 1
        nave.mover()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if jugando:
                    if event.key == K_SPACE:
                        x, y = nave.rect.center  # el disparo debe salir desde el centro de la nave
                        nave.disparar(x, y)
        if jugando:
            keys = pygame.key.get_pressed()
            nave.rect.x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * nave.velocidad

            # elif event.type == pygame.KEYDOWN:
            #     if jugando:
            #         if event.key == K_LEFT:
            #             nave.rect.left -= nave.velocidad  # para que se mueva acorde a su velocidad
            #         elif event.key == K_RIGHT:
            #             nave.rect.right += nave.velocidad
            #         elif event.key == K_SPACE:
            #             x, y = nave.rect.center  # el disparo debe salir desde el centro de la nave
            #             nave.disparar(x, y)

        if not jugando:
            fuenteGameOver = pygame.font.SysFont('Arial', 40)
            textoGameOver = fuenteGameOver.render('GAME OVER', True, (120, 240, 12))
            ventana.blit(textoGameOver, (140, 350))
            # pygame.mixer.music.fadeout(3000)  # cuando comprobemos el final del juego, para la musica
        pygame.display.update()


meteoritos()
