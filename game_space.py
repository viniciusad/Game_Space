import pygame
import sys
from random import randint
from pygame.locals import *

pygame.init()

WIDTH, HEIGHT = 800, 600

a = 0
b = -550  # Fundo

# Posiciona inimigos de forma aleatória
pos_x = randint(0, WIDTH - 100)
pos_y = randint(HEIGHT + 100, HEIGHT + 300)  # Tie-Fighter
pos_a = randint(0, WIDTH - 100)
pos_b = randint(100, HEIGHT + 200)  # Asteroide Direita
pos_a2 = randint(0, WIDTH - 100)
pos_b2 = randint(-300, -100)  # Asteroide Central

timer = 0
tempo_segundo = 0
game_over = False

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
big_font = pygame.font.SysFont('Bauhaus 93', 50)
texto = font.render("Tempo: ", True, (0, 200, 0), (0, 0, 0))
pos_texto = texto.get_rect()
pos_texto.center = (60, 20)
restart_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 50, 200, 50)

janela = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(
    "Game Space | Controle pelo Mouse")

clock = pygame.time.Clock()

def reset_game():
    global pos_x, pos_y, pos_a, pos_b, pos_a2, pos_b2, tempo_segundo, timer, game_over
    tempo_segundo = 0
    timer = 0
    pos_x = randint(0, WIDTH - 100)
    pos_y = randint(HEIGHT + 100, HEIGHT + 300)
    pos_a = randint(0, WIDTH - 100)
    pos_b = randint(HEIGHT, HEIGHT + 300)
    pos_a2 = randint(0, WIDTH - 100)
    pos_b2 = randint(-300, -100)
    game_over = False


while True:
    mx, my = pygame.mouse.get_pos()
    nave_rect = nave.get_rect(center=(mx, my))
    tie_rect = tie.get_rect(topleft=(pos_x, pos_y))
    ast_rect = asteroide.get_rect(topleft=(pos_a, pos_b))
    ast2_rect = asteroide2.get_rect(topleft=(pos_a2, pos_b2))

    rot = 0
    if click:
        rot -= 90
    if Rclick:
        rot += 180
    if Mclick:
        rot += 90

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                if game_over and restart_rect.collidepoint(event.pos):
                    reset_game()
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

    janela.blit(fundo, (a, b))

    if not game_over:
        # Movimentacao dos Objetos
        if pos_b <= -10:
            pos_b = randint(HEIGHT, HEIGHT + 300)
            pos_a = randint(0, WIDTH - 100)
        if pos_y <= -10:
            pos_y = randint(HEIGHT, HEIGHT + 300)
            pos_x = randint(0, WIDTH - 100)
        if pos_b2 >= HEIGHT:
            pos_b2 = randint(-300, -100)
            pos_a2 = randint(0, WIDTH - 100)
        if b >= 0:
            b = -550

        if timer < 60:
            timer += 1
        else:
            tempo_segundo += 1
            texto = font.render("Tempo: "+str(tempo_segundo), True, (0, 200, 0), (0, 0, 0))
            timer = 0

        b += velocidade_nave - 11
        pos_y -= velocidade_tie
        pos_b -= velocidade_asteroide + 3
        pos_b2 += velocidade_asteroide

        if nave_rect.colliderect(tie_rect) or nave_rect.colliderect(ast_rect) or nave_rect.colliderect(ast2_rect):
            game_over = True

        janela.blit(pygame.transform.rotate(nave, rot), (mx-70, my-70))
        janela.blit(tie, (pos_x, pos_y))
        janela.blit(asteroide, (pos_a, pos_b))
        janela.blit(asteroide2, (pos_a2, pos_b2))
        janela.blit(texto, pos_texto)
    else:
        score = big_font.render(f"Score: {tempo_segundo}s", True, (255, 255, 255))
        score_rect = score.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
        restart_text = font.render("Reiniciar", True, (255, 255, 255))
        pygame.draw.rect(janela, (50, 50, 50), restart_rect)
        janela.blit(restart_text, restart_text.get_rect(center=restart_rect.center))
        janela.blit(score, score_rect)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
