import pygame
import random
import math
from pygame import mixer
pygame.init()


screen = pygame.display.set_mode((800,600))

background=pygame.image.load('background.jpg')

mixer.music.load('sp1.mp3')
mixer.music.play(-1)

pygame.display.set_caption("Space Invaders")
icon=pygame.image.load('ufo.png')
pygame.display.set_icon(icon)


playerImg=pygame.image.load('space-invaders.png')
playerX=370
playerY=480
playerX_change=0
playerY_change=0


enemyImg=[]
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]
no_of_enemies=6
for i in range(no_of_enemies):
    enemyImg.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(4)
    enemyY_change.append(20)

bulletImg=pygame.image.load('bullet.png')
bulletX=0
bulletY=480
bulletX_change=0
bulletY_change=10
bullet_state="ready"

score=0
font = pygame.font.Font('freesansbold.ttf',32)
textX=10
textY=10

over_font=pygame.font.Font('freesansbold.ttf',64)


def show_score(x,y):
    scores=font.render("Score :"+ str(score),True, (255,255,255))
    screen.blit(scores,(x,y))

def game_over():
    over_text=over_font.render("GAME OVER",True, (255,255,255))
    screen.blit(over_text,(200,250))

def player(x,y):
    screen.blit(playerImg,(x,y))


def enemy(x,y,i):
    screen.blit(enemyImg[i], (x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state="fire"
    screen.blit(bulletImg, (x+16,y+10))

def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance=math.sqrt((math.pow(enemyX-bulletX,2))+(math.pow(enemyY-bulletY,2)))
    if distance<27:
        return True
    else:
        return False

running=True

while running:
    screen.fill((0, 0, 0))
    screen.blit(background,(0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
           
        if event.type== pygame.KEYDOWN:
            if event.key ==pygame.K_LEFT:
                playerX_change= -5
            if event.key==pygame.K_RIGHT:
                playerX_change=5
            if event.key==pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound=mixer.Sound('lg1.mp3')
                    bullet_sound.play()
                    bulletX=playerX
                    fire_bullet(bulletX,bulletY)

                
        if event.type==pygame.KEYUP:
            if event.key ==pygame.K_LEFT or event.key== pygame.K_RIGHT:
                playerX_change=0
    playerX+=playerX_change
    if playerX <=0:
        playerX=0
    elif playerX>=736:
        playerX=736
    for i in range(no_of_enemies):
        if enemyY[i]>440:
            for j in range(no_of_enemies):
                enemyY[j]=2000
            game_over()
            break
        enemyX[i] +=enemyX_change[i]
        if enemyX[i] <=0:
            enemyX_change[i]=2
            enemyY[i] +=enemyY_change[i]
        elif enemyX[i]>=736:
            enemyX_change[i]=-2
            enemyY[i] +=enemyY_change[i]
        collision=isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            explosion_sound=mixer.Sound('ms1.mp3')
            explosion_sound.play()
            bulletY=480
            bullet_state="ready"
            score+=1
            enemyX[i]=random.randint(0,735)
            enemyY[i]=random.randint(50,150)
        enemy(enemyX[i],enemyY[i],i)
    if bulletY <=0:
        bulletY=480
        bullet_state="ready"

    if bullet_state is "fire":
        fire_bullet(bulletX,bulletY)
        bulletY-= bulletY_change
    

    player(playerX,playerY)
    show_score(textX,textY)
    pygame.display.update()