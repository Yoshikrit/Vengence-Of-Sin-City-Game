import pygame
from player import Player, HealthBar
from enemy import RangeEnemy ,MeleeEnemy , Boss
from block import Water ,Decoration,Exit ,ItemBox

MAX_LEVELS = 5
TILE_SIZE = 50
TILE_TYPES = 58
#store tiles in a list
img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'Pictures\Tiles\{x}.png')
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)

class World():
    def __init__(self):
        self.obstacle_list = []

    def process_data(self, data , watergroup , decorationgroup , itemboxgroup , exitgroup , enemygroup1 , enemygroup2 , bossgroup , itemboxes):
        self.level_length = len(data[0])
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)
                    if ((tile >= 0 and tile <= 3) or (tile >= 18 and tile <= 29) or (tile >= 40 and tile <= 43) or (tile >= 47 and tile <= 50) ) :#hard block   
                        self.obstacle_list.append(tile_data)
                    elif tile == 5 :#water
                        water = Water(img , x * TILE_SIZE , y * TILE_SIZE)
                        watergroup.add(water)
                    elif tile == 4  or (tile >= 52 and tile <= 54) or (tile >= 34 and tile <= 36) or tile == 38 or tile == 45 or tile == 46:#decoration
                        decoration = Decoration(img , x * TILE_SIZE , y * TILE_SIZE)
                        decorationgroup.add(decoration)
                    elif tile == 6:#ammo crate
                        itembox = ItemBox('Ammo' , x * TILE_SIZE , y * TILE_SIZE , itemboxes)
                        itemboxgroup.add(itembox)
                    elif tile == 7:#health crate
                        itembox = ItemBox('Health' , x * TILE_SIZE , y * TILE_SIZE ,itemboxes )
                        itemboxgroup.add(itembox)
                    elif tile == 8:#grenade crate
                        itembox = ItemBox('Grenade' , x * TILE_SIZE , y * TILE_SIZE , itemboxes)
                        itemboxgroup.add(itembox)
                    elif tile == 10:#fire crate
                        itembox = ItemBox('Fireball' , x * TILE_SIZE , y * TILE_SIZE , itemboxes)
                        itemboxgroup.add(itembox)
                    elif tile == 9 or tile == 51:#exit
                        exitsign = Exit(img , x * TILE_SIZE , y * TILE_SIZE)
                        exitgroup.add(exitsign)
                    elif tile == 11:#player position
                        player = Player('player', x * TILE_SIZE , y * TILE_SIZE, 1 , 10 , 5 , 0 , 0 )
                        healthbar = HealthBar(10,51,player.health,player.health)
                    elif tile == 12:#c1 position
                        heavy = RangeEnemy('c1', x * TILE_SIZE , y * TILE_SIZE , 1 , 2 , 20 , 100 , 10 , 300 , 200 , 175 , 70 , 5)
                        enemygroup1.add(heavy)
                    elif tile == 13:#c2 position
                        enemy = RangeEnemy('c2', x * TILE_SIZE , y * TILE_SIZE , 1 , 3 , 10 , 100 , 20 , 250 , 200 , 175 , 70 , 10)
                        enemygroup1.add(enemy)
                    elif tile == 14:#c3 position
                        enemy = RangeEnemy('c3', x * TILE_SIZE , y * TILE_SIZE , 1 , 3 , 10 , 100 , 30 , 250 , 200 , 175 , 70 , 10)
                        enemygroup1.add(enemy)
                    elif tile == 15:#c4 position
                        enemy = RangeEnemy('c4', x * TILE_SIZE , y * TILE_SIZE , 1 , 0 , 1 , 100 , 50 , 400 , 300 , 250 , 110 , 20)
                        enemygroup1.add(enemy)
                    elif tile == 16:#c5 position
                        enemy = MeleeEnemy('c5', x * TILE_SIZE , y * TILE_SIZE , 1 , 4 , 80 , 800 ,100 , 0 , 0.3)
                        enemygroup2.add(enemy)
                    elif tile == 17:#godoffire position
                        enemy = MeleeEnemy('godoffire', x * TILE_SIZE , y * TILE_SIZE , 1 , 3 , 280 , 1200 , 400 , 0 , 1)
                        enemygroup2.add(enemy)
                    elif tile == 30:#c6 position
                        enemy = RangeEnemy('c6', x * TILE_SIZE , y * TILE_SIZE , 1 , 0 , 1 , 100 , 50 , 400 , 300 , 250 , 110 , 30)
                        enemygroup1.add(enemy)
                    elif tile == 31:#c7 position
                        enemy = MeleeEnemy('c7', x * TILE_SIZE , y * TILE_SIZE , 1 , 3 , 80 , 350 , 50 , 0 , 0.1)
                        enemygroup2.add(enemy)
                    elif tile == 32:#c8 position
                        enemy = RangeEnemy('c8', x * TILE_SIZE , y * TILE_SIZE , 1 , 4 , 3 , 100 , 30 , 400 , 100 , 250 , 110 , 20)
                        enemygroup1.add(enemy)
                    elif tile == 33:#Sage position
                        boss = Boss('Sage', x * TILE_SIZE , y * TILE_SIZE , 1 , 0 , 4 , 800 , 30 , 1400 , 300 , 0 , 100 , 100 , 4 , 0 , 0 ,0)
                        bossgroup.add(boss)
                    elif tile == 37:#the chad boss
                        boss = Boss('Boss', x * TILE_SIZE , y * TILE_SIZE , 1 , 5 , 4 , 4800 , 50 , 1400 , 400 , 0 , 100 , 100 , 4 , 5 , 0 ,0)
                        bossgroup.add(boss)
                    elif tile == 39:#Invincible position
                        boss = Boss('Invincible', x * TILE_SIZE , y * TILE_SIZE , 1 , 4 , 0 , 2800 , 80 , 1400 , 400 , 0 , 70 , 70 , 0 , 4 , 4 , 4)
                        bossgroup.add(boss)
                    elif tile == 44:#c9 position
                        enemy = MeleeEnemy('c9', x * TILE_SIZE , y * TILE_SIZE , 1 , 3 , 120 , 800 ,100 , 0 , 0.3)
                        enemygroup2.add(enemy)
                    elif tile == 55:#c10 position
                        enemy = RangeEnemy('c10', x * TILE_SIZE , y * TILE_SIZE , 1 , 2 , 20 , 100 , 10 , 300 , 200 , 175 , 70 , 5)
                        enemygroup1.add(enemy)
                    elif tile == 56:#General position
                        boss = Boss('General', x * TILE_SIZE , y * TILE_SIZE , 1 , 0 , 0 , 1000 , 40 , 1400 , 400 , 0 , 100 , 100 , 0 , 0 , 3 , 3)
                        bossgroup.add(boss)
                    elif tile == 57:#c11 position
                        enemy = MeleeEnemy('c11', x * TILE_SIZE , y * TILE_SIZE , 1 , 3 , 120 , 600 ,100 , 0 , 0.3)
                        enemygroup2.add(enemy)

        return player, healthbar
    
    def draw(self , screen_scroll , screen):
        for tile in self.obstacle_list:
            tile[1][0] += screen_scroll
            screen.blit(tile[0],tile[1])# 0 = image ,1 = rect
