#Controle apenas pelas teclas "W, A, S, D"
import pygame
from random import randint
#Definindo música
music = 'musica-tema.mp3'
pygame.init()
#Configurando música de fundo
pygame.mixer.init()
pygame.mixer.music.load(music)
pygame.mixer.music.play(-1)     #Definindo loop infinito da música
#Definindo Objetos
a = 0
b = -550        #Fundo
x = 400
y = 100         #Nave Principal
pos_x = 120
pos_y = 400     #Tie-Fighter
pos_a = 650
pos_b = 100     #Asteroide Direita
pos_a2 = 400
pos_b2 = 500    #Asteroide Central 
timer = 0
tempo_segundo = 0
#Velocidade dos objetos
velocidade_nave = 12
velocidade_tie = 6
velocidade_asteroide = 4
#Design dos objetos
fundo = pygame.image.load('tela.png')
nave = pygame.image.load('falcon.png')
tie = pygame.image.load('tie.png')
asteroide = pygame.image.load('asteroide.png')
asteroide2 = pygame.image.load('asteroide2.png')

#Timer
font = pygame.font.SysFont('Bauhaus 93',30)
texto = font.render("Tempo: ",True,(0,200,0),(0,0,0))
pos_texto = texto.get_rect()
pos_texto.center = (60,20)

#Tamanho da janela e título
janela = pygame.display.set_mode((900,600))
pygame.display.set_caption("Space Asteroids | Controle pelas teclas 'W, A, S, D'")
#Definindo parametros para a janela se manter aberta até usuário decidir fechar
janela_aberta = True
while janela_aberta :
    pygame.time.delay(2)  #frame de atualização da tela. Em milisegundos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            janela_aberta = False
        sair = pygame.key.get_pressed()
        if sair[pygame.K_ESCAPE]:
            janela_aberta = False

#Configurando movimentação da nave principal
#Limitando movimentação até determinado ponto da tela
    comandos = pygame.key.get_pressed()
    if comandos[pygame.K_w] and y >= 0:
        y -= velocidade_nave
    if comandos[pygame.K_s] and y <= 400:
        y += velocidade_nave
    if comandos[pygame.K_d] and x <= 750:
        x += velocidade_nave
    if comandos[pygame.K_a] and x >= 10:
        x -= velocidade_nave

#Configurando colisão lado DIREITO
    if ((x + 140 > pos_a and y + 150 > pos_b)):
        x=400

#Configurando colisão lado ESQUERDO
    if ((x - 140 < pos_x and y + 150 > pos_y)):
        x=400

#Configurando colisão no CENTRO
    if ((x + 140 > pos_a2 and y - 150 < pos_b2)) and ((x - 140 < pos_a2 and y + 150 > pos_b2)):
        x=600

#Movimentação dos Objetos
    #Asteroide Direita
    if (pos_b <= -200):
        pos_b = randint (800,1000)
    #Tie-Fighter
    if ((pos_y <= -400)): 
        pos_y = randint (600,2000)
    #Asteroide Central
    if ((pos_b2 >= 1000)):
        pos_b2 = randint (-500,-150)

#Movimentação Tie-Fighter
#    if ((pos_y <= -180)):
#        pos_y = randint (600,2000)
#Configurando colisão com nave principal
#    if ((x + 140 > pos_a and y + 182 > pos_b)):
#        x=400
#Movimentação Asteroide
#    if ((pos_b <= -180)):
#        pos_b = randint (800,1000)
#Movimentação Asteroide2
#    if (pos_b2 >= 1000):
#        pos_b2 = randint (-500,-150)
#Movimentação Fundo
    if (b >= 0):
        b = -550

#Configurando Timer
    if (timer <60):
        timer +=1
    else:
        tempo_segundo +=1
        texto = font.render("Tempo: "+str(tempo_segundo),True,(0,200,0),(0,0,0))
        timer = 0

#Incrementando ou decrementando o movimento dos objetos, para que se movam continuamente
    b += velocidade_nave - 11
    pos_y -= velocidade_tie
    pos_b -= velocidade_asteroide + 3
    pos_b2 += velocidade_asteroide

#Exibir na janela o posicionamento dos objetos
    janela.blit(fundo,(a,b))
    janela.blit(nave,(x,y))
    janela.blit(tie,(pos_x, pos_y))
    janela.blit(asteroide,(pos_a, pos_b))
    janela.blit(asteroide2,(pos_a2, pos_b2))
    janela.blit(texto,pos_texto)

    pygame.display.update()
pygame.quit()