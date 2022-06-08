import pygame
import random
from block import ItemBox , Exit
from enemyweapons import BulletEnemy1 , BulletEnemy2 , BulletEnemy3 , RPG , Laser , FireEnemy
from bomb import Poof

WINDOW_SIZE = (1200 , 800)
TILE_SIZE = 50
SCROLL_THRESH = 600 #ระยะที่playerไปที่มุมได้ก่อนเริ่มเลื่อนหน้าจอ
gravity = 0.8#gravity 0.75

bossappear_fx = pygame.mixer.Sound('Sounds\Bossappear.wav')
bossappear_fx.set_volume(0.02)
shoot1_fx = pygame.mixer.Sound('Sounds\Shoot1.wav')
shoot1_fx.set_volume(0.02)
drop_fx = pygame.mixer.Sound('Sounds\Drop.wav')
drop_fx.set_volume(0.02)
enemydeath_fx = pygame.mixer.Sound('Sounds\Enemydeath.wav')
enemydeath_fx.set_volume(0.03)
fireball_fx = pygame.mixer.Sound('Sounds\Fireshot.wav')
fireball_fx.set_volume(0.02)
laser_fx = pygame.mixer.Sound('Sounds\Lasershoot.wav')
laser_fx.set_volume(0.02)

class RangeEnemy(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale , speed , ammo , health , cooldown , vision_length1 , aware_length1 , vision_length2 , aware_length2 , damage):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.ammo = ammo
        self.startammo = ammo
        self.shootcooldown = 0#cooldown การยิง
        self.cooldown = cooldown
        self.health = health#เลือด
        self.direction = 1
        self.vel_y = 0
        self.timer = 100
        self.vision_length1 = vision_length1#ระยะที่ศัตรูมองเห็น
        self.aware_length1 = aware_length1#ระยะที่ศัตรูมองกลับ
        self.vision_length2 = vision_length2#ระยะห่างจากสายตาที่ศัตรูมองเห็น
        self.aware_length2 = aware_length2#ระยะห่างจากสายตาที่ศัตรูมองกลับ
        self.damage = damage
        self.flip = False
        img = pygame.image.load(f'Pictures\Characters\{self.char_type}.png')
        self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        #create ai variable
        self.move_counter = 0
        self.vision = pygame.Rect(0,0,vision_length1,100)#ระยะไกล 100 สูง ระยะที่กำหนดให้ ai มองเห็นเราแล้วยัง
        self.aware = pygame.Rect(0,0,aware_length1,100)
        self.idling = False
        self.idling_counter = 0
    
    def update(self , poofgroup , itemboxgroup , itemboxes):
        self.checkalive(poofgroup , itemboxgroup , itemboxes)
        #update cooldown
        if self.shootcooldown > 0:
            self.shootcooldown -= 1

    def move(self, moving_left, moving_right ,world ,watergroup):
        #reset movement variables
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
                self.direction *= -1
                self.move_counter = 0
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
        #check if fall
        if self.rect.bottom > WINDOW_SIZE[1]:
            self.health = 0

        #check ถ้าไปสุดขอบ
        if self.rect.left + dx < 0 or self.rect.right + dx > WINDOW_SIZE[0]:
            dx = 0

        #update rectangle position
        self.rect.x += dx
        self.rect.y += dy

    def shoot(self ,bulletgroup2 ,rpggroup):
        #cooldown การยิง
        if self.ammo == 0:
            self.timer -= 1
            if self.timer <= 0:
                self.ammo = 20
                self.timer = 100

        if self.shootcooldown == 0 and self.ammo > 0:
            self.shootcooldown = self.cooldown#reload time ยิ่งน้อย ยิ่งreloadเร็ว
            if self.damage == 5:
                bullet = BulletEnemy1(self.rect.centerx + (0.6 *self.rect.size[0] * self.direction), self.rect.centery,self.direction )#เลขในวงเล็บไว้เปลี่ยนจุดปล่อยกระสุนให้ไกลขึ้น
                bulletgroup2.add(bullet)
            if self.damage == 10:
                bullet = BulletEnemy2(self.rect.centerx + (0.6 *self.rect.size[0] * self.direction), self.rect.centery,self.direction)
                bulletgroup2.add(bullet)
            if self.damage == 20:
                bullet = BulletEnemy3(self.rect.centerx + (0.6 *self.rect.size[0] * self.direction), self.rect.centery,self.direction )
                bulletgroup2.add(bullet)
            if self.damage == 30:
                rpg = RPG(self.rect.centerx + (0.6 *self.rect.size[0] * self.direction), self.rect.centery,self.direction )
                rpggroup.add(rpg)

            #กระสุนหายไปหลังจากยิงทีละนัด
            self.ammo -= 1
            shoot1_fx.play()

    def ai(self , player , screen_scroll ,world ,watergroup , bulletgroup2 ,rpggroup):
        if self.alive and player.alive:
            if self.idling == False and random.randint(1,300) == 1:
                self.idling = True
                self.idling_counter = 50
            #check if ai near player
            if self.vision.colliderect(player.rect):
                #stop running and face to player and shoot
                self.shoot(bulletgroup2 ,rpggroup)
                if self.aware.colliderect(player.rect):
                #stop running and face to player and shoot
                    self.direction *= -1
            else:
                if self.idling == False:
                    if self.direction == 1:
                        ai_moving_right = True
                    else:
                        ai_moving_right = False
                    ai_moving_left = not ai_moving_right
                    self.move(ai_moving_left , ai_moving_right ,world ,watergroup)
                    self.move_counter += 1
                    #update ai vision ของศัตรูตอนเดิน
                    self.vision.center = (self.rect.centerx + self.vision_length2 * self.direction,self.rect.centery )
                    #pygame.draw.rect(screen , RED , self.vision)#เช็ควิสัยทัศ ai
                    self.aware.center = (self.rect.centerx - self.aware_length2 * self.direction,self.rect.centery )
                    #pygame.draw.rect(screen , GREEN, self.aware)#เช็คกรณีเดินผ่าน ให้ยิง

                    if self.move_counter > TILE_SIZE:
                        self.direction *= -1
                        self.move_counter *= -1
                else:
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                        self.idling = False

        self.rect.x += screen_scroll

    def Damage(self , player , enemygroup):
        if self.alive and player.alive:
            if pygame.sprite.spritecollide(player, enemygroup ,False):
                player.health -= 0.1
            
    def checkalive(self , poofgroup , itemboxgroup ,itemboxes):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.kill()
            poof = Poof(self.rect.x + TILE_SIZE, self.rect.y + TILE_SIZE, 1)
            poofgroup.add(poof)
            enemydeath_fx.play()
            if random.randint(1,8) == 1:
                itembox = ItemBox('Ammo' , self.rect.x + TILE_SIZE , self.rect.y + TILE_SIZE , itemboxes)
                itemboxgroup.add(itembox)
                drop_fx.play()
    
    def draw(self,screen):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

