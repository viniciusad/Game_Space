import pygame
from random import randint
pygame.init()

a = 0
b = -550  # Fundo
x = 330
y = 100  # Nave Principal
pos_x = 100
pos_y = 400  # Tie-Fighter
pos_a = 560
pos_b = 100  # Asteroide Direita
pos_a2 = 330
pos_b2 = 500  # Asteroide Central
timer = 0
tempo_segundo = 0

musica = 'musica-tema.mp3'

pygame.mixer.init()
pygame.mixer.music.load(musica)
pygame.mixer.music.play(-1)

velocidade_nave = 12
velocidade_tie = 5
velocidade_asteroide = 3

fundo = pygame.image.load('tela.png')
nave = pygame.image.load('falcon.png')
tie = pygame.image.load('tie.png')
asteroide = pygame.image.load('asteroide.png')
asteroide2 = pygame.image.load('asteroide2.png')

font = pygame.font.SysFont('Bauhaus 93', 30)
texto = font.render("Tempo: ", True, (0, 200, 0), (0, 0, 0))
pos_texto = texto.get_rect()
pos_texto.center = (60, 20)

janela = pygame.display.set_mode((800, 600))
pygame.display.set_caption(
    "Space Asteroids | Controle pelas teclas 'W, A, S, D'")

janela_aberta = True
while janela_aberta:
    pygame.time.delay(2)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            janela_aberta = False
        sair = pygame.key.get_pressed()
        if sair[pygame.K_ESCAPE]:
            janela_aberta = False

    comandos = pygame.key.get_pressed()
    if comandos[pygame.K_w] and y >= 0:
        y -= velocidade_nave
    if comandos[pygame.K_s] and y <= 415:
        y += velocidade_nave
    if comandos[pygame.K_d] and x <= 660:
        x += velocidade_nave
    if comandos[pygame.K_a] and x >= 0:
        x -= velocidade_nave

    if ((x + 135 > pos_a and y + 110 > pos_b)):
        x = 100

    if ((x - 125 < pos_x and y + 110 > pos_y)):
        x = 330

    if ((x + 100 > pos_a2 and y - 110 < pos_b2)) and ((x - 100 < pos_a2 and y + 110 > pos_b2)):
        x = 560

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
    janela.blit(nave, (x, y))
    janela.blit(tie, (pos_x, pos_y))
    janela.blit(asteroide, (pos_a, pos_b))
    janela.blit(asteroide2, (pos_a2, pos_b2))
    janela.blit(texto, pos_texto)

    pygame.display.update()
pygame.quit()
