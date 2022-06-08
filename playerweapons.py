import pygame
from bomb import Explosion 
from blood import Blood

WINDOW_SIZE = (1200 , 800)
screen = pygame.display.set_mode(WINDOW_SIZE,0,32)#start window

gravity = 0.8#gravity 0.75
TILE_SIZE = 50

RED = (255, 0, 0)

explosion_fx = pygame.mixer.Sound('Sounds\Explosion.wav')
explosion_fx.set_volume(0.02)

#all ammunation
bulletimg = pygame.image.load(f'Pictures\Weapons\Bullet.png').convert_alpha()
grenadeimg = pygame.image.load(f'Pictures\Weapons\grenade.png').convert_alpha()
fireballimg = pygame.image.load(f'Pictures\Weapons\Fireball.png').convert_alpha()
rpgimg = pygame.image.load(f'Pictures\Weapons\Rocket.png').convert_alpha()

class Bullet(pygame.sprite.Sprite):#กระสุนเรา
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 20
        self.image = bulletimg
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.direction = direction
    
    def update(self , player , screen_scroll , world ,bulletgroup1 , enemygroup1 , enemygroup2 , bossgroup):
        #move bullet
        self.rect.x += (self.direction * self.speed) + screen_scroll
        #ถ้ากระสุนยิงสุดขอบ
        #if self.rect.right < 0 or self.rect.left > WINDOW_SIZE[0] - 100:
        if self.rect.right < player.rect.left - 650 or self.rect.left > player.rect.right + 650:
            self.kill()
        #check collision
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                self.kill()

        #ยิงโดนตัวไหม
        for enemy in enemygroup1:
            if pygame.sprite.spritecollide(enemy, bulletgroup1,False):
                if enemy.alive:
                    enemy.health -= 40
                    self.kill()
        for enemy in enemygroup2:
            if pygame.sprite.spritecollide(enemy, bulletgroup1,False):
                if enemy.alive:
                    enemy.health -= 40
                    self.kill()
        for enemy in bossgroup:
            if pygame.sprite.spritecollide(enemy, bulletgroup1,False):
                if enemy.alive:
                    enemy.health -= 40
                    self.kill()

class Grenade(pygame.sprite.Sprite):
    def __init__(self, x, y, direction ):
        pygame.sprite.Sprite.__init__(self)
        self.timer = 100
        self.vel_y = -11
        self.speed = 7
        self.image = grenadeimg
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.direction = direction

    def update(self , screen_scroll , world , explosiongroup , player , enemygroup1 , enemygroup2 , bossgroup, bloodgroup):
        self.vel_y += gravity
        dx = self.direction * self.speed
        dy = self.vel_y

        #check for collision with level
        for tile in world.obstacle_list:
            #check collision with walls
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                self.direction *= -1
                dx = self.direction * self.speed
            #check for collision in the y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                self.speed = 0
                #check if below the ground, i.e. thrown up
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                #check if above the ground, i.e. falling
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    dy = tile[1].top - self.rect.bottom 


        #update grenade position
        self.rect.x += dx + screen_scroll
        self.rect.y += dy

        #countdown timer
        self.timer -= 1
        if self.timer <= 0:
            self.kill()
            explosion = Explosion(self.rect.x, self.rect.y, 1)
            explosiongroup.add(explosion)
            #do damage to anyone that is nearby
            if abs(self.rect.centerx - player.rect.centerx) < TILE_SIZE * 2 and \
                abs(self.rect.centery - player.rect.centery) < TILE_SIZE * 2:
                player.health -= 99
                t = Blood(player.rect.center, RED , screen)
                bloodgroup.add(t)
                
            for enemy in enemygroup1:
                if abs(self.rect.centerx - enemy.rect.centerx) < TILE_SIZE * 2 and \
                    abs(self.rect.centery - enemy.rect.centery) < TILE_SIZE * 2:
                    enemy.health -= 100
            for enemy in enemygroup2:
                if abs(self.rect.centerx - enemy.rect.centerx) < TILE_SIZE * 2 and \
                    abs(self.rect.centery - enemy.rect.centery) < TILE_SIZE * 2:
                    enemy.health -= 100
            for boss in bossgroup:
                if abs(self.rect.centerx - boss.rect.centerx) < TILE_SIZE * 2 and \
                    abs(self.rect.centery - boss.rect.centery) < TILE_SIZE * 2:
                    boss.health -= 100

class Fire(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 20
        self.image = fireballimg
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.direction = direction
    
    def update(self , screen_scroll , player , world , enemygroup1 , enemygroup2 , bossgroup , fireballgroup1):
        #move bullet
        self.rect.x += (self.direction * self.speed) + screen_scroll
        #ถ้ากระสุนยิงสุดขอบ 
        if self.rect.right < player.rect.left - 800 or self.rect.left > player.rect.right + 800:
            self.kill()
        #check collision
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                self.kill()

        #ยิงโดนตัวไหม
        for enemy in enemygroup1:
            if pygame.sprite.spritecollide(enemy, fireballgroup1,False):
                if enemy.alive:
                    enemy.health -= 200
                    self.kill()
        for enemy in enemygroup2:
            if pygame.sprite.spritecollide(enemy, fireballgroup1,False):
                if enemy.alive:
                    enemy.health -= 200
                    self.kill()
        for boss in bossgroup:
            if pygame.sprite.spritecollide(boss, fireballgroup1,False):
                if boss.alive:
                    boss.health -= 200
                    self.kill()