import pygame
import os
import math


pygame.init()
pygame.font.init()
vec = pygame.math.Vector2

#Main Character
MAIN_CHARACTER = pygame.image.load(os.path.join('Main Characters', 'Main Character.png'))
MC_WEAPON = pygame.image.load(os.path.join('Main Characters', 'Main With Bat1.png'))


#Movement Animation
right1 = pygame.image.load(os.path.join('Main Characters','Main Character-Walking_Left1.png'))
right2 = pygame.image.load(os.path.join('Main Characters','Main Character-Walking_Left2.png'))
right3 = pygame.image.load(os.path.join('Main Characters','Main Character-Walking_Left3.png'))
movingRight = [right1, right2, right3]
left1 = pygame.transform.flip(right1, True, False)
left2 = pygame.transform.flip(right2, True, False)
left3 = pygame.transform.flip(right3, True, False)
movingLeft = [left1, left2, left3]
down1 = pygame.image.load(os.path.join('Main Characters','Main Character-Walking_Down1.png'))
down2 = pygame.image.load(os.path.join('Main Characters','Main Character-Walking_Down2.png'))
down3 = pygame.image.load(os.path.join('Main Characters','Main Character-Walking_Down3.png'))
down4 = pygame.image.load(os.path.join('Main Characters','Main Character-Walking_Down4.png'))
down5 = pygame.image.load(os.path.join('Main Characters','Main Character-Walking_Down5.png'))
movingDown = [down1, down2, down3, down4, down5]
up1 = pygame.transform.flip(down1, False, True)
up2 = pygame.transform.flip(down2, False, True)
up3 = pygame.transform.flip(down3, False, True)
up4 = pygame.transform.flip(down4, False, True)
up5 = pygame.transform.flip(down5, False, True)
movingUp = [up1, up2, up3, up4, up5]

WALK = 0

#Attack Animation
attack1 = pygame.image.load(os.path.join('Main Characters', 'Main With Bat2.png'))
attack2 = pygame.image.load(os.path.join('Main Characters', 'Main With Bat3.png'))
attack3 = pygame.image.load(os.path.join('Main Characters', 'Main With Bat4.png'))
attack4 = pygame.image.load(os.path.join('Main Characters', 'Main With Bat5.png'))
attack5 = pygame.image.load(os.path.join('Main Characters', 'Main With Bat6.png'))
attack6 = pygame.image.load(os.path.join('Main Characters', 'Main With Bat7.png'))

attacking = [attack1, attack2, attack2, attack4, attack5, attack6]

ATTACK = 0

#Wall Tile
Hos_Wall = pygame.image.load(os.path.join('Game Tiles','Game_Wall.png'))
Game_Wall = pygame.image.load(os.path.join('Game Tiles', 'Wall.png'))
Game_Brick = pygame.image.load(os.path.join('Game Tiles', 'Brick.png'))
Game_Glass = pygame.image.load(os.path.join('Game Tiles', 'Glass.png'))

#Doors
LockedDoor = pygame.image.load(os.path.join('Game Tiles','Locked_Door.png'))

#Floor Tiles
Hos_Floor = pygame.image.load(os.path.join('Game Tiles','Game_Floor.png'))

#Fire
FIRE = pygame.image.load(os.path.join('Game Tiles', 'Fire.png'))

#Inventory
INVENTORY = pygame.image.load('Game_Inventory.png')

#Items
gamekey = pygame.image.load(os.path.join('Game Items','Game_Key.png'))
gamefuse = pygame.image.load(os.path.join('Game Items', 'Game_Fuse.png'))
HOOKEDCABLE = pygame.image.load(os.path.join('Game Items','HookedCable.png'))
UNHOOKEDCABLE = pygame.image.load(os.path.join('Game Items','UnhookedCable.png'))                            
Bat_level1 = pygame.image.load(os.path.join('Game Items', 'Level 1 Bat.png'))
HEALTH_POTION = pygame.image.load(os.path.join('Game Items', 'Health Potion.png'))
COIN = pygame.image.load(os.path.join('Game Items','Coin.png'))
Bat_Vending_Machine_lvl1 = pygame.image.load(os.path.join('Game Items', 'Bat Vending Machine.png'))
Bat_Vending_Machine_lvl2 = pygame.image.load(os.path.join('Game Items', 'Bat Vending Machine Level 2.png'))
ARMOUR = pygame.image.load(os.path.join('Game Items', 'Armour Potion.png'))
SUPER_POTION = pygame.image.load(os.path.join('Game Items', 'Super Potion.png'))
KEY = pygame.image.load(os.path.join('Game Items', 'Key.png'))
Strength_potion = pygame.image.load(os.path.join('Game Items', 'Strength Potion.png'))

