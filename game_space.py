import pygame
import sys
from random import randint
from pygame.locals import *
pygame.init()

a = 0
b = -550  # Fundo
# x = 330
# y = 100  # Nave Principal
pos_x = 100
pos_y = 400  # Tie-Fighter
pos_a = 560
pos_b = 100  # Asteroide Direita
pos_a2 = 330
pos_b2 = 500  # Asteroide Central
timer = 0
tempo_segundo = 0

offset = [0, 0]
click = False
Rclick = False
Mclick = False

pygame.mixer.init()
pygame.mixer.music.load('assets/musica-tema.mp3')
pygame.mixer.music.play(-1)

velocidade_nave = 12
velocidade_tie = 5
velocidade_asteroide = 3

fundo = pygame.image.load('assets/tela.png')
nave = pygame.image.load('assets/falcon.png')
tie = pygame.image.load('assets/tie.png')
asteroide = pygame.image.load('assets/asteroide.png')
asteroide2 = pygame.image.load('assets/asteroide2.png')
icone = pygame.image.load('assets/GameSpace.ico')
pygame.display.set_icon(icone)

font = pygame.font.SysFont('Bauhaus 93', 30)
texto = font.render("Tempo: ", True, (0, 200, 0), (0, 0, 0))
pos_texto = texto.get_rect()
pos_texto.center = (60, 20)

janela = pygame.display.set_mode((800, 600))
pygame.display.set_caption(
    "Game Space | Controle pelo Mouse")

while True:
    rot = 0
    mx, my = pygame.mouse.get_pos()
    position = [mx, my]
    if click:
        rot -= 90
    if Rclick:
        rot += 180
    if Mclick:
        rot += 90
    janela.blit(pygame.transform.rotate(nave, rot),
                (position[0] + offset[0], position[1] + offset[1]))

    Rclick = False
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                click = True
            if event.button == 3:
                Rclick = True
            if event.button == 2:
                Mclick = not Mclick
            if event.button == 4:
                offset[1] -= 10
            if event.button == 5:
                offset[1] += 10

        if event.type == MOUSEBUTTONUP:
            if event.button == 1:
                click = False

# ------------ TESTE COLISÃO --------------
    # limite = pygame.mouse.get_pos()
    # if (nave, (mx-70, my-70)) and y >= 0:
    #     y -= velocidade_nave
    # if (nave, (mx-70, my-70)) and y <= 415:
    #     y += velocidade_nave
    # if (nave, (mx-70, my-70)) and x <= 660:
    #     x += velocidade_nave
    # if (nave, (mx-70, my-70)) and x >= 0:
    #     x -= velocidade_nave

    # if ((mx + 135 > pos_a and my + 110 > pos_b)):
    #     mx = 100

    # if ((mx - 125 < pos_x and my + 110 > pos_y)):
    #     mx = 330

    # if ((mx + 100 > pos_a2 and my - 110 < pos_b2)) and ((mx - 100 < pos_a2 and my + 110 > pos_b2)):
    #     mx = 560
# ------------ TESTE COLISÃO --------------

    # Movimentação dos Objetos
    # Asteroide Direita
    if (pos_b <= -10):
        pos_b = randint(1500, 2000)
    # Tie-Fighter
    if ((pos_y <= -10)):
        pos_y = randint(1000, 1500)
    # Asteroide Central
    if ((pos_b2 >= 700)):
        pos_b2 = randint(-800, -250)
    # Plano de Fundo
    if (b >= 0):
        b = -550

    if (timer < 60):
        timer += 1
    else:
        tempo_segundo += 1
        texto = font.render("Tempo: "+str(tempo_segundo),
                            True, (0, 200, 0), (0, 0, 0))
        timer = 0

    b += velocidade_nave - 11
    pos_y -= velocidade_tie
    pos_b -= velocidade_asteroide + 3
    pos_b2 += velocidade_asteroide

    janela.blit(fundo, (a, b))
    janela.blit(nave, (mx-70, my-70))
    janela.blit(tie, (pos_x, pos_y))
    janela.blit(asteroide, (pos_a, pos_b))
    janela.blit(asteroide2, (pos_a2, pos_b2))
    janela.blit(texto, pos_texto)

    pygame.display.update()
pygame.quit()
