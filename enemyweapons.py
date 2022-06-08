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
laser_fx = pygame.mixer.Sound('Sounds\Lasershoot.wav')
laser_fx.set_volume(0.02)

#all ammunation
bulletimg = pygame.image.load(f'Pictures\Weapons\Bullet.png').convert_alpha()
grenadeimg = pygame.image.load(f'Pictures\Weapons\grenade.png').convert_alpha()
fireballimg = pygame.image.load(f'Pictures\Weapons\Fireball.png').convert_alpha()
rpgimg = pygame.image.load(f'Pictures\Weapons\Rocket.png').convert_alpha()
laserimg = pygame.image.load(f'Pictures\Weapons\Laser.png').convert_alpha()

class BulletEnemy1(pygame.sprite.Sprite):#กระสุนของศัตรู
    def __init__(self, x, y, direction ):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 40
        self.image = bulletimg
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.direction = direction
    
    def update(self ,  player , screen_scroll , world , bulletgroup2 , bloodgroup):
        #move bullet
        self.rect.x += (self.direction * self.speed) + screen_scroll
        #ถ้ากระสุนยิงสุดขอบ
        if self.rect.right < player.rect.left - 400 or self.rect.left > player.rect.right + 400:
            self.kill()
        #check collision
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                self.kill()

        #ยิงโดนตัวไหม
        if pygame.sprite.spritecollide(player, bulletgroup2,False):
            if player.alive:
                player.health -= 1
                self.kill()
                t = Blood(player.rect.center, RED , screen)
                bloodgroup.add(t)

class BulletEnemy2(pygame.sprite.Sprite):#กระสุนของศัตรู
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 40
        self.image = bulletimg
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.direction = direction
    
    def update(self ,  player , screen_scroll , world , bulletgroup2, bloodgroup):
        #move bullet
        self.rect.x += (self.direction * self.speed) + screen_scroll
        #ถ้ากระสุนยิงสุดขอบ
        if self.rect.right < player.rect.left - 400 or self.rect.left > player.rect.right + 400:
            self.kill()
        #check collision
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                self.kill()

        #ยิงโดนตัวไหม
        if pygame.sprite.spritecollide(player, bulletgroup2,False):
            if player.alive:
                player.health -= 10
                self.kill()
                t = Blood(player.rect.center, RED , screen)
                bloodgroup.add(t)

class BulletEnemy3(pygame.sprite.Sprite):#กระสุนของศัตรู
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 40
        self.image = bulletimg
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.direction = direction
    
    def update(self ,  player , screen_scroll , world , bulletgroup2, bloodgroup):
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
        if pygame.sprite.spritecollide(player, bulletgroup2,False):
            if player.alive:
                player.health -= 20
                self.kill()
                t = Blood(player.rect.center, RED , screen)
                bloodgroup.add(t)

class RPG(pygame.sprite.Sprite):#กระสุนของศัตรู
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 30
        self.image = rpgimg
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.direction = direction
    
    def update(self ,  player , screen_scroll , world , rpggroup , explosiongroup, bloodgroup):
        #move bullet
        self.rect.x += (self.direction * self.speed) + screen_scroll
        #ถ้ากระสุนยิงสุดขอบ
        if self.rect.right < player.rect.left - 300 or self.rect.left > player.rect.right + 300:
            self.kill()
            explosion = Explosion(self.rect.x, self.rect.y, 1)
            explosiongroup.add(explosion)
        #check collision
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                self.kill()
                explosion = Explosion(self.rect.x, self.rect.y, 1)
                explosiongroup.add(explosion)
                explosion_fx.play()

        #ยิงโดนตัวไหม
        if pygame.sprite.spritecollide(player, rpggroup,False):
            if player.alive:
                player.health -= 30
                t = Blood(player.rect.center, RED , screen)
                bloodgroup.add(t)
                self.kill()
                explosion = Explosion(self.rect.x, self.rect.y, 1)
                explosiongroup.add(explosion)
                explosion_fx.play()

class Laser(pygame.sprite.Sprite):#laserของศัตรู
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self) 
        self.speed = 10
        self.image = laserimg
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.direction = direction
    
    def update(self,  player , screen_scroll , world ,lasergroup, bloodgroup):
        #move bullet
        self.rect.x += (self.direction * self.speed) + screen_scroll
        #ถ้ากระสุนยิงสุดขอบ
        if self.rect.right < player.rect.left - 300 or self.rect.left > player.rect.right + 300:
            self.kill()
        #check collision
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                self.kill()

        #ยิงโดนตัวไหม
        if pygame.sprite.spritecollide(player, lasergroup ,False):
            if player.alive:
                player.health -= 1
                laser_fx.play()
                t = Blood(player.rect.center, RED , screen)
                bloodgroup.add(t)

class FireEnemy(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 20
        self.image = fireballimg
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.direction = direction
    
    def update(self ,screen_scroll , player , world , fireballgroup2, bloodgroup):
        #move bullet
        self.rect.x += (self.direction * self.speed)  + screen_scroll
        #ถ้ากระสุนยิงสุดขอบ
        if self.rect.right < player.rect.left - 600 or self.rect.left > player.rect.right + 600:
            self.kill()
        #check collision
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                self.kill()

        #ยิงโดนตัวไหม
        if pygame.sprite.spritecollide(player, fireballgroup2, False):
            if player.alive:
                player.health -= 5
                self.kill()
                t = Blood(player.rect.center, RED , screen)
                bloodgroup.add(t)