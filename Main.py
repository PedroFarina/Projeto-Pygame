import pygame
import time
import sys
import random

#Containers e fontes
pygame.init()
pygame.font.init()
pygame.mixer.pre_init()
pygame.mixer.init()
screen = pygame.display.set_mode([400,400])
#Sons
pygame.mixer.music.load("Sons/theme.mp3")
pygame.mixer.music.play()
rSound = pygame.mixer.Sound("Sons/reload.ogg")
cSound = pygame.mixer.Sound("Sons/clip.ogg")
fSound = pygame.mixer.Sound("Sons/fire.ogg")

fontGrande = pygame.font.Font("Fontes/FonteGame.ttf", 30)
fontNormal = pygame.font.SysFont('Comis Sans MS', 15)
textNormal = "PRESSIONE [ENTER] PARA INICIAR O JOGO"
textGrande = " "
#Imagens de background
lImages = (pygame.image.load("Imagens/bg1.jpg"), pygame.image.load("Imagens/bg2.jpg"), pygame.image.load("Imagens/bg3.jpg"), pygame.image.load("Imagens/bg4.jpg"))
lRects = []
rectBackground = lImages[0].get_rect()
rectBackground.left, rectBackground.top = [0,0]
#Vilões
 #Imagens de vilões
lbgImages = (pygame.image.load("Imagens/badguy01.png"),pygame.image.load("Imagens/badguy02.png"), pygame.image.load("Imagens/miniboss.png"), pygame.image.load("Imagens/boss.png"))
lbgRects = []
 #Vilões ativos
lEnemies = []
#Variaveis controladoras
morto = False
keep = [] #Lista com cada tecla que permanece sendo pressionada
d4Background = random.randint(0,3)
bullets = 30
reloading = False
highscore = []
difficulty = 0
MaxEnemies = 3
#Passo do jogo
clock = pygame.time.Clock()
pygame.time.set_timer(pygame.USEREVENT + 5, 1000) #Mostrando tempo de jogo
tempoJogo = 0
spawnTime = 2000
#Pontuação
killed = 0

while True:
    screen.fill([255, 255, 255])
    screen.blit(lImages[d4Background], rectBackground)
    if difficulty != 0:
        for Enemy in lEnemies:
            screen.blit(Enemy[0], Enemy[1])
        for event in pygame.event.get():
            eType = event.type
            if eType == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif eType == pygame.USEREVENT + 1: #Terminar reload
                reloading = False
                pygame.time.set_timer(pygame.USEREVENT + 1, 0)
            elif eType == pygame.USEREVENT + 2: #Aumentar dificuldade
                difficulty += 1
                MaxEnemies = 3 * difficulty
            elif eType == pygame.USEREVENT + 3: #Spawnar inimigo
                spawnTime = max(2000 - (difficulty * 200), 200)
                if len(lEnemies) < MaxEnemies:
                    d4BadGuys = random.randint(0, min(difficulty, len(lbgImages) - 1))
                    bgImage = lbgImages[d4BadGuys].copy()
                    bgRect = bgImage.get_rect()
                    bgRect.left, bgRect.top = [random.randint(1,150) * 2, random.randint(50,150) * 2]
                    lEnemies.append([bgImage, bgRect,  random.randint(50 + (10 * difficulty), 100 + (10 * difficulty))])
                    if len(lEnemies) > 4:
                        textGrande = "DEFEAT!"
                        pygame.time.set_timer(pygame.USEREVENT + 4, 1000)
                        highscore.append(killed)
                        lEnemies = []
                        tempoJogo = 0
                        textNormal = "PRESSIONE [ENTER] PARA TENTAR NOVAMENTE"
                        pygame.time.set_timer(pygame.USEREVENT + 2, 0)
                        difficulty = 0
            elif eType == pygame.USEREVENT + 5: #Mostrar tempo de jogo
                tempoJogo += 1
            elif eType == pygame.KEYDOWN:  #KEYDOWN
                k = event.key
                apend = False
                if k == pygame.K_ESCAPE:                          #Sair do jogo
                    pygame.quit()
                    sys.exit()
                elif k == pygame.K_LEFT or k == pygame.K_RIGHT:   #Mudar de cenário
                    d4a = d4Background
                    while d4Background == d4a:
                        d4Background = random.randint(0,3)
                elif k == pygame.K_r:                             #Recarregar arma
                    bullets = 30
                    reloading = True
                    rSound.play()
                    textNormal = ""
                    textGrande = ""
                    pygame.time.set_timer(pygame.USEREVENT + 1, 1000)
                if apend:
                    keep.append(k)
            elif event.type == pygame.KEYUP:    #KEYUP
                k = event.key
                if k in keep:
                    keep.remove(k)
            elif event.type == pygame.MOUSEBUTTONDOWN:            #TIRO
                if event.button == 1:
                    keep.append(pygame.K_LCTRL)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if pygame.K_LCTRL in keep:
                        keep.remove(pygame.K_LCTRL)
        for keys in keep:
            if keys == pygame.K_LCTRL and not(reloading):
                if bullets < 10:
                    textNormal = "Low ammo."
                if bullets > 0:
                    bullets -= 1
                    fSound.play()
                    pos = pygame.mouse.get_pos()
                    shadowEnemies = lEnemies
                    for bg in shadowEnemies:
                        if bg[1].collidepoint(pos):
                            vida = bg[2]
                            vida -= (24 + random.randint(0,7))
                            if vida <= 0:
                                lEnemies.remove(bg)
                                killed += 1
                            bg[2] = vida
                else:
                    cSound.play()
                    textNormal = ""
                    textGrande = "RELOAD!"
    else:
        for event in pygame.event.get():
            eType = event.type
            if eType == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif eType == pygame.USEREVENT + 4:
                textGrande = ""
                morto = True
            elif eType == pygame.KEYDOWN:
                if event.key == 13:
                    morto = False
                    difficulty = 1
                    killed = 0
                    bullets = 30
                    textGrande = ""
                    textNormal = ""
                    pygame.time.set_timer(pygame.USEREVENT + 2, 5000) #Aumentando a dificuldade
                    pygame.time.set_timer(pygame.USEREVENT + 3, spawnTime) #Spawnar inimigo
        if morto:
            txtsHighscore = []
            textHigh = "Highscore:"
            loc = [70, 200]
            highscore.sort()
            highscore.reverse()
            txtsHighscore.append(fontGrande.render(textHigh, True, (220, 220, 0)))
            for pontuacao in highscore:
                txtsHighscore.append(fontGrande.render(str(pontuacao), True, (220, 220, 0)))
                locatual = 0
            for txt in txtsHighscore:
                screen.blit(txt, [loc[0], (loc[1] + (locatual * 30))])
                loc[0] = 180
                locatual += 1
    txtNormal = fontNormal.render(textNormal, True, (255,255,255))
    txtGrande = fontGrande.render(textGrande, True, (255,0,0))
    txtScore = fontGrande.render("Score: " + str(killed), True, (220,220,0))
    txtTempo = fontGrande.render(str(tempoJogo) + "s", True, (255, 255, 255))
    screen.blit(txtNormal, (80, 350))
    screen.blit(txtGrande, (100, 200))
    screen.blit(txtScore, (20, 20))
    screen.blit(txtTempo, (320, 20))
    clock.tick(8)
    pygame.display.update()
