import pygame
from clases import disparo


class Nave(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imagenNave = pygame.image.load("images/nave.png")
        self.imagenExplota = pygame.image.load("images/naveExplota.png")

        self.rect = self.imagenNave.get_rect()

        # posicion inicial de la nave
        self.rect.centerx = 240
        self.rect.centery = 690

        self.velocidad = 2
        self.vida = True
        self.listaDisparo = []
        self.sonidoDisparo = pygame.mixer.Sound('sounds/disparo.wav')

    def mover(self):
        if self.vida:
            if self.rect.left <= 0:
                self.rect.left = 0
            elif self.rect.right > 490:
                self.rect.right = 490

    def disparar(self, x, y):
        if self.vida:
            misil = disparo.Misil(x, y)
            self.listaDisparo.append(misil)
            # self.sonidoDisparo.play()

    def dibujar(self, superficie):
        if self.vida:
            superficie.blit(self.imagenNave, self.rect)
        else:
            superficie.blit(self.imagenExplota, self.rect)