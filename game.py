#Игра "Звездный защитник"


import pygame, random, sys
from pygame.locals import *

#Создание экрана
WINDOWWIDTH = 800
WINDOWHEIGHT = 600
TEXTCOLOR = (255, 0, 0)
BACKGROUNDCOLOR = (0, 0, 0)

#Количество кадров в сек
FPS = 60

#Падающие спрайты: Злодеи
BADDIEMINSIZE = 10
BADDIEMAXSIZE = 40
BADDIEMINSPEED = 1
BADDIEMAXSPEED = 6
ADDNEWBADDIERATE = 6

PLAYERMOVERATE = 10

# Добавление паузы и завершение игры
def terminate():
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # Нажатие ESC осуществляет выход.
                    terminate()
                return

#Если произошло столкновение со злодеем
def playerHasHitBaddie(playerRect, baddies):
    for b in baddies:
        if playerRect.colliderect(b['rect']):
            return True
    return False

#Тексты в игре
def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

##############################################################

# Настройка pygame, окна и указателя мыши.
pygame.init()
mainClock = pygame.time.Clock()
#windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption('Ловкач Гоша')
pygame.mouse.set_visible(False)

# Настройка шрифтов.
font = pygame.font.SysFont(None, 35)

'''
# Настройка звуков.
gameOverSound = pygame.mixer.Sound('gameover.wav')
pygame.mixer.music.load('background.mid')
'''
# Настройка изображений.
playerImage = pygame.image.load('player.png')
playerRect = playerImage.get_rect()
baddieImage = pygame.image.load('baddie.png')

# Вывод начального экрана.
windowSurface.fill(BACKGROUNDCOLOR)
drawText('Звездный защитник', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
drawText('Нажмите клавишу для начала игры', font, windowSurface, (WINDOWWIDTH / 5) - 30, (WINDOWHEIGHT / 3) + 50)
pygame.display.update()
waitForPlayerToPressKey()

topScore = 0
while True:
    # Настройка начала игры.
    baddies = []
    score = 0
    playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50)
    moveLeft = moveRight = moveUp = moveDown = False
    reverseCheat = slowCheat = False
    baddieAddCounter = 0
    #pygame.mixer.music.play(-1, 0.0)

    while True: # Игровой цикл выполняется, пока игра работает.
        score += 1 # Увеличение количества очков.

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == K_z:
                    reverseCheat = True
                if event.key == K_x:
                    slowCheat = True


            if event.type == KEYUP:
                if event.key == K_z:
                    reverseCheat = False
                    score = 0
                if event.key == K_x:
                    slowCheat = False
                    score = 0
                if event.key == K_ESCAPE:
                    terminate()

            if event.type == MOUSEMOTION:
            # Если мышь движется, переместить игрока к указателю мыши.
                playerRect.centerx = event.pos[0]
                playerRect.centery = event.pos[1]

        # Если необходимо, добавить новых злодеев в верхнюю часть экрана.
        if not reverseCheat and not slowCheat:  
            baddieAddCounter += 1
        if baddieAddCounter == ADDNEWBADDIERATE:
            baddieAddCounter = 0
            baddieSize = random.randint(BADDIEMINSIZE, BADDIEMAXSIZE)
            newBaddie={'rect':pygame.Rect(random.randint(0,WINDOWWIDTH-baddieSize),0-baddieSize,baddieSize,baddieSize),
                                    'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                                'surface':pygame.transform.scale(baddieImage, (baddieSize, baddieSize)),
                                    }

            baddies.append(newBaddie)

        # Перемещение игрока по экрану.
        if moveLeft and playerRect.left > 0:
             playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
        if moveRight and playerRect.right < WINDOWWIDTH:
            playerRect.move_ip(PLAYERMOVERATE, 0)
        if moveUp and playerRect.top > 0:
            playerRect.move_ip(0, -1 * PLAYERMOVERATE)
        if moveDown and playerRect.bottom < WINDOWHEIGHT:
            playerRect.move_ip(0, PLAYERMOVERATE)

        # Перемещение злодеев вниз.
        for b in baddies:
            if not reverseCheat and not slowCheat:
                b['rect'].move_ip(0, b['speed'])

            elif reverseCheat:
                b['rect'].move_ip(0, -5)
            elif slowCheat:
                b['rect'].move_ip(0, 1)


        # Удаление злодеев, упавших за нижнюю границу экрана.
        for b in baddies[:]:
            if b['rect'].top > WINDOWHEIGHT:
                baddies.remove(b)

        # Отображение в окне игрового мира.
        windowSurface.fill(BACKGROUNDCOLOR)

        # Отображение количества очков и лучшего результата.
        drawText('Счет: %s' % (score), font, windowSurface, 10, 0)
        drawText('Рекорд: %s' % (topScore), font, windowSurface, 10, 40)

        # Отображение прямоугольника игрока.
        windowSurface.blit(playerImage, playerRect)

        # Отображение каждого злодея.
        for b in baddies:
            windowSurface.blit(b['surface'], b['rect'])

        pygame.display.update()

        # Проверка, попал ли в игрока какой-либо из злодеев.
        if playerHasHitBaddie(playerRect, baddies):
            if score > topScore:
                topScore = score # установка нового рекорда
            break

        mainClock.tick(FPS)
# Отображение игры и вывод надписи 'Игра окончена'.
#pygame.mixer.music.stop()
#gameOverSound.play()

drawText('ИГРА ОКОНЧЕНА!', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
drawText('Нажмите клавишу для начала новой игры', font, windowSurface, (WINDOWWIDTH / 3) - 120, (WINDOWHEIGHT / 3) + 50)
pygame.display.update()
waitForPlayerToPressKey()


gameOverSound.stop()