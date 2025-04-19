import pygame as pg
import pyganim
import os

from Super_Mario_boy.blocks import ICON_DIR
from count_collector.params import WIDTH, HEIDHT

MOVE_SPEED = 7
WIDTH = 22
HEIDHT = 32
COLOR = "#888888"
JUMP_POWER = 10
GRAVITY = 0.35
ANIMATION_DELAY = 0.1
ICON_DIR = os.path.dirname(__file__)

ANIMATION_RIGHT = [
    ('%s/mario/r1.png' % ICON_DIR),
('%s/mario/r2.png' % ICON_DIR),
('%s/mario/r3.png' % ICON_DIR),
('%s/mario/r4.png' % ICON_DIR),
('%s/mario/r5.png' % ICON_DIR),
]

ANIMATION_LEFT = [
    ('%s/mario/l1.png' % ICON_DIR),
('%s/mario/l2.png' % ICON_DIR),
('%s/mario/l3.png' % ICON_DIR),
('%s/mario/l4.png' % ICON_DIR),
('%s/mario/l5.png' % ICON_DIR),
]
ANIMATION_JUMP_LEFT = [('%s/mario/jl.png' % ICON_DIR, 0.1)]
ANIMATION_JUMP_RIGHT = [('%s/mario/jr.png' % ICON_DIR, 0.1)]
ANIMATION_JUMP = [('%s/mario/j.png' % ICON_DIR, 0.1)]
ANIMATION_STAY = [('%s/mario/0.png' % ICON_DIR, 1)]

class Player(pg.Sprite):
    def __init__(self,x,y):
        pg.sprite.Sprite.__init__(self)
        self.xvel = 0 #Скорость перемещения, 0 - стоять на месте
        self.yvel = 0 #скорость вертикального перемещения

        #стартовая позиция игрока
        self.startX = x
        self.startY = y

        self.on_ground = False #на земле ли я?

        self.image = pg.Surface((WIDTH, HEIDHT))
        self.image.fill(pg.Color(COLOR))
        self.image.set_colorkey(pg.Color(COLOR)) #делаем фон прозрачным


        self.rect = pg.Rect(x,y, WIDTH, HEIDHT) #ля удобства объект должен быть квадратным

        #Анимации
        boltAnim = []
        for a in ANIMATION_RIGHT:
            boltAnim.append((a, ANIMATION_DELAY))
        self.boltAnimRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimRight.play()

        boltAnim = []
        for a in ANIMATION_LEFT:
            boltAnim.append((a, ANIMATION_DELAY))
        self.boltAnimLeft= pyganim.PygAnimation(boltAnim)
        self.boltAnimLeft.play()

        self.boltAnimStay = pyganim.PygAnimation(ANIMATION_STAY)
        self.boltAnimStay.play()
        self.boltAnimStay.blit(self.image, (0, 0)) #По-умолчанию - стоим

        self.boltAnimJumpLeft = pyganim.PygAnimation(ANIMATION_STAY)
        self.boltAnimJumpLeft.play()

        self.boltAnimJumpRight = pyganim.PygAnimation(ANIMATION_STAY)
        self.boltAnimJumpRight.play()

        self.boltAnimJump = pyganim.PygAnimation(ANIMATION_STAY)
        self.boltAnimJump.play()

    def update(self, left, right, up, platforms):

        if up:
            if self.on_ground:
                self.yvel = -JUMP_POWER
            self.image.fill(pg.Color(COLOR))
            self.boltAnimJump.blit(self.image, (0,0))

        if left:
            self.xvel = -MOVE_SPEED
            self.image.fill(pg.Color(COLOR))

            if up:
                self.boltAnimLeft.blit(self.image, (0, 0))
            else:
                self.boltAnimLeft.blit(self.image, (0,0))

        if right:
            self.xvel = -MOVE_SPEED
            self.image.fill(pg.Color(COLOR))

            if up:
                self.boltAnimRight.blit(self.image, (0, 0))
            else:
                self.boltAnimRight.blit(self.image, (0, 0))


        if not (left or right):
            self.xvel = 0
            if not up:
                self.image.fill(pg.Color(COLOR))
                self.boltAnimStay.blit(self.image, (0,0))

        if not self.on_ground:
            self.yvel += GRAVITY

        self.on_ground = False

        self.rect.y += self.yvel
        self.collide(0, self.yvelm, platforms)

        self.tect.x += self.xvel
        self.collide(self.xvel, 0, platforms)

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if pg.sprite.collide_rect(self, p):

                if xvel > 0:
                    self.rect.right = p.rect.left
                if xvel > 0:
                    self.rect.left = p.rect.right

                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.on_ground = True
                    self.yvel = 0
                if yvel < 0:
                    self.rect.top = p.rect.bottom
                    self.yvel = 0

