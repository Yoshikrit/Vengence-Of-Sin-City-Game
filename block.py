import pygame

MAX_LEVELS = 5
TILE_SIZE = 50
TILE_TYPES = 58

health_fx = pygame.mixer.Sound('Sounds\Health.wav')
health_fx.set_volume(0.02)
pick_fx = pygame.mixer.Sound('Sounds\Pick.wav')
pick_fx.set_volume(0.02)

class Decoration(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self , screen_scroll) :
        self.rect.x += screen_scroll

class Water(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self , screen_scroll):
        self.rect.x += screen_scroll

class Exit(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self, screen_scroll):
        self.rect.x += screen_scroll

class ItemBox(pygame.sprite.Sprite):
    def __init__(self, itemtype, x, y , itemboxes):
        pygame.sprite.Sprite.__init__(self)
        self.itemtype = itemtype
        self.image = itemboxes[self.itemtype]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self, screen_scroll , player):
        #scroll
        self.rect.x += screen_scroll
        #check if player picked box
        if pygame.sprite.collide_rect(self, player):
            #check type box it is
            if self.itemtype == 'Health':
                if player.health <= 50:
                    player.health += 50
                    self.kill()#delete box
                    health_fx.play()
                elif player.health > 50 and player.health < 100:
                    player.health = 100
                    self.kill()#delete box
                    health_fx.play()
            elif self.itemtype == 'Ammo':
                player.ammo += 6
                self.kill()#delete box
                pick_fx.play()
            elif self.itemtype == 'Grenade':
                player.grenades += 4
                self.kill()#delete box
                pick_fx.play()
            elif self.itemtype == 'Fireball':
                player.fireball += 6
                self.kill()#delete box
                pick_fx.play()
