import pygame
import sys
import math
from random import randint
from pygame.locals import *

pygame.init()

# Tamanho da tela ampliado
WIDTH, HEIGHT = 1280, 960

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

# Controle de movimento mais suave e angulo da nave
ship_pos = [WIDTH // 2, HEIGHT // 2]
ship_angle = 0
prev_mouse = ship_pos[:]

# Listas para lasers e explosoes
lasers = []
explosoes = []
laser_speed = 8
# tempo do campo de forca (em frames)
force_field_timer = 0
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


def fire_lasers(center, angle):
    """Cria lasers de acordo com o nivel de poder atual e direcao da nave."""
    rad = math.radians(angle)
    # vetor perpendicular para espalhar lasers
    perp = rad + math.pi / 2
    for i in range(power_level):
        offset = (i - (power_level - 1) / 2) * 15
        x = center[0] + math.cos(rad) * 30 + math.cos(perp) * offset
        y = center[1] - math.sin(rad) * 30 - math.sin(perp) * offset
        rect = pygame.Rect(x - 2, y - 8, 4, 15)
        lasers.append({'rect': rect, 'dx': math.cos(rad), 'dy': -math.sin(rad)})


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
    global power_level, proximo_power, ship_angle, prev_mouse, force_field_timer
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
    ship_angle = 0
    prev_mouse = ship_pos[:]
    lasers.clear()
    explosoes.clear()
    power_level = 0
    proximo_power = 10
    force_field_timer = 0


while True:
    shooting = False
    mx, my = pygame.mouse.get_pos()
    mouse_dx = mx - prev_mouse[0]
    mouse_dy = my - prev_mouse[1]
    mouse_speed = math.hypot(mouse_dx, mouse_dy)
    prev_mouse[0], prev_mouse[1] = mx, my
    nave_rect = nave.get_rect(center=(int(ship_pos[0]), int(ship_pos[1])))
    tie_rect = tie.get_rect(topleft=(pos_x, pos_y))
    ast_rect = asteroide.get_rect(topleft=(pos_a, pos_b))
    ast2_rect = asteroide2.get_rect(topleft=(pos_a2, pos_b2))

    target_angle = math.degrees(math.atan2(-(my - ship_pos[1]), mx - ship_pos[0]))
    delta = (target_angle - ship_angle + 180) % 360 - 180
    rot_speed = 0.05 + min(0.45, mouse_speed * 0.01)
    ship_angle += delta * rot_speed
    rot = ship_angle

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
            fire_lasers(nave_rect.center, rot)
            force_field_timer = 120  # 2 segundos a 60fps

        # Atualiza lasers
        for laser in list(lasers):
            laser['rect'].x += laser['dx'] * laser_speed
            laser['rect'].y += laser['dy'] * laser_speed
            if (laser['rect'].right < 0 or laser['rect'].left > WIDTH or
                    laser['rect'].bottom < 0 or laser['rect'].top > HEIGHT):
                lasers.remove(laser)
            else:
                if laser['rect'].colliderect(tie_rect):
                    explosoes.append({'pos': tie_rect.center, 'timer': 10})
                    pos_y = randint(HEIGHT, HEIGHT + 300)
                    pos_x = randint(0, WIDTH - 100)
                    lasers.remove(laser)
                elif laser['rect'].colliderect(ast_rect):
                    explosoes.append({'pos': ast_rect.center, 'timer': 10})
                    pos_b = randint(HEIGHT, HEIGHT + 300)
                    pos_a = randint(0, WIDTH - 100)
                    lasers.remove(laser)
                elif laser['rect'].colliderect(ast2_rect):
                    explosoes.append({'pos': ast2_rect.center, 'timer': 10})
                    pos_b2 = randint(-300, -100)
                    pos_a2 = randint(0, WIDTH - 100)
                    lasers.remove(laser)

        if nave_rect.colliderect(tie_rect) or nave_rect.colliderect(ast_rect) or nave_rect.colliderect(ast2_rect):
            game_over = True

        for laser in lasers:
            pygame.draw.rect(janela, (255, 0, 0), laser['rect'])

        for exp in list(explosoes):
            pygame.draw.circle(janela, (255, 100, 0), exp['pos'], 20 - exp['timer'])
            exp['timer'] -= 1
            if exp['timer'] <= 0:
                explosoes.remove(exp)

        rotated_nave = pygame.transform.rotate(nave, rot)
        rot_rect = rotated_nave.get_rect(center=nave_rect.center)
        if force_field_timer > 0:
            radius = max(rot_rect.width, rot_rect.height) // 2 + 10
            aura = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
            pygame.draw.circle(aura, (255, 255, 255, 128), (radius, radius), radius)
            janela.blit(aura, aura.get_rect(center=rot_rect.center))
            force_field_timer -= 1
        janela.blit(rotated_nave, rot_rect.topleft)
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