class MeleeEnemy(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale , speed , health ,  vision_length1x,vision_length1y , vision_length2 , damage):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.shootcooldown = 0#cooldown การยิง
        self.health = health#เลือด
        self.direction = 1
        self.vel_y = 0#ความเร็วการกระโดด
        self.in_air = True
        self.vision_length1x = vision_length1x#ระยะที่ศัตรูมองเห็น
        self.vision_length1y = vision_length1y
        self.vision_length2 = vision_length2#ระยะห่างจากสายตาที่ศัตรูมองเห็น
        self.damage = damage#type of damage by gun

        self.flip = False
        img = pygame.image.load(f'Pictures\Characters\{self.char_type}.png')
        self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        #create ai variable
        self.move_counter = 0
        self.vision = pygame.Rect(0,0,vision_length1x,vision_length1y)#ระยะไกล 100 สูง ระยะที่กำหนดให้ ai มองเห็นเราแล้วยัง
        self.idling = False
        self.idling_counter = 0
    
    def update(self, poofgroup , exitgroup ):
        self.checkalive(poofgroup , exitgroup)
        #update cooldown
        if self.shootcooldown > 0:
            self.shootcooldown -= 1

    def move(self, moving_left, moving_right , world ,watergroup):
        #reset movement variables
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
                self.direction *= -1
                self.move_counter = 0
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
        #check if fall
        if self.rect.bottom > WINDOW_SIZE[1]:
            self.health = 0
        
        #check ถ้าไปสุดขอบ
        if self.rect.left + dx < 0 or self.rect.right + dx > WINDOW_SIZE[0]:
            dx = 0

        #update rectangle position
        self.rect.x += dx
        self.rect.y += dy

    def ai(self , player , screen_scroll ,world ,watergroup):
        if self.alive and player.alive:
            if self.direction == 1:
                ai_moving_right = True
            else:
                ai_moving_right = False
            ai_moving_left = not ai_moving_right
            self.move(ai_moving_left , ai_moving_right ,world ,watergroup)
            self.move_counter += 1
            self.vision.center = (self.rect.centerx + self.vision_length2 * self.direction,self.rect.centery )
            #pygame.draw.rect(screen , RED , self.vision)#เช็ควิสัยทัศ ai

            if self.move_counter > TILE_SIZE:
                self.direction *= -1
                self.move_counter *= -1
                
            #check if ai near player
            if self.vision.colliderect(player.rect):
                self.speed = 4
                if self.char_type == 'godoffire':
                    bossappear_fx.play()
                if player.rect.x > self.rect.x:
                    self.direction = 1
                if player.rect.x < self.rect.x:
                    self.direction = -1
            else:
                self.speed = 2

        self.rect.x += screen_scroll

    def Damage(self , player , enemygroup):
        if self.alive and player.alive:
            if pygame.sprite.spritecollide(player, enemygroup ,False):
                player.health -= self.damage
    
    def checkalive(self , poofgroup , exitgroup):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.kill()
            poof = Poof(self.rect.x + TILE_SIZE, self.rect.y + TILE_SIZE, 1)
            poofgroup.add(poof)
            enemydeath_fx.play()
            if self.char_type == 'godoffire':
                exitsign = Exit(pygame.image.load(f'Pictures\Tiles\9.png') , self.rect.x + TILE_SIZE , self.rect.y + TILE_SIZE)
                exitgroup.add(exitsign)
                drop_fx.play()

    def draw(self , screen):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

