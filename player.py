import pygame
from bomb import Poof
from playerweapons import Bullet , Fire

WINDOW_SIZE = (1200 , 800)
TILE_SIZE = 50
SCROLL_THRESH = 600 #ระยะที่playerไปที่มุมได้ก่อนเริ่มเลื่อนหน้าจอ
gravity = 0.8#gravity 0.75

BLACK = (0, 0, 0)
GREY = (65,65,65)
RED = (255, 0, 0)

#sound
shoot1_fx = pygame.mixer.Sound('Sounds\Shoot1.wav')
shoot1_fx.set_volume(0.02)
fireball_fx = pygame.mixer.Sound('Sounds\Fireshot.wav')
fireball_fx.set_volume(0.02)
playerdeath_fx = pygame.mixer.Sound('Sounds\Death.wav')
playerdeath_fx.set_volume(0.03)


class Player(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale , speed , ammo , grenades , fireball):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.ammo = ammo
        self.startammo = ammo
        self.shootcooldown = 0#cooldown การยิง
        self.grenades = grenades
        self.fireball = fireball
        self.health = 100#เลือด
        self.maxhealth = self.health#healthbar
        self.direction = 1
        self.vel_y = 0#ความเร็วการกระโดด
        self.jump = False
        self.in_air = True#checkให้กระโดดครั้งเดียว
        self.flip = False
        img = pygame.image.load(f'Pictures\Characters\{self.char_type}.png')
        self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
    
    def update(self,poofgroup):
        self.checkalive(poofgroup)
        #update cooldown
        if self.shootcooldown > 0:
            self.shootcooldown -= 1

    def move(self, moving_left, moving_right , world ,watergroup , exitgroup, bg_scroll , screen_scroll):
        #reset movement variables
        screen_scroll = 0
        dx = 0
        dy = 0

        #assign movement variables if moving left or right
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1
        #jump
        if self.jump == True and self.in_air == False:
            self.vel_y = -17
            self.jump = False
            self.in_air = True

        #apply gravity
        self.vel_y += gravity
        if self.vel_y > 5:
            self.vel_y
        dy += self.vel_y

        #check for collision
        for tile in world.obstacle_list:
            #check collision in the x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
                #if self.char_type == 'enemy':
                    #self.direction *= -1
                    #self.move_counter = 0
            #check for collision in the y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                #check if below the ground, i.e. jumping
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                #check if above the ground, i.e. falling
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom

        #check dat fall water = ded
        if pygame.sprite.spritecollide(self, watergroup , False):
            self.health = 0

        #check collision exit
        level_complete = False
        #if not godoffire.alive and level == 0:
            #level_complete = True
        if pygame.sprite.spritecollide(self, exitgroup , False):
            level_complete = True

        #check if fall
        if self.rect.bottom > WINDOW_SIZE[1]:
            self.health = 0

        #check ถ้าไปสุดขอบ
        if self.char_type == 'player':
            if self.rect.left + dx < 0 or self.rect.right + dx > WINDOW_SIZE[0]:
                dx = 0

        #update rectangle position
        self.rect.x += dx
        self.rect.y += dy

        #update scroll base on player location
        if self.char_type == 'player':
            if (self.rect.right > WINDOW_SIZE[0] - SCROLL_THRESH and bg_scroll < (world.level_length * TILE_SIZE) - WINDOW_SIZE[0])\
                or (self.rect.left < SCROLL_THRESH and bg_scroll > abs(dx)):
                self.rect.x -= dx
                screen_scroll = -dx
        
        return screen_scroll , level_complete

    def shoot(self , bulletgroup1):
        if self.shootcooldown == 0 and self.ammo > 0:
            self.shootcooldown = 20#reload time ยิ่งน้อย ยิ่งreloadเร็ว
            bullet = Bullet(self.rect.centerx + (0.6 *self.rect.size[0] * self.direction), self.rect.centery,self.direction)
            bulletgroup1.add(bullet)
            #กระสุนหายไปหลังจากยิงทีละนัด
            self.ammo -= 1
            shoot1_fx.play()
    
    def shoot2(self , fireballgroup1):
        if self.shootcooldown == 0 and self.fireball > 0:
            self.shootcooldown = 25#reload time ยิ่งน้อย ยิ่งreloadเร็ว
            flare = Fire(self.rect.centerx + (0.6 *self.rect.size[0] * self.direction), self.rect.centery,self.direction)
            fireballgroup1.add(flare)
            #กระสุนหายไปหลังจากยิงทีละนัด
            self.fireball -= 1
            fireball_fx

    def checkalive(self , poofgroup):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.kill()
            poof = Poof(self.rect.x + TILE_SIZE, self.rect.y + TILE_SIZE, 1)
            poofgroup.add(poof)
            #playerdeath_fx.play()

    def draw(self , screen):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
        #pygame.draw.rect(screen, RED, self.rect , 1)
    
class HealthBar():
    def __init__(self, x, y, health, maxhealth):
        self.x = x
        self.y = y
        self.health = health
        self.maxhealth = maxhealth

    def draw(self, health , screen ):
        #update  new hp
        self.health = health
        #คำนวณเลือด
        ratio = self.health / self.maxhealth
        pygame.draw.rect(screen, GREY, (self.x - 2 , self.y - 2 , 254 , 24))
        pygame.draw.rect(screen, BLACK, (self.x , self.y , 250 , 20))# 250 = ยาวในการแสดงเลือด , 20 = แท่งเลือดสูง
        pygame.draw.rect(screen, RED, (self.x , self.y , 250 * ratio ,20))


