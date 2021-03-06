import pygame
from pygame import mixer

mixer.init()


explosion_fx = pygame.mixer.Sound('Sounds\Explosion.wav')
explosion_fx.set_volume(0.02)


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, scale ):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 6):
            img = pygame.image.load(f'Pictures\Explosion\{num}.png').convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            self.images.append(img)
        self.frame_index = 0
        self.image = self.images[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0


    def update(self , screen_scroll):
        #scroll
        self.rect.x += screen_scroll
        EXPLOSION_SPEED = 5
        #update explosion amimation
        self.counter += 1

        if self.counter >= EXPLOSION_SPEED:
            self.counter = 0
            self.frame_index += 1
            #if the animation is complete then delete the explosion
            if self.frame_index >= len(self.images):
                self.kill()
                explosion_fx.play()
            else:
                self.image = self.images[self.frame_index]

class Poof(pygame.sprite.Sprite):
    def __init__(self, x, y , scale):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1,4):
            img = pygame.image.load(f'Pictures\Poof\{num}.png').convert_alpha()
            img = pygame.transform.scale(img,(int (img.get_width() * scale), int(img.get_height() * scale)))
            self.images.append(img)
        self.frame_index = 0
        self.image = self.images[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.counter = 0 
    
    def update(self , screen_scroll):
        #scroll
        self.rect.x += screen_scroll
        POOF_SPEED = 4
        #animantion
        self.counter += 1

        if self.counter >= POOF_SPEED:
            self.counter = 0
            self.frame_index += 1
            #if animation ?????? ?????? ??????
            if self.frame_index >= len(self.images):
                self.kill()
            else:
                self.image = self.images[self.frame_index]