#Font
score = pygame.font.SysFont('Arial', 20)

class Character(pygame.sprite.Sprite):
    def __init__(self,player, screen, x, y, groupA, groupB, groupC, groupD):
        self.groups = player.all_sprites, player.players
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.player = player
        self.screen = screen
        self.image = MAIN_CHARACTER
        self.rect = self.image.get_rect()
        self.inventory = []
        self.x = x
        self.y = y
        self.up = -1
        self.down = 1
        self.right = 1
        self.left = -1
        self.damage = 5
        self.health = 100
        self.AttackRange = 132
        self.MaxHealth = 100
        '''armour adds to this value allowing the user to heal up to higher health'''
        self.in_GhostAttackRange = False
        self.in_DogAttackRange = False
        self.in_ClownAttackRange = False
        self.in_BossAttackRange = False
        self.groupA = groupA
        self.groupB = groupB
        self.groupC = groupC
        self.groupD = groupD
        #self.groupE = groupE
        self.coins = 0
        self.keys = []
        
    def update(self):
        self.rect.x = self.x * 32
        self.rect.y = self.y * 32
        
        '''if self.health == 0:
            self.health = 100'''
        ghost_hit = pygame.sprite.groupcollide(self.groupB, self.groupA, False, False)
        #for enemy in self.player.enemies:
        for enemy in ghost_hit:
            enemyX = enemy.x *32
            enemyY = enemy.y *32
            dis = math.sqrt((self.rect.x - enemyX)**2 + (self.rect.y - enemyY)**2)
            if dis < self.AttackRange:
                self.in_GhostAttackRange = True
                
            if dis > self.AttackRange:
                self.in_GhostAttackRange = False
                
        dog_hit = pygame.sprite.groupcollide(self.groupC, self.groupA, False, False)
        for dog in dog_hit:
            dogX = dog.x *32
            dogY = dog.y *32
            dis = math.sqrt((self.rect.x - dogX)**2 + (self.rect.y - dogY)**2)
            if dis < self.AttackRange:
                self.in_DogAttackRange = True
                
            if dis > self.AttackRange:
                self.in_DogAttackRange = False

        clown_hit = pygame.sprite.groupcollide(self.groupD, self.groupA, False, False)
        for clown in clown_hit:
            clownX = clown.x *32
            clownY = clown.y *32

            dis = math.sqrt((self.rect.x - clownX)**2 + (self.rect.y - clownY)**2)
            if dis < self.AttackRange:
                self.in_ClownAttackRange = True
                
            if dis > self.AttackRange:
                self.in_ClownAttackRange = False
                
        '''Add more groups and just do this again and again for each group'''
    def health_bar(self):
        pygame.draw.rect(self.screen, (255,0,0), (0,0, 100, 20))
        pygame.draw.rect(self.screen, (0,128,0), (0,0, 100 - (1 * (100-self.health)), 20))
        scoreboard = score.render('Coins: ' + str(self.coins), True, (255,0,0))
        self.screen.blit(scoreboard, (550, 0))

    def inventory_bar(self):
        self.screen.blit(INVENTORY, (160,608))
        
    #Movement Commands       
    def move_up(self):
        global WALK
        
        if WALK + 1 >= 5:
            WALK = 0
            
        if not self.collide(0,self.up) and not self.LD_collide(0, self.up) and not self.Brick_collide(0, self.up) and not self.Glass_collide(0, self.up):
            self.y += self.up
            self.image = movingUp[WALK//1]
            WALK += 1
        elif self.LD_collide(0, self.up):
            for item in self.inventory:
                if isinstance(item, Key):
                    self.inventory.remove(item)
                    self.y += self.up
                    self.image = movingUp[WALK//1]
                    WALK += 1
            
    def move_down(self):
        global WALK
        
        if WALK + 1 >= 5:
            WALK = 0
            
        if not self.collide(0, self.down) and not self.LD_collide(0, self.down) and not self.Brick_collide(0, self.down) and not self.Glass_collide(0, self.down):
            self.y += self.down
            self.image = movingDown[WALK//1]
            WALK += 1
        elif self.LD_collide(0, self.down):
            for item in self.inventory:
                if isinstance(item, Key):
                    self.inventory.remove(item)
                    self.y += self.down
                    self.image = movingDown[WALK//1]
                    WALK += 1

    def move_right(self):
        global WALK
        
        if WALK + 1 >= 3:
            WALK = 0
            
        if not self.collide(self.right,0) and not self.LD_collide(self.right, 0) and not self.Brick_collide(self.right, 0) and not self.Glass_collide(self.right, 0):
            self.x += self.right
            self.image = movingRight[WALK//1]
            WALK += 1
        elif self.LD_collide(self.right, 0):
            for item in self.inventory:
                if isinstance(item, Key):
                    self.inventory.remove(item)
                    self.x += self.right
                    self.image = movingUp[WALK//1]
                    WALK += 1
            
    def move_left(self):
        global WALK
        
        if WALK + 1 >= 3:
            WALK = 0
            
        if not self.collide(self.left, 0) and not self.LD_collide(self.left, 0) and not self.Brick_collide(self.left, 0) and not self.Glass_collide(self.left, 0):
            self.x += self.left
            self.image = movingLeft[WALK//1]
            WALK += 1
        elif self.LD_collide(self.left, 0):
            for item in self.inventory:
                if isinstance(item, Key):
                    self.inventory.remove(item)
                    self.x += self.left
                    self.image = movingLeft[WALK//1]
                    WALK += 1
            
            
    def standing(self):
        global WALK
        self.image = MAIN_CHARACTER
        WALK = 0
                
    def ghost_hit(self):
        global ATTACK

        if ATTACK + 1 >= 6:
            ATTACK = 0
            
        ghost_hits  = pygame.sprite.groupcollide(self.groupB, self.groupA, False, False)
        for hit in ghost_hits:
            hit.health -= self.damage
            self.image = attacking[ATTACK//1] #Different attacking animation
            ATTACK += 1
                
    def dog_hit(self):
        global ATTACK

        if ATTACK + 1 >= 6:
            ATTACK = 0
        
        dog_hits = pygame.sprite.groupcollide(self.groupC, self.groupA, False, False)
        for hit in dog_hits:
            hit.health -= self.damage
            self.image = attacking[ATTACK//1]
            ATTACK += 1

    def clown_hit(self):
        global ATTACK

        if ATTACK + 1 >= 6:
            ATTACK = 0
            
        clown_hits = pygame.sprite.groupcollide(self.groupD, self.groupA, False, False)
        for hit in clown_hits:
            hit.health -= self.damage
            self.image = attacking[ATTACK//1]
            ATTACK += 1

    def Boss_hit(self):
        pass

        '''Add more groups and just do this again and again for each group'''
                
    #Wall Collision
    def collide(self,dx,dy):
        for wall in self.player.walls:
            if self.x + dx == wall.x and self.y + dy == wall.y :
                return True
        return False
    
    #Door Collision
    def LD_collide(self, dx, dy):
        for LD in self.player.LockedDoors:
            if self.x + dx == LD.x and self.y + dy == LD.y:
                return True
        return False
    
    #Glass Collision
    def Glass_collide(self, dx, dy):
        for glass in self.player.glass:
            if self.x + dx == glass.x and self.y + dy == glass.y:
                return True
        return False
    
    #Brick Collision
    def Brick_collide(self, dx, dy):
        for brick in self.player.bricks:
            if self.x + dx == brick.x and self.y + dy == brick.y:
                return True
        return False
    
    #Add health
    def add_health(self, amount):
        self.health += amount
        if self.health > self.MaxHealth:
            self.health = self.MaxHealth
    #Add Armour
    def add_armour(self, amount):
        self.MaxHealth += amount
        if self.MaxHealth > 150:
            self.MaxHealth = 150

    #Player Death
    def player_death(self):
        pass

class Wall(pygame.sprite.Sprite):
    def __init__(self, player, x, y):
        self.groups = player.all_sprites, player.walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.player = player
        self.image = Game_Wall
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * 32
        self.rect.y = y * 32

class Brick(pygame.sprite.Sprite):
    def __init__(self, player, x, y):
        self.groups = player.all_sprites, player.bricks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.player = player
        self.image = Game_Brick
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * 32
        self.rect.y = y * 32

class Glass(pygame.sprite.Sprite):
    def __init__(self, player, x, y):
        self.groups = player.all_sprites, player.glass
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.player = player
        self.image = Game_Glass
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * 32
        self.rect.y = y * 32

class Key(pygame.sprite.Sprite):
    def __init__(self, player,png, x, y):
        self.groups = player.all_sprites, player.keys
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.player = player
        self.png = png
        self.image = pygame.image.load(os.path.join('Game Items', png))
        self.rect = self.image.get_rect()
        self.x = x 
        self.y = y
        self.rect.x = x*32
        self.rect.y = y*32
 
class Weapon(pygame.sprite.Sprite):
    def __init__(self, player,png, x, y):
        self.groups = player.all_sprites, player.weapons
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.player = player
        self.png = png
        self.image = pygame.image.load(os.path.join('Game Items', png))
        self.rect = self.image.get_rect()
        self.x = x 
        self.y = y
        self.rect.x = x*32
        self.rect.y = y*32
        
class Level2_Weapon(pygame.sprite.Sprite):
    def __init__(self, player,png):
        self.groups = player.all_sprites, player.weapons_lvl2
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.player = player
        self.png = png
        self.image = pygame.image.load(os.path.join('Game Items', png))
        self.rect = self.image.get_rect()
        #self.x = x 
        #self.y = y
        #self.rect.x = x*32
        #self.rect.y = y*32
        
class Level3_Weapon(pygame.sprite.Sprite):
    def __init__(self, player,png):
        self.groups = player.all_sprites, player.weapons_lvl3
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.player = player
        self.png = png
        self.image = pygame.image.load(os.path.join('Game Items', png))
        self.rect = self.image.get_rect()
        #self.x = x 
        #self.y = y
        #self.rect.x = x*32
        #self.rect.y = y*32
        
class Crowbar(pygame.sprite.Sprite):
    def __init__(self, player,png, x, y):
        self.groups = player.all_sprites, player.crowbars
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.player = player
        self.png = png
        self.image = pygame.image.load(os.path.join('Game Items', png))
        self.rect = self.image.get_rect()
        self.x = x 
        self.y = y
        self.rect.x = x*32
        self.rect.y = y*32

class Locked_Door(pygame.sprite.Sprite):
    def __init__(self, player, x, y):
        self.groups = player.all_sprites, player.LockedDoors
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.player = player
        self.image = LockedDoor
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x*32
        self.rect.y = y*32

class Health(pygame.sprite.Sprite):
    def __init__(self, player, x, y):
        self.groups = player.all_sprites, player.health
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.player = player
        self.image = HEALTH_POTION
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x*32
        self.rect.y = y*32

class Super_Health(pygame.sprite.Sprite):
    def __init__(self, player, x, y):
        self.groups = player.all_sprites, player.super_health
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.player = player
        self.image = SUPER_POTION
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x*32
        self.rect.y = y*32
        
class Coin(pygame.sprite.Sprite):
    def __init__(self, player, x, y):
        self.groups = player.all_sprites, player.coin
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.player = player
        self.image = COIN
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x*32
        self.rect.y = y*32

class Armour(pygame.sprite.Sprite):
    def __init__(self, player, x, y):
        self.groups = player.all_sprites, player.armour
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.player = player
        self.image = ARMOUR
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x*32
        self.rect.y = y*32
        
class Bat_Vending_lvl1(pygame.sprite.Sprite):
    def __init__(self, player, x, y):
        self.groups = player.all_sprites, player.B_vendings_lvl1
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.player = player
        self.image = Bat_Vending_Machine_lvl1
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x*32
        self.rect.y = y*32

class Bat_Vending_lvl2(pygame.sprite.Sprite):
    def __init__(self, player, x, y):
        self.groups = player.all_sprites, player.B_vendings_lvl2
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.player = player
        self.image = Bat_Vending_Machine_lvl2
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x*32
        self.rect.y = y*32

class Seven_key(pygame.sprite.Sprite):
    def __init__(self, player, x, y):
        self.groups = player.all_sprites, player.game_keys
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.player = player
        self.image = KEY
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x*32
        self.rect.y = y*32
        
class Strength_Potion(pygame.sprite.Sprite):
    def __init__(self, player, x, y):
        self.groups = player.all_sprites, player.strength
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.player = player
        self.image = Strength_potion
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x*32
        self.rect.y = y*32
        
class Fire(pygame.sprite.Sprite):
    def __init__(self, player, x, y):
        self.groups = player.all_sprites, player.fire
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.player = player
        self.image = FIRE
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x*32
        self.rect.y = y*32

        
        
        
