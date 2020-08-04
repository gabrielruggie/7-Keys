import pygame
import os
import math
from sprites import *

vec = pygame.math.Vector2
#Enemies
#GHOST_ENEMY = pygame.image.load(os.path.join('Main Characters', 'Ghost.png'))
#new = pygame.transform.flip(GHOST_ENEMY, True, False)

SITTING_GHOST1 = pygame.image.load(os.path.join('Main Characters', 'Sitting Ghost1.png'))
SITTING_GHOST2 = pygame.image.load(os.path.join('Main Characters', 'Sitting Ghost2.png'))
SITTING_GHOST3 = pygame.image.load(os.path.join('Main Characters', 'Sitting Ghost3.png'))
SITTING_GHOST4 = pygame.image.load(os.path.join('Main Characters', 'Sitting Ghost4.png'))
SITTING_GHOST5 = pygame.image.load(os.path.join('Main Characters', 'Sitting Ghost5.png'))
SITTING_GHOST6 = pygame.image.load(os.path.join('Main Characters', 'Sitting Ghost6.png'))
sitting = [SITTING_GHOST1, SITTING_GHOST1, SITTING_GHOST1, SITTING_GHOST1, SITTING_GHOST2, SITTING_GHOST2,
           SITTING_GHOST2, SITTING_GHOST2, SITTING_GHOST3, SITTING_GHOST3, SITTING_GHOST3, SITTING_GHOST3,
           SITTING_GHOST4, SITTING_GHOST4, SITTING_GHOST4, SITTING_GHOST4, SITTING_GHOST5, SITTING_GHOST5,
           SITTING_GHOST5, SITTING_GHOST5, SITTING_GHOST6, SITTING_GHOST6, SITTING_GHOST6, SITTING_GHOST6]
SIT = 0

MOVING_GHOST1 = pygame.image.load(os.path.join('Main Characters', 'Sinister Ghost1.png'))
MOVING_GHOST2 = pygame.image.load(os.path.join('Main Characters', 'Sinister Ghost2.png'))
moving = [MOVING_GHOST1, MOVING_GHOST1, MOVING_GHOST1, MOVING_GHOST1, MOVING_GHOST1,
          MOVING_GHOST1, MOVING_GHOST1, MOVING_GHOST2, MOVING_GHOST2, MOVING_GHOST2,
          MOVING_GHOST2, MOVING_GHOST2, MOVING_GHOST2, MOVING_GHOST2, MOVING_GHOST2,
          MOVING_GHOST2, MOVING_GHOST2]
MOVE = 0

DOG = pygame.image.load(os.path.join('Main Characters', 'Guard Dog.png'))
DOG_FLIP = pygame.transform.flip(DOG, True, False)

CLOWN = pygame.image.load(os.path.join('Main Characters', 'Standing_Clown.png'))
ANGRY_CLOWN = pygame.image.load(os.path.join('Main Characters', 'Angry Clown.png'))
ANGRY_CLOWN2 = pygame.transform.flip(ANGRY_CLOWN, True, False)

