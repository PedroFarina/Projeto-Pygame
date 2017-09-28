import pygame
import time
import sys
import random

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode([400,400])

font = pygame.font.SysFont('Comis Sans MS', 15)
text = "PRESSIONE [ENTER] PARA INICIAR O JOGO"
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
keep = [] #Lista com cada tecla que permanece sendo pressionada
d4Background = random.randint(0,3)
bullets = 30
reloading = False
difficulty = 0
MaxEnemies = 3
#Passo do jogo
clock = pygame.time.Clock()
spawnTime = 2000

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
                print("OK")
            elif eType == pygame.USEREVENT + 2: #Aumentar dificuldade
                difficulty += 1
                MaxEnemies = 3 * difficulty
            elif eType == pygame.USEREVENT + 3: #Spawnar inimigo
                spawnTime = max(2000 - (difficulty * 200), 200)
                if len(lEnemies) < MaxEnemies:
                    d4BadGuys = random.randint(0, min(difficulty, len(lbgImages) - 1))
                    bgImage = lbgImages[d4BadGuys].copy()
                    bgRect = bgImage.get_rect()
                    bgRect.left, bgRect.top = [random.randint(1,150) * 2, random.randint(1,150) * 2]
                    lEnemies.append([bgImage, bgRect, difficulty * random.randint(50, 100)])
            elif event.type == pygame.KEYDOWN:  #KEYDOWN
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
                    text = ""
                    pygame.time.set_timer(pygame.USEREVENT + 1, 1000)
                if apend:
                    keep.append(k)
            elif event.type == pygame.KEYUP:    #KEYUP
                k = event.key
                if k in keep:
                    keep.remove(k)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    keep.append(pygame.K_LCTRL)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    keep.remove(pygame.K_LCTRL)
        for keys in keep:
            if keys == pygame.K_LCTRL and not(reloading):
                if bullets < 10:
                    text = "Low ammo."
                if bullets > 0:
                    bullets -= 1
                    pos = pygame.mouse.get_pos()
                    shadowEnemies = lEnemies
                    for bg in shadowEnemies:
                        if bg[1].collidepoint(pos):
                            vida = bg[2]
                            vida -= (24 + random.randint(0,7))
                            print(vida)
                            if vida <= 0:
                                lEnemies.remove(bg)
                            bg[2] = vida
                else:
                    text = "RELOAD!"
    else:
        for event in pygame.event.get():
            eType = event.type
            if eType == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif eType == pygame.KEYDOWN:
                if event.key == 13:
                    difficulty = 1
                    text = ""
                    pygame.time.set_timer(pygame.USEREVENT + 2, 5000) #Aumentando a dificuldade
                    pygame.time.set_timer(pygame.USEREVENT + 3, spawnTime) #Spawnar inimigo
    txt = font.render(text, True, (255,255,255))
    screen.blit(txt, (80, 350))
    clock.tick(8)
    pygame.display.update()
