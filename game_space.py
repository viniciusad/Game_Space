import pygame
import sys
from random import randint
from pygame.locals import *

pygame.init()

# Tamanho da tela um pouco maior para dar mais espaco ao jogador
WIDTH, HEIGHT = 960, 720

# Variaveis de deslocamento do fundo
a = 0
b = 0  # ajustado apos carregar o fundo

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

# Controle de movimento mais suave
ship_pos = [WIDTH // 2, HEIGHT // 2]

# Listas para lasers e explosoes
lasers = []
explosoes = []
laser_speed = 8
power_level = 0
proximo_power = 10


pygame.mixer.init()
pygame.mixer.music.load('assets/musica-tema.mp3')
pygame.mixer.music.play(-1)

velocidade_nave = 12
velocidade_tie = 5
velocidade_asteroide = 3

fundo = pygame.image.load('assets/tela.png')
# Ajusta o fundo para o tamanho da tela mantendo proporcao
fundo = pygame.transform.scale(fundo, (WIDTH, fundo.get_height()))
# Posiciona o fundo para que ocupe toda a tela
b = HEIGHT - fundo.get_height()

# Imagens reduzidas para aumentar a area livre
scale_factor = 0.7
nave = pygame.transform.rotozoom(pygame.image.load('assets/falcon.png'), 0, scale_factor)
tie = pygame.transform.rotozoom(pygame.image.load('assets/tie.png'), 0, scale_factor)
asteroide = pygame.transform.rotozoom(pygame.image.load('assets/asteroide.png'), 0, scale_factor)
asteroide2 = pygame.transform.rotozoom(pygame.image.load('assets/asteroide2.png'), 0, scale_factor)
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


def fire_lasers(center):
    """Cria lasers de acordo com o nivel de poder atual."""
    for i in range(power_level):
        offset = (i - (power_level - 1) / 2) * 15
        rect = pygame.Rect(center[0] + offset - 2, center[1] - 30, 4, 15)
        lasers.append(rect)


def update_power():
    global power_level, proximo_power
    if tempo_segundo >= proximo_power:
        if power_level == 0:
            power_level = 1
        else:
            power_level *= 2
        proximo_power *= 2

def reset_game():
    global pos_x, pos_y, pos_a, pos_b, pos_a2, pos_b2
    global tempo_segundo, timer, game_over, ship_pos, lasers, explosoes
    global power_level, proximo_power
    tempo_segundo = 0
    timer = 0
    pos_x = randint(0, WIDTH - 100)
    pos_y = randint(HEIGHT + 100, HEIGHT + 300)
    pos_a = randint(0, WIDTH - 100)
    pos_b = randint(HEIGHT, HEIGHT + 300)
    pos_a2 = randint(0, WIDTH - 100)
    pos_b2 = randint(-300, -100)
    game_over = False
    ship_pos = [WIDTH // 2, HEIGHT // 2]
    lasers.clear()
    explosoes.clear()
    power_level = 0
    proximo_power = 10


while True:
    shooting = False
    mx, my = pygame.mouse.get_pos()
    nave_rect = nave.get_rect(center=(int(ship_pos[0]), int(ship_pos[1])))
    tie_rect = tie.get_rect(topleft=(pos_x, pos_y))
    ast_rect = asteroide.get_rect(topleft=(pos_a, pos_b))
    ast2_rect = asteroide2.get_rect(topleft=(pos_a2, pos_b2))

    rot = 0

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
                else:
                    shooting = True
            if event.button == 3 and game_over:
                reset_game()
        if event.type == KEYDOWN:
            if event.key == K_SPACE and not game_over:
                shooting = True

    janela.blit(fundo, (a, b))

    if not game_over:
        # atualiza posicao suavemente em direcao ao mouse
        ship_pos[0] += (mx - ship_pos[0]) * 0.2
        ship_pos[1] += (my - ship_pos[1]) * 0.2
        nave_rect = nave.get_rect(center=(int(ship_pos[0]), int(ship_pos[1])))

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
            b = HEIGHT - fundo.get_height()

        if timer < 60:
            timer += 1
        else:
            tempo_segundo += 1
            texto = font.render("Tempo: "+str(tempo_segundo), True, (0, 200, 0), (0, 0, 0))
            timer = 0
            update_power()

        b += velocidade_nave - 11
        pos_y -= velocidade_tie
        pos_b -= velocidade_asteroide + 3
        pos_b2 += velocidade_asteroide

        if shooting and power_level > 0:
            fire_lasers(nave_rect.center)

        # Atualiza lasers
        for laser in list(lasers):
            laser.y -= laser_speed
            if laser.y < -20:
                lasers.remove(laser)
            else:
                if laser.colliderect(tie_rect):
                    explosoes.append({'pos': tie_rect.center, 'timer': 10})
                    pos_y = randint(HEIGHT, HEIGHT + 300)
                    pos_x = randint(0, WIDTH - 100)
                    lasers.remove(laser)
                elif laser.colliderect(ast_rect):
                    explosoes.append({'pos': ast_rect.center, 'timer': 10})
                    pos_b = randint(HEIGHT, HEIGHT + 300)
                    pos_a = randint(0, WIDTH - 100)
                    lasers.remove(laser)
                elif laser.colliderect(ast2_rect):
                    explosoes.append({'pos': ast2_rect.center, 'timer': 10})
                    pos_b2 = randint(-300, -100)
                    pos_a2 = randint(0, WIDTH - 100)
                    lasers.remove(laser)

        if nave_rect.colliderect(tie_rect) or nave_rect.colliderect(ast_rect) or nave_rect.colliderect(ast2_rect):
            game_over = True

        for laser in lasers:
            pygame.draw.rect(janela, (255, 0, 0), laser)

        for exp in list(explosoes):
            pygame.draw.circle(janela, (255, 100, 0), exp['pos'], 20 - exp['timer'])
            exp['timer'] -= 1
            if exp['timer'] <= 0:
                explosoes.remove(exp)

        janela.blit(pygame.transform.rotate(nave, rot), nave_rect.topleft)
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
