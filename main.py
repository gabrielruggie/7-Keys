import pygame
import os
import sys
from sprites import *
from camera import *
from enemies import *

#Initiation
w,h = 640,640
TILESIZE = 32
TITLE = '7 Keys'

#Characters
MC_WEAPON = pygame.image.load(os.path.join('Main Characters', 'Main With Bat1.png'))


#items
gamekey = pygame.image.load(os.path.join('Game Items','Game_Key.png'))
HOOKEDCABLE = pygame.image.load(os.path.join('Game Items','HookedCable.png'))
UNHOOKEDCABLE = pygame.image.load(os.path.join('Game Items','UnhookedCable.png'))

#Game Floor
Floor = pygame.image.load(os.path.join('Game Tiles','GameFloor.png'))
Floor_test = pygame.image.load(os.path.join('Game Tiles', 'Floor_test.png'))
Floor_test2 = pygame.image.load('Final Floor Test.png')

#Start Screen
start = pygame.image.load('Start Screen Alpha.png')
controls = pygame.image.load('Controls.png')



class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((w,h))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        pygame.key.set_repeat(500,100)
        self.load()
        
        
    def load(self):
        self.map = Map('Beta_Map.txt')

    
    def new_char(self):
        #Creating Sprite Groups
        self.all_sprites = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        
        self.walls = pygame.sprite.Group()
        self.bricks = pygame.sprite.Group()
        self.glass = pygame.sprite.Group()
        self.LockedDoors = pygame.sprite.Group()

        self.keys = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        
        self.weapons = pygame.sprite.Group()
        self.weapons_lvl2 = pygame.sprite.Group()
        self.weapons_lvl3 = pygame.sprite.Group()
        
        self.health = pygame.sprite.Group()
        self.super_health = pygame.sprite.Group()

        self.armour = pygame.sprite.Group()
        
        self.coin = pygame.sprite.Group()
        
        self.dogs = pygame.sprite.Group()
        self.clowns = pygame.sprite.Group()

        self.B_vendings_lvl1 = pygame.sprite.Group()
        self.B_vendings_lvl2 = pygame.sprite.Group()

        self.game_keys = pygame.sprite.Group()
        
        self.strength = pygame.sprite.Group()

        self.fire = pygame.sprite.Group()
        
        #Creating items in game
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                if tile == '2':
                    Brick(self, col, row)
                if tile == '3':
                    Glass(self, col, row)
                if tile == 'k':
                    self.k = Key(self, 'Game_Key.png', col, row)
                if tile == 'L':
                    self.LD = Locked_Door(self, col, row)
                if tile == 'G':
                    self.ghost = Ghost(self, self.screen, col, row)
                if tile == 'W':
                    self.bat = Weapon(self, 'Level 1 Bat.png', col, row)
                if tile == 'H':
                    self.potion = Health(self, col, row)
                if tile == 'C':
                    self.c = Coin(self, col, row)
                if tile == 'd':
                    self.dog = Dog(self, col, row)
                if tile == '4':
                    self.bat_vending_machine = Bat_Vending_lvl1(self, col, row)
                if tile == '5':
                    self.bad_vending_machine_lvl2 = Bat_Vending_lvl2(self, col, row)
                if tile == 'A':
                    self.armor = Armour(self, col, row)
                if tile == 'S':
                    self.SH = Super_Health(self, col, row)
                if tile == 'K':
                    self.game_key = Seven_key(self, col, row)
                if tile == 'F':
                    self.flame = Fire(self, col, row)
                if tile == 't':
                    self.st_potion = Strength_Potion(self, col, row)
                if tile == 'X':
                    self.clown = Clown(self, col, row)

                    
        self.player = Character(self, self.screen, 2,2, self.players, self.enemies, self.dogs, self.clowns)
        self.camera = Camera(self.map.Width, self.map.Height)
        self.level2_bat = Level2_Weapon(self, 'Level 2 Bat.png')
        self.level3_bat = Level3_Weapon(self, 'Level 3 Bat.png')
    def update(self):
        self.all_sprites.update()
        self.camera.update(self.player)
        
        keys = pygame.sprite.spritecollide(self.player, self.keys, False)
        weapons = pygame.sprite.spritecollide(self.player, self.weapons, False)
        health_potions = pygame.sprite.spritecollide(self.player, self.health, False)
        coin_counter = pygame.sprite.spritecollide(self.player, self.coin, False)
        vending_bat_lvl2 = pygame.sprite.spritecollide(self.player, self.B_vendings_lvl1, False)
        vending_batlvl3 = pygame.sprite.spritecollide(self.player, self.B_vendings_lvl2, False)
        super_health_potion = pygame.sprite.spritecollide(self.player, self.super_health, False)
        armour_potion = pygame.sprite.spritecollide(self.player, self.armour, False)
        actual_key = pygame.sprite.spritecollide(self.player, self.game_keys, False)
        fire_collision = pygame.sprite.spritecollide(self.player, self.fire, False)
        strength_potion = pygame.sprite.spritecollide(self.player, self.strength, False)

        if fire_collision:
            self.player.health -= 1
            
        for strength in strength_potion:
            self.player.damage += 3
            strength.kill()
                          
        for key in actual_key:
            self.player.keys.append(key)
            key.kill()
        
        for SUPER in super_health_potion:
            if self.player.health < self.player.MaxHealth:
                self.player.add_health(50)
                SUPER.kill()

        for armour in armour_potion:
            if self.player.MaxHealth < 150:
                self.player.add_armour(5)
                armour.kill()
        
        for weapon in weapons:
            if len(self.player.inventory) < 5:
                self.player.inventory.append(weapon)
                self.player.damage = self.player.damage + 5
                weapon.kill()
        
        if vending_bat_lvl2:
            for item in self.player.inventory:
                if self.player.coins >= 20:
                    if isinstance(item, Weapon):
                        self.player.inventory.remove(item)
                        self.player.inventory.append(self.level2_bat)
                        self.player.damage += 4
                        self.player.coins -= 20
                        
        if vending_batlvl3:
            for item in self.player.inventory:
                if self.player.coins >= 50:
                    if isinstance(item, Level2_Weapon):
                        self.player.inventory.remove(item)
                        self.player.inventory.append(self.level3_bat)
                        self.player.damage += 6
                        self.player.coins -= 50
                
        for coin in coin_counter:
            self.player.coins += 1
            with open('Coin Amount.txt', 'w') as e:
                e.write(str(self.player.coins))
                
            coin.kill()
            
        for HP in health_potions:
            if self.player.health < self.player.MaxHealth:
                self.player.add_health(10)
                HP.kill()
        
        for key in keys:
            if len(self.player.inventory) < 5:
                self.player.inventory.append(key)
                key.kill()
        
    def draw(self):
        #Draws all Sprites to the screen
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.user(sprite))
            if isinstance(sprite, Character):
                sprite.health_bar()
                sprite.inventory_bar()
        
    #Start Screen
    def Start_Screen(self):
        click = None
        while True:
            self.screen.fill((0,0,0))
            self.screen.blit(start, (0,0))
            
            PLAYBUTTON = pygame.Rect(30, 570, 200, 50)
            PLAYFONT = pygame.font.SysFont('Arial', 20)

            CONTROLBUTTON = pygame.Rect(260, 570, 200, 50)
            CONTROLFONT = pygame.font.SysFont('Arial', 20)

            pygame.draw.rect(self.screen, (0, 0, 0), PLAYBUTTON)
            self.screen.blit(PLAYFONT.render('PLAY', True, (255,255,255)), (100,580))

            pygame.draw.rect(self.screen, (0,0,0), CONTROLBUTTON)
            self.screen.blit(CONTROLFONT.render('CONTROLS', True, (255, 255, 255)), (300, 580))

            click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True
                        
            mx, my = pygame.mouse.get_pos()

            if PLAYBUTTON.collidepoint(mx, my):
                if click:
                    self.run()

            if CONTROLBUTTON.collidepoint(mx, my):
                if click:
                    self.Controls()
                             
            pygame.display.flip()
            self.clock.tick(60)

    #Control Screen
    def Controls(self):
        running = True
        while running:
            self.screen.fill((0,0,0))
            self.screen.blit(controls, (0,0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        
            pygame.display.flip()
            self.clock.tick(60)

    #Main Game Loop
    def run(self):
        running = True
        while running:
            self.screen.fill((255,255,255))
            self.screen.blit(Floor_test2, (0,0))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        
                    if event.key == pygame.K_DOWN:
                        self.player.move_down()
                        
                    if event.key == pygame.K_UP:
                        self.player.move_up()
                        
                    if event.key == pygame.K_LEFT:
                        self.player.move_left()
                        
                    if event.key == pygame.K_RIGHT:
                        self.player.move_right()
                        
                    if event.key == pygame.K_SPACE:
                        if self.player.in_GhostAttackRange:
                            self.player.ghost_hit()
                            
                        if self.player.in_DogAttackRange:
                            self.player.dog_hit()

                        if self.player.in_ClownAttackRange:
                            self.player.clown_hit()
                            
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        self.player.standing()
                    if event.key == pygame.K_UP:
                        self.player.standing()
                    if event.key == pygame.K_LEFT:
                        self.player.standing()
                    if event.key == pygame.K_RIGHT:
                        self.player.standing()
                    
            self.update()
            self.draw()

            count = 0
            for item in self.player.inventory:
                converted = pygame.image.load(os.path.join('Game Items',item.png))
                self.screen.blit(converted, (176+count,608))
                count += 64
                
            if self.player.health <= 0:
                self.lose_screen()
                

            pygame.display.flip()
            self.clock.tick(60)
    def lose_screen(self):
        running = True
        while running:
            self.screen.fill((0,0,0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                        
            pygame.display.flip()
            self.clock.tick(60)

    def end_game(self):
        if len(self.player.keys) == 7:
            pass

game = Game()
game.new_char()
game.Start_Screen()