class Ghost(pygame.sprite.Sprite):
    def __init__(self, player, screen, x, y):
        self.groups = player.all_sprites, player.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.player = player
        self.screen = screen
        self.image = SITTING_GHOST1
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x*32
        self.rect.y = y*32
        self.range = 120
        self.inRange = False
        self.health = 40
        self.damage = 1
        self.speed_index = 1.1
        
        
    def update(self):
        global SIT
        global MOVE
        
        
        for player in self.player.players:
            playerX = player.x *32
            playerY = player.y *32
            dis = math.sqrt((self.rect.x - playerX)**2 + (self.rect.y - playerY)**2)
            if dis < self.range:
                if MOVE + 1 >= 17:
                    MOVE = 0
                self.image = moving[MOVE//1]
                MOVE += 1
                self.move(player)
            if dis > self.range:
                if SIT + 1 >= 24:
                    SIT = 0
            
                self.image = sitting[SIT//1]
                SIT += 1
        if self.health <= 0:
            self.kill()
                
    def move(self, player):
        dx, dy = player.x * 32 - self.rect.x, player.y * 32 - self.rect.y

        dist = math.hypot(dx, dy)
        if dist != 0:
            dx, dy = dx/dist, dy/dist

            self.rect.x += dx * self.speed_index
            self.rect.y += dy * self.speed_index
        else:
            for player in self.player.players:
                self.attack(player)
            dx, dy = 0,0

    def attack(self, player):
        player.health = player.health - self.damage
    


class Dog(pygame.sprite.Sprite):
    def __init__(self, player, x, y):
        self.groups = player.all_sprites, player.dogs
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.player = player
        self.image = DOG
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x*32
        self.rect.y = y*32
        self.health = 20
        self.damage = 4
        self.range = 132
        self.inRange = False
        self.speed_index = 1.4

        self.dx = 0
        self.dy = 0

    def update(self):

        for player in self.player.players:
            playerX = player.x *32
            playerY = player.y *32
            dis = math.sqrt((self.rect.x - playerX)**2 + (self.rect.y - playerY)**2)
            if dis < self.range:
                self.move(player)
                
        if self.health <= 0:
            self.kill()
            
                        
    def move(self, player):
        dx, dy = player.x * 32 - self.rect.x, player.y * 32 - self.rect.y
        dist = math.hypot(dx, dy)
        collide = pygame.sprite.spritecollideany(self, self.player.walls, False)
        collide2 = pygame.sprite.spritecollideany(self, self.player.LockedDoors, False)
        
        if dist != 0:
            dx, dy = dx/dist, dy/dist
            
            self.rect.x += dx * self.speed_index
            self.rect.y += dy * self.speed_index

            if collide:
                self.rect.x -= dx * self.speed_index
                self.rect.y -= dy * self.speed_index

            if collide2:
                self.rect.x -= dx * self.speed_index
                self.rect.y -= dy * self.speed_index
                    
            if dx > 0:
                self.image = DOG_FLIP
            else:
                self.image = DOG
        else:
            self.attack(player)
            dx, dy = 0,0


    def attack(self, player):
        player.health -= self.damage
        

class Clown(pygame.sprite.Sprite):
    def __init__(self, player, x, y):
        self.groups = player.all_sprites, player.clowns 
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.player = player
        self.image = CLOWN
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x*32
        self.rect.y = y*32
        self.health = 60
        self.damage = 2
        self.range = 120
        self.inRange = False
        self.speed_index = 1
        
    def update(self):
        global SIT
        global MOVE
        
        
        for player in self.player.players:
            playerX = player.x *32
            playerY = player.y *32
            dis = math.sqrt((self.rect.x - playerX)**2 + (self.rect.y - playerY)**2)
            if dis < self.range:
                self.move(player)
                self.image = ANGRY_CLOWN
            else:
                self.image = CLOWN
                
        if self.health <= 0:
            self.kill()


    def move(self, player):
        dx, dy = player.x * 32 - self.rect.x, player.y * 32 - self.rect.y
        dist = math.hypot(dx, dy)
        collide = pygame.sprite.spritecollideany(self, self.player.walls, False)
        collide2 = pygame.sprite.spritecollideany(self, self.player.LockedDoors, False)

        if dist != 0:
            
            dx, dy = dx/dist, dy/dist
                
            self.rect.x += dx * self.speed_index
            self.rect.y += dy * self.speed_index
            
            if collide:
                self.rect.x -= dx * self.speed_index
                self.rect.y -= dy * self.speed_index
            if collide2:
                self.rect.x -= dx * self.speed_index
                self.rect.y -= dy * self.speed_index
                
        else:
            for player in self.player.players:
                self.attack(player)
            dx, dy = 0,0
    
    def attack(self, player):
        player.health -= self.damage


class BOSS(pygame.sprite.Sprite):
    def __init__(self, player, x, y):
        self.groups = player.all_sprite, player.boss
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.player = player
        self.image = None
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x*32
        self.rect.y = y*32
        self.health = 200
        self.range = 100
        self.inRange = False
        self.damage = 8
        self.speed_index = 1.1