class Boss(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale , speed , fireball , health , cooldown , vision_lengthx1 ,vision_lengthy1 , vision_length2 , timer , maxtimer , maxfireball , maxspeed , laser , maxlaser):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.fireball = fireball
        self.maxfireball = maxfireball
        self.startfireball = fireball
        self.shootcooldown = 0#cooldown การยิง
        self.cooldown = cooldown
        self.health = health#เลือด
        self.direction = 1
        self.vel_y = 0
        self.timer = timer
        self.maxtimer = maxtimer
        self.maxspeed = maxspeed
        self.laser = laser
        self.maxlaser = maxlaser
        self.vision_lengthx1 = vision_lengthx1#ระยะที่ศัตรูมองเห็นx
        self.vision_lengthy1 = vision_lengthy1#ระยะที่ศัตรูมองเห็นy
        self.vision_length2 = vision_length2#ระยะห่างจากสายตาที่ศัตรูมองเห็น
        self.flip = False
        img = pygame.image.load(f'Pictures\Characters\{self.char_type}.png')
        self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        #create ai variable
        self.move_counter = 0
        self.vision = pygame.Rect(0,0,vision_lengthx1,vision_lengthy1)#ระยะไกล  สูง ระยะที่กำหนดให้ ai มองเห็นเราแล้วยัง
        self.idling = False
        self.idling_counter = 0
    
    def update(self , poofgroup , exitgroup):
        self.checkalive(poofgroup , exitgroup)
        #update cooldown
        if self.shootcooldown > 0:
            self.shootcooldown -= 1

    def move(self, moving_left, moving_right , world , watergroup):
        #reset movement variables
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
                self.direction *= -1
                self.move_counter = 0
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
        #check if fall
        if self.rect.bottom > WINDOW_SIZE[1]:
            self.health = 0

        #check ถ้าไปสุดขอบ
        if self.rect.left + dx < 0 or self.rect.right + dx > WINDOW_SIZE[0]:
            dx = 0

        #update rectangle position
        self.rect.x += dx
        self.rect.y += dy

    def shoot(self , fireballgroup2 , lasergroup ):
        #cooldown การยิง
        if (self.char_type == 'Sage') or (self.char_type == 'Boss'):
            if self.fireball == 0:
                self.speed = 0
                self.timer -= 1
                if self.timer <= 0:
                    self.fireball = self.maxfireball
                    self.timer = self.maxtimer
                    self.speed = self.maxspeed

            if self.shootcooldown == 0 and self.fireball > 0:
                self.shootcooldown = self.cooldown#reload time ยิ่งน้อย ยิ่งreloadเร็ว
                fire = FireEnemy(self.rect.centerx + (0.6 *self.rect.size[0] * self.direction), self.rect.centery,self.direction)#เลขในวงเล็บไว้เปลี่ยนจุดปล่อยกระสุนให้ไกลขึ้น
                fireballgroup2.add(fire)
                #กระสุนหายไปหลังจากยิงทีละนัด
                self.fireball -= 1
                fireball_fx.play()

        if (self.char_type == 'Invincible') or (self.char_type == 'General'):
            if self.laser == 0:
                self.speed = 0
                self.timer -= 1
                if self.timer <= 0:
                    self.laser = self.maxlaser
                    self.timer = self.maxtimer
                    self.speed = self.maxspeed

            if self.shootcooldown == 0 and self.laser > 0:
                self.shootcooldown = self.cooldown#reload time ยิ่งน้อย ยิ่งreloadเร็ว
                laser = Laser(self.rect.centerx + (0.6 *self.rect.size[0] * self.direction), self.rect.centery - 30,self.direction)#เลขในวงเล็บไว้เปลี่ยนจุดปล่อยกระสุนให้ไกลขึ้น

                lasergroup.add(laser)
                #กระสุนหายไปหลังจากยิงทีละนัด
                self.laser -= 1
                laser_fx.play()
            

    def ai(self , player , screen_scroll ,world ,watergroup , fireballgroup2 , lasergroup):
        if self.alive and player.alive:
            if self.direction == 1:
                ai_moving_right = True
            else:
                ai_moving_right = False
            ai_moving_left = not ai_moving_right
            self.move(ai_moving_left , ai_moving_right ,world ,watergroup)
            self.move_counter += 1
            self.vision.center = (self.rect.centerx + self.vision_length2 * self.direction,self.rect.centery )
            #pygame.draw.rect(screen , RED , self.vision)#เช็ควิสัยทัศ ai

            if self.move_counter > TILE_SIZE:
                self.direction *= -1
                self.move_counter *= -1
                
            #check if ai near player
            if self.vision.colliderect(player.rect):
                bossappear_fx.play()
                #self.speed = 3
                if player.rect.x > self.rect.x:
                    self.direction = 1
                    self.shoot(fireballgroup2 , lasergroup)
                if player.rect.x < self.rect.x:
                    self.direction = -1
                    self.shoot(fireballgroup2 , lasergroup)
            else:
                self.speed = self.maxspeed

        self.rect.x += screen_scroll

    def Damage(self,player , bossgroup):
        if self.alive and player.alive:
            if pygame.sprite.spritecollide(player, bossgroup ,False):
                player.health -= 0.3
            
    def checkalive(self , poofgroup , exitgroup):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.kill()
            poof = Poof(self.rect.x + TILE_SIZE, self.rect.y + TILE_SIZE, 1)
            poofgroup.add(poof)
            enemydeath_fx.play()
            exitsign = Exit(pygame.image.load(f'Pictures\Tiles\9.png') , self.rect.x + TILE_SIZE , self.rect.y + TILE_SIZE)
            exitgroup.add(exitsign)
            drop_fx.play()
    
    def draw(self ,screen):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)