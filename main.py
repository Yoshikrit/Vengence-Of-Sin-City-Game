import pygame
from pygame import mixer
import csv
from pygame.locals import *
import button
from playerweapons import Grenade 
from world import World 
from fade import ScreenFade

mixer.init()
pygame.init()

WINDOW_SIZE = (1200 , 800)
screen = pygame.display.set_mode(WINDOW_SIZE,0,32)#start window

pygame.display.set_caption('VENGENCE OF SIN CITY')#ชื่อเกม
icon = pygame.image.load('Pictures\logo.png')
pygame.display.set_icon(icon)

#set framerate
clock = pygame.time.Clock()

#game variable
gravity = 0.8#gravity 0.75
TILE_SIZE = 50
ROWS1 = 16
COLS1 = 144
TILE_TYPES = 58
level = 0
SCROLL_THRESH = 600 #ระยะที่playerไปที่มุมได้ก่อนเริ่มเลื่อนหน้าจอ
screen_scroll = 0
bg_scroll = 0
MAX_LEVELS = 5
start_intro = False
end_intro = False
sound_on = True

startgame = False
mainstate = "main"
gamestate = "main"

#player action variables
moving_left = False
moving_right = False
shoot = False
shoot2 = False
grenade = False
grenadethrown = False

#music and sound
pygame.mixer.music.load('Sounds\Batman.mp3')
pygame.mixer.music.set_volume(0.02)#set volume 30%
pygame.mixer.music.play(-1, 0.0 , 5000)# -1 = song loop fir ever , 0.0 = song delay , song fade in 5000 millisecond or 5 sec
jump_fx = pygame.mixer.Sound('Sounds\Jump.wav')
jump_fx.set_volume(0.02)
grenade_fx = pygame.mixer.Sound('Sounds\Grenade.wav')
grenade_fx.set_volume(0.02)
click_fx = pygame.mixer.Sound('Sounds\Click.wav')
click_fx.set_volume(0.02)

#all ammunation
bulletimg = pygame.image.load(f'Pictures\Weapons\Bullet.png').convert_alpha()
grenadeimg = pygame.image.load(f'Pictures\Weapons\grenade.png').convert_alpha()
fireballimg = pygame.image.load(f'Pictures\Weapons\Fireball.png').convert_alpha()
rpgimg = pygame.image.load(f'Pictures\Weapons\Rocket.png').convert_alpha()
laserimg = pygame.image.load(f'Pictures\Weapons\Laser.png').convert_alpha()

#all crates pick up
healthboximg = pygame.image.load(f'Pictures\Crates\heart.png').convert_alpha()
ammoboximg = pygame.image.load(f'Pictures\Crates\Bulletcrate.png').convert_alpha()
grenadeboximg = pygame.image.load(f'Pictures\Crates\grenadecrate.png').convert_alpha()
firecampimg = pygame.image.load(f'Pictures\Crates\campfire.png').convert_alpha()
itemboxes = {
    'Health' : healthboximg,
    'Ammo' : ammoboximg,
    'Grenade' : grenadeboximg,
    'Fireball' : firecampimg,
}

#define colours
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (243,114,32)
YELLOW = (255,255,0)
BLUE = (31,69,252)

#create text in main menu
def draw_text(text, font , color, surface, x , y):
    textobj = font.render(text, 1,color)
    textrect = textobj.get_rect()
    textrect.topleft = (x,y)
    surface.blit(textobj, textrect)

#set window
screen = pygame.display.set_mode(WINDOW_SIZE,0,32)#start window

#img
#background
darknight = pygame.image.load('Pictures\Backgrounds\city background.jpg')
military = pygame.image.load('Pictures\Backgrounds\military.jpg')
factory = pygame.image.load('Pictures\Backgrounds\Factory.jpg')
Moon = pygame.image.load('Pictures\Backgrounds\Moon.jpg')
lightcity = pygame.image.load('Pictures\Backgrounds\lightcity2.jpg')

def draw_bg1():
    width = factory.get_width()
    for x in range(6):
        screen.blit(factory ,  ((x * width) - bg_scroll * 0.5,0))

#button image
startimg = pygame.image.load('Pictures\Buttons\start.png').convert_alpha()
exitimg = pygame.image.load('Pictures\Buttons\exit.png').convert_alpha()
restartimg = pygame.image.load('Pictures\Buttons\Restart.png').convert_alpha()
nextimg = pygame.image.load('Pictures\Buttons\go.png').convert_alpha()
soundimg = pygame.image.load('Pictures\Buttons\Musicon.png').convert_alpha()
resumeimg = pygame.image.load('Pictures\Buttons\Resume.png').convert_alpha()
backimg = pygame.image.load('Pictures\Buttons\Back.png').convert_alpha()
exitimg = pygame.image.load('Pictures\Buttons\exit.png').convert_alpha()
l1img = pygame.image.load('Pictures\Buttons\Lvl1.png').convert_alpha()
l2img = pygame.image.load('Pictures\Buttons\Lvl2.png').convert_alpha()
l3img = pygame.image.load('Pictures\Buttons\Lvl3.png').convert_alpha()
l4img = pygame.image.load('Pictures\Buttons\Lvl4.png').convert_alpha()
l5img = pygame.image.load('Pictures\Buttons\Lvl5.png').convert_alpha()
mainmenuimg = pygame.image.load('Pictures\Buttons\mainmenu.png').convert_alpha()
l0img = pygame.image.load('Pictures\Buttons\Tutorial.png').convert_alpha()
backimg = pygame.image.load('Pictures\Buttons\Back.png').convert_alpha()
levelimg = pygame.image.load('Pictures\Buttons\Lvl.png').convert_alpha()

#type of font
font_main = pygame.font.SysFont(None, 50)#font for game name
font_intro = pygame.font.SysFont(None, 30)#font for intro
font = pygame.font.SysFont(None, 20)#font for main menu

#function to reset level
def reset_level():
    enemygroup1.empty()
    enemygroup2.empty()
    bossgroup.empty()
    bulletgroup1.empty()
    bulletgroup2.empty()
    grenadegroup.empty()
    fireballgroup1.empty()
    fireballgroup2.empty()
    lasergroup.empty()
    explosiongroup.empty()
    poofgroup.empty()
    bloodgroup.empty()
    itemboxgroup.empty()
    watergroup.empty()
    decorationgroup.empty()
    exitgroup.empty()

    #create empty tile
    data = []
    for row in range(ROWS1):
        r = [-1] * COLS1
        data.append(r)

    return data

intro_fade = ScreenFade(1 , BLACK , 40)
death_fade = ScreenFade(2 ,  BLACK , 40)
endchap0_fade = ScreenFade(2 ,  BLACK , 15)

#สร้างปุ่ม
startbutton = button.Button(WINDOW_SIZE[0] // 2 - 100 , WINDOW_SIZE[1] // 2   , startimg , 1)
exitbutton = button.Button(WINDOW_SIZE[0] // 2 - 100 , WINDOW_SIZE[1] // 2 + 150 , exitimg , 1)
restartbutton = button.Button(WINDOW_SIZE[0] // 2 - 100  , WINDOW_SIZE[1] // 2 , restartimg , 1)
nextbutton = button.Button(WINDOW_SIZE[0] // 2 - 100 , WINDOW_SIZE[1] // 2 , nextimg , 1)
soundbutton = button.Button(1150 , 0 , soundimg , 0.5)
resumebutton = button.Button(WINDOW_SIZE[0] // 2 - 100 , WINDOW_SIZE[1] // 2 - 300, resumeimg , 1)
menubutton = button.Button(WINDOW_SIZE[0] // 2 - 100 , WINDOW_SIZE[1] // 2 - 150, mainmenuimg , 1)
exitbutton2 = button.Button(WINDOW_SIZE[0] // 2 + 100 , WINDOW_SIZE[1] // 2 + 100 , exitimg , 1)
lv0button = button.Button(WINDOW_SIZE[0] // 2 - 450 , WINDOW_SIZE[1] // 2 - 150, l0img , 1)
lv1button = button.Button(WINDOW_SIZE[0] // 2 - 300 , WINDOW_SIZE[1] // 2 - 150, l1img , 1)
lv2button = button.Button(WINDOW_SIZE[0] // 2 - 150 , WINDOW_SIZE[1] // 2 - 150, l2img , 1)
lv3button = button.Button(WINDOW_SIZE[0] // 2 + 50 , WINDOW_SIZE[1] // 2 - 150, l3img , 1)
lv4button = button.Button(WINDOW_SIZE[0] // 2 + 200 , WINDOW_SIZE[1] // 2 - 150, l4img , 1)
lv5button = button.Button(WINDOW_SIZE[0] // 2 + 350 , WINDOW_SIZE[1] // 2 - 150, l5img , 1)
backbutton = button.Button(WINDOW_SIZE[0] // 2 - 100 , WINDOW_SIZE[1] // 2 + 150, backimg , 1)
menubutton2 = button.Button(WINDOW_SIZE[0] // 2 - 300 , WINDOW_SIZE[1] // 2 + 100, mainmenuimg , 1)

#สร้าง sprite group
enemygroup1 = pygame.sprite.Group()
enemygroup2 = pygame.sprite.Group()
bossgroup = pygame.sprite.Group()
bulletgroup1 = pygame.sprite.Group()
bulletgroup2 = pygame.sprite.Group()
grenadegroup = pygame.sprite.Group()
rpggroup = pygame.sprite.Group()
fireballgroup1 = pygame.sprite.Group()
fireballgroup2 = pygame.sprite.Group()
lasergroup = pygame.sprite.Group()
explosiongroup = pygame.sprite.Group()
poofgroup = pygame.sprite.Group()
bloodgroup = pygame.sprite.Group()
itemboxgroup = pygame.sprite.Group()
decorationgroup = pygame.sprite.Group()
watergroup = pygame.sprite.Group()
exitgroup = pygame.sprite.Group()

#create empty tile list
world_data = []
for row in range(ROWS1):
    r = [-1] * COLS1
    world_data.append(r)
#load level and create
with open(f'level{level}_data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)
world = World()
player, healthbar = world.process_data(world_data, watergroup , decorationgroup , itemboxgroup , exitgroup , bossgroup , enemygroup1 ,enemygroup2 , itemboxes)

run = True
while run:

    clock.tick(60)#ให้windowรันframerateกี่fps
    screen.blit(darknight ,  (0,0))
    if startgame == False:
        #main menu
        if mainstate == "main":
            draw_text('VENGENCE OF SIN CITY', font_main, ORANGE, screen, 400, 150)
            #add buttons
            if startbutton.draw(screen):
                level = 0
                click_fx.play()
                mainstate = "level"

            if exitbutton.draw(screen):
                run = False
            
            if soundbutton.draw(screen):
                sound_on = not sound_on
                click_fx.play()
                if sound_on == True:
                    pygame.mixer.music.play(-1, 0.0 , 5000)# -1 = song loop fir ever , 0.0 = song delay , song fade in 5000 millisecond or 5 sec
                else:
                    pygame.mixer.music.stop()

        if mainstate == "level":
            screen.blit(levelimg ,  (WINDOW_SIZE[0] // 2 - 100 , WINDOW_SIZE[1] // 2 - 300))
            if lv0button.draw(screen):
                click_fx.play()
                level = 0
                startgame = True
                start_intro = True
            if lv1button.draw(screen):
                click_fx.play()
                level = 1
                startgame = True
                start_intro = True
            if lv2button.draw(screen):
                click_fx.play()
                level = 2
                startgame = True
                start_intro = True
            if lv3button.draw(screen):
                click_fx.play()
                level = 3
                startgame = True
                start_intro = True
            if lv4button.draw(screen):
                click_fx.play()
                level = 4
                startgame = True
                start_intro = True
            if lv5button.draw(screen):
                click_fx.play()
                level = 5
                startgame = True
                start_intro = True
            if backbutton.draw(screen):
                click_fx.play()
                mainstate = "main"
            bg_scroll = 0
            world_data = reset_level()
            #load level and create
            with open(f'level{level}_data.csv', newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for x, row in enumerate(reader):
                    for y, tile in enumerate(row):
                        world_data[x][y] = int(tile)
            world = World()
            player, healthbar  = world.process_data(world_data, watergroup , decorationgroup , itemboxgroup , exitgroup , enemygroup1 , enemygroup2 , bossgroup , itemboxes)

        if mainstate == "pause":
            pygame.draw.rect(screen, BLACK , (0 ,0, WINDOW_SIZE[0], WINDOW_SIZE[1]))
            if resumebutton.draw(screen):
                startgame = True
                click_fx.play()

            if menubutton.draw(screen):
                startgame = False
                mainstate = "main"
                click_fx.play()

            if restartbutton.draw(screen):
                startgame = True
                click_fx.play()
                bg_scroll = 0
                world_data = reset_level()
                #load level and create
                with open(f'level{level}_data.csv', newline='') as csvfile:
                    reader = csv.reader(csvfile, delimiter=',')
                    for x, row in enumerate(reader):
                        for y, tile in enumerate(row):
                            world_data[x][y] = int(tile)
                world = World()
                player, healthbar  = world.process_data(world_data, watergroup , decorationgroup , itemboxgroup , exitgroup , enemygroup1 , enemygroup2 , bossgroup , itemboxes)

            if exitbutton.draw(screen):
                run = False
            if soundbutton.draw(screen):
                sound_on = not sound_on
                if sound_on == True:
                    pygame.mixer.music.play(-1, 0.0 , 5000)# -1 = song loop fir ever , 0.0 = song delay , song fade in 5000 millisecond or 5 sec
                else:
                    pygame.mixer.music.stop()
       
    else:
        #update background
        if level == 3:
            screen.blit(military ,  (0,0))
        elif level == 4:
            draw_bg1()
        else:
            screen.blit(darknight ,  (0,0))
        #draw world
        world.draw(screen_scroll , screen)
        
        player.update(poofgroup)
        player.draw(screen)

        for enemy in enemygroup1:
            enemy.ai(player , screen_scroll  ,world ,watergroup ,bulletgroup2 ,rpggroup)
            enemy.update(poofgroup , itemboxgroup , itemboxes)
            enemy.Damage(player , enemygroup1)
            enemy.draw(screen)

        for enemy in enemygroup2:
            enemy.ai(player , screen_scroll  ,world ,watergroup)
            enemy.update(poofgroup , exitgroup)
            enemy.Damage(player , enemygroup2)
            enemy.draw(screen) 

        for boss in bossgroup:
            boss.ai(player , screen_scroll ,world ,watergroup  , fireballgroup2 , lasergroup)
            boss.update(poofgroup , exitgroup)
            boss.Damage(player , bossgroup)
            boss.draw(screen) 

        #update and draw groups
        bulletgroup1.update( player , screen_scroll , world ,bulletgroup1 , enemygroup1 , enemygroup2 , bossgroup)
        bulletgroup2.update( player , screen_scroll , world , bulletgroup2 , bloodgroup)
        rpggroup.update(player , screen_scroll , world , rpggroup , explosiongroup , bloodgroup)
        grenadegroup.update( screen_scroll , world , explosiongroup , player , enemygroup1 , enemygroup2 , bossgroup, bloodgroup )
        fireballgroup1.update(screen_scroll , player , world , enemygroup1 , enemygroup2 , bossgroup , fireballgroup1)
        fireballgroup2.update(screen_scroll , player , world , fireballgroup2 , bloodgroup)
        lasergroup.update(player , screen_scroll , world ,lasergroup , bloodgroup)
        explosiongroup.update(screen_scroll)
        poofgroup.update(screen_scroll)
        bloodgroup.update(screen)
        itemboxgroup.update(screen_scroll , player)
        decorationgroup.update(screen_scroll)
        watergroup.update(screen_scroll)
        exitgroup.update(screen_scroll)
        bulletgroup1.draw(screen)
        bulletgroup2.draw(screen)
        rpggroup.draw(screen)
        grenadegroup.draw(screen)
        fireballgroup1.draw(screen)
        fireballgroup2.draw(screen)
        lasergroup.draw(screen)
        explosiongroup.draw(screen)
        poofgroup.draw(screen)
        itemboxgroup.draw(screen)
        decorationgroup.draw(screen)
        watergroup.draw(screen)
        exitgroup.draw(screen)

        #intro
        if start_intro == True:
            if intro_fade.fade(screen):
                start_intro = False
                intro_fade.fade_counter = 0
        if end_intro == True:
            if endchap0_fade.fade(screen):
                end_intro = False
                endchap0_fade.fade_counter = 0

        #show player status
        if level == 0:
            draw_text('Tutorial', font_main , WHITE , screen , 10 , 700)
            draw_text(': Forest Camp', font_intro , WHITE , screen , 10 , 740)
            if player.rect.x < 500:
                draw_text('Welcome Player To The Tutorial', font_main , WHITE , screen , 10 , 10)
                draw_text(f'If You Want To Walk ', font_intro , YELLOW , screen , 10 , 55)
                draw_text(f'Press Key LEFT And Key RIGHT To Walk ', font_intro , YELLOW , screen , 10 , 85)
                draw_text('Press Key UP To Jump Across The River', font_intro , WHITE , screen , 10 , 115)
                draw_text('Dont Step On The Water', font_intro , BLUE , screen , 10 , 145)
                draw_text('Because You Are A Fire', font_intro , RED , screen , 10 , 175)
            if player.rect.x > 500:
                draw_text('Your Mission Is To Defeat All Hidden Evil And Darkness In This Sin City', font_main , WHITE , screen , 10 , 10)
                draw_text(f'Thats Run By The Criminals , Hero And  Evil Ploiticians Like The Gotham City', font_intro , YELLOW , screen , 10 , 55)
                draw_text(f'But To Do That You Need A Weapon To Fight, Pick An Ammo Crate To Get Weapons ', font_intro , YELLOW , screen , 10 , 85)
                draw_text('Press Key Z To Shoot Bullet, To Deal Some Damage To Enemy', font_intro , ORANGE , screen , 10 , 115)
                draw_text('Press Key X To Shoot Grenades, Its Gonna Deal Blast Damage', font_intro , ORANGE , screen , 10 , 145)
                draw_text('But You Need To Beware The Blast Radius, It Could Kill You', font_intro , RED , screen , 10 , 175)
                draw_text('And Press Key C To Shoot Sacred Fire, The Strongest Weapon. Deal High Damage To The Boss', font_intro , ORANGE , screen , 10 , 205)
                draw_text('Every Enemy Have Different Behavior, So Be Careful, All Of Them Could Harm You', font_intro , WHITE , screen , 10 , 235)
                draw_text('Pick The Health Box Will Heal You 50% Of Max Health', font_intro , ORANGE, screen , 10 , 265)
                draw_text('Everything Is Limits So Use It Propery, Get To The Portal And Find Every Evil In The City', font_intro , WHITE , screen , 10 , 295)
                

        if level == 1:
            draw_text('Chapter 1', font_main , WHITE , screen , 10 , 700)
            draw_text(': Sin Suburb', font_intro , WHITE , screen , 10 , 740)
            draw_text('Player', font_main , WHITE , screen , 10 , 10)
            healthbar.draw(player.health , screen)#print health bar
            draw_text(f'AMMO : ', font_intro , YELLOW , screen , 10 , 85)
            screen.blit(bulletimg , (96 , 87.5))
            draw_text(f'x {player.ammo}', font_intro , YELLOW , screen , 115 , 85)
            draw_text('Press Z to shoot', font_intro , WHITE , screen , 10 , 115)
            if player.rect.x < 500:
                draw_text('Objective :', font_main , WHITE , screen , 1000 , 10)
                draw_text('Defeat The God Of Fire', font_main, RED , screen , 815 , 50)
                draw_text('The Politician Of The Hell', font_intro, YELLOW , screen , 935 , 93)
                draw_text('Alias : The Thug Boss Of Sin City', font_intro, WHITE , screen , 860 , 123)

        if level == 2:
            draw_text('Chapter 2', font_main , WHITE , screen , 10 , 700)
            draw_text(': Dark Gate Harbor', font_intro , WHITE , screen , 10 , 740)
            draw_text('Player', font_main , WHITE , screen , 10 , 10)
            healthbar.draw(player.health , screen)#print health bar
            draw_text(f'AMMO : ', font_intro , WHITE , screen , 10 , 85)
            screen.blit(bulletimg , (96 , 87.5))
            draw_text(f'x {player.ammo}', font_intro , WHITE , screen , 115 , 85)
            draw_text(f'GRENADE : ', font_intro , WHITE , screen , 10 , 115)
            screen.blit(grenadeimg , (128 , 116.5))
            draw_text(f'x {player.grenades}', font_intro , WHITE , screen , 149 , 115)
            draw_text(f'Press X to shoot', font_intro , WHITE , screen , 10 , 145)
            if player.rect.x < 500:
                draw_text('Objective :', font_main , WHITE , screen , 1000 , 10)
                draw_text('Defeat The Dark Sage', font_main, RED , screen , 820 , 50)
                draw_text('Leader Of The Dark Gate', font_intro, YELLOW , screen , 940 , 93)
                draw_text('Alias : The Crazy Sorcerer', font_intro, WHITE , screen , 925 , 123)

        if level == 3:
            draw_text('Chapter 3', font_main , WHITE , screen , 10 , 700)
            draw_text(': Military Headquarters', font_intro , WHITE , screen , 10 , 740)
            draw_text('Player', font_main , WHITE , screen , 10 , 10)
            healthbar.draw(player.health , screen)#print health bar
            draw_text(f'AMMO : ', font_intro , WHITE , screen , 10 , 85)
            screen.blit(bulletimg , (96 , 87.5))
            draw_text(f'x {player.ammo}', font_intro , WHITE , screen , 115 , 85)
            draw_text(f'GRENADE : ', font_intro , WHITE , screen , 10 , 115)
            screen.blit(grenadeimg , (128 , 116.5))
            draw_text(f'x {player.grenades}', font_intro , WHITE , screen , 149 , 115)
            if player.rect.x < 500:
                draw_text('Objective :', font_main , WHITE , screen , 1000 , 10)
                draw_text('Defeat The Rambo', font_main, RED , screen , 880 , 50)
                draw_text('The General Of Sin City', font_intro, YELLOW , screen , 945 , 93)
                draw_text('Alias : The World War Weapons Seller', font_intro, WHITE , screen , 810 , 123)
            
        if level == 4:
            draw_text('Chapter 4', font_main , WHITE , screen , 10 , 700)
            draw_text(': Drug Factory', font_intro , WHITE , screen , 10 , 740)
            draw_text('Player', font_main , WHITE , screen , 10 , 10)
            healthbar.draw(player.health , screen)#print health bar
            draw_text(f'AMMO : ', font_intro , WHITE , screen , 10 , 85)
            screen.blit(bulletimg , (96 , 87.5))
            draw_text(f'x {player.ammo}', font_intro , WHITE , screen , 115 , 85)
            draw_text(f'GRENADE : ', font_intro , WHITE , screen , 10 , 115)
            screen.blit(grenadeimg , (128 , 116.5))
            draw_text(f'x {player.grenades}', font_intro , WHITE , screen , 149 , 115)
            draw_text(f'SACRED FIRE : ', font_intro , WHITE , screen , 10 , 145)
            screen.blit(fireballimg , (162 , 148))
            draw_text(f'x {player.fireball}', font_intro , WHITE , screen , 182 , 145)
            draw_text(f'Press C to shoot', font_intro , WHITE , screen , 10 , 175)
            if player.rect.x < 500:
                draw_text('Objective :', font_main , WHITE , screen , 1000 , 10)
                draw_text('Defeat The Invincible', font_main, RED , screen , 835 , 50)
                draw_text('The Strongest Hero In The World', font_intro, YELLOW , screen , 865 , 93)
                draw_text('Alias : Homelander Of The Sin City', font_intro, WHITE , screen , 840 , 123)
        
        if level == 5:
            draw_text('Chapter 5', font_main , WHITE , screen , 10 , 700)
            draw_text(': Sin City Capital', font_intro , WHITE , screen , 10 , 740)
            draw_text('Player', font_main , WHITE , screen , 10 , 10)
            healthbar.draw(player.health , screen)#print health bar
            draw_text(f'AMMO : ', font_intro , WHITE , screen , 10 , 85)
            screen.blit(bulletimg , (96 , 87.5))
            draw_text(f'x {player.ammo}', font_intro , WHITE , screen , 115 , 85)
            draw_text(f'GRENADE : ', font_intro , WHITE , screen , 10 , 115)
            screen.blit(grenadeimg , (128 , 116.5))
            draw_text(f'x {player.grenades}', font_intro , WHITE , screen , 149 , 115)
            draw_text(f'SACRED FIRE : ', font_intro , WHITE , screen , 10 , 145)
            screen.blit(fireballimg , (162 , 148))
            draw_text(f'x {player.fireball}', font_intro , WHITE , screen , 182 , 145)
            if player.rect.x < 500:
                draw_text('Objective :', font_main , WHITE , screen , 1000 , 10)
                draw_text('Defeat The Chad', font_main, RED , screen , 905 , 50)
                draw_text('The One Above All President', font_intro, YELLOW , screen , 905 , 93)
                draw_text('Alias : The Strongest Man In The Universe', font_intro, WHITE , screen , 775 , 123)        

        #update player actions
        if player.alive:
            #shoot bullets
            if shoot:
                player.shoot(bulletgroup1)
            elif shoot2:
                player.shoot2(fireballgroup1)
            #throw grenades
            elif grenade and grenadethrown == False and player.grenades > 0:
                grenade = Grenade(player.rect.centerx + (0.5 * player.rect.size[0] * player.direction),\
                            player.rect.top, player.direction)
                grenadegroup.add(grenade)
                #reduce grenades
                player.grenades -= 1#reduce grenade
                grenade_fx.play()
                grenadethrown = True
            screen_scroll , level_complete = player.move(moving_left, moving_right , world ,watergroup , exitgroup, bg_scroll , screen_scroll)
            bg_scroll -= screen_scroll
            #check if complete
            
            #check cutscene after win
            if level_complete:
                player.speed = 0
                player.vel_y = 0
                end_intro = False
                if endchap0_fade.fade(screen):
                    if level == 0:
                        draw_text('We Got An Info About The Place Where The First Criminal Hide', font_main , WHITE , screen , WINDOW_SIZE[0] // 2 - 500 , WINDOW_SIZE[1] // 2 - 300 )
                        draw_text('This Is The Suburb Where The Politician Names God Of Fire Do His Dirty Job', font_intro , WHITE , screen , WINDOW_SIZE[0] // 2 - 390, WINDOW_SIZE[1] // 2 - 240)
                        draw_text('He Is One Of The Evil Group Member Who Like to Oppressed The People In This City', font_intro , WHITE , screen , WINDOW_SIZE[0] // 2 - 420, WINDOW_SIZE[1] // 2 -207)
                        draw_text('You Need Take Him Down And Find The Infomation About Another Evil In This City', font_intro , WHITE , screen , WINDOW_SIZE[0] // 2 - 390, WINDOW_SIZE[1] // 2 - 174)
                        draw_text('But The Thing Is. God Of Fire Is The Man With Fire Around His Body , So Be Careful', font_intro , RED , screen , WINDOW_SIZE[0] // 2 - 410, WINDOW_SIZE[1] // 2 - 140)
                        draw_text('Get Ready For Your Mission', font_main , YELLOW , screen , WINDOW_SIZE[0] // 2  - 220, WINDOW_SIZE[1] // 2 - 100 )
                    if level == 1:
                        draw_text('From The Info You Got, The Next Place Is Harbor', font_main , WHITE , screen , WINDOW_SIZE[0] // 2 - 400 , WINDOW_SIZE[1] // 2 - 300 )
                        draw_text('Where The Religious Leader Of The Dark Gate Names Dark Sage Hide', font_intro , WHITE , screen , WINDOW_SIZE[0] // 2 - 340, WINDOW_SIZE[1] // 2 - 240)
                        draw_text('He Is One Of The Evil Group Member Who Lead People To Do The Bad Things', font_intro , WHITE , screen , WINDOW_SIZE[0] // 2 - 380, WINDOW_SIZE[1] // 2 -207)
                        draw_text('But Now He Is Doing Some Ritual To Create Sacred Fire', font_intro , WHITE , screen , WINDOW_SIZE[0] // 2 - 280, WINDOW_SIZE[1] // 2 - 174)
                        draw_text('You Need To Take Him Down And Get That Sacred Fire To Fight Another Evil Members', font_intro , RED , screen , WINDOW_SIZE[0] // 2 - 410, WINDOW_SIZE[1] // 2 - 140)
                        draw_text('Get Ready For Your Mission', font_main , YELLOW , screen , WINDOW_SIZE[0] // 2  - 220, WINDOW_SIZE[1] // 2 - 100 )
                        
                    if level == 2:
                        draw_text('Good Job , Your Info Is Really Useful', font_main , WHITE , screen , WINDOW_SIZE[0] // 2 - 300 , WINDOW_SIZE[1] // 2 - 300 )
                        draw_text('Military Headquarters Is The Next One, To Stop The General Rambo', font_intro , WHITE , screen , WINDOW_SIZE[0] // 2 - 320, WINDOW_SIZE[1] // 2 - 240)
                        draw_text('This Man Sell Weapons To The Criminals And Want To Create His Own Colonies', font_intro , WHITE , screen , WINDOW_SIZE[0] // 2 - 380, WINDOW_SIZE[1] // 2 -207)
                        draw_text('We Need To Stop Him, Before Him And His Evil Group Will Start The World War', font_intro , WHITE , screen , WINDOW_SIZE[0] // 2 - 370, WINDOW_SIZE[1] // 2 - 174)
                        draw_text('People Will Not Realise That His General Is Starting The War And People Will Be Dead', font_intro , RED , screen , WINDOW_SIZE[0] // 2 - 410, WINDOW_SIZE[1] // 2 - 140)
                        draw_text('Get Ready For Your Mission', font_main , YELLOW , screen , WINDOW_SIZE[0] // 2  - 220, WINDOW_SIZE[1] // 2 - 100 )
                        
                    if level == 3:
                        draw_text('Nice Work , The Next Mission Is A Tough One', font_main , WHITE , screen , WINDOW_SIZE[0] // 2 - 360 , WINDOW_SIZE[1] // 2 - 300 )
                        draw_text('From The Info, The Next Place Is At Drug Factory, Where The Invincible Lives', font_intro , WHITE , screen , WINDOW_SIZE[0] // 2 - 360, WINDOW_SIZE[1] // 2 - 240)
                        draw_text('He Is The Strongest Hero In The World That People In This City Praise As A Good Hero', font_intro , WHITE , screen , WINDOW_SIZE[0] // 2 - 400, WINDOW_SIZE[1] // 2 -207)
                        draw_text('But Behind His Mask, He Is A Drug Dealer And Kill A Lot Of Innocent In Any Accident Thats He Fighting Villian', font_intro , WHITE , screen , WINDOW_SIZE[0] // 2 - 540, WINDOW_SIZE[1] // 2 - 174)
                        draw_text('Use Ya Packs Weapons To Take Him Down, But Sacred Fire Is Like A Kryptonite For Him', font_intro , RED , screen , WINDOW_SIZE[0] // 2 - 410, WINDOW_SIZE[1] // 2 - 140)
                        draw_text('Get Ready For Your Mission', font_main , YELLOW , screen , WINDOW_SIZE[0] // 2  - 220, WINDOW_SIZE[1] // 2 - 100 )
                        
                    if level == 4:
                        draw_text('Nice Work. The Last Page Wrote That The Last Man Is The President', font_main , WHITE , screen , WINDOW_SIZE[0] // 2 - 560 , WINDOW_SIZE[1] // 2 - 300 )
                        draw_text('He Is The Evil Leader Who Controlled This City In A Bad Way', font_intro , WHITE , screen , WINDOW_SIZE[0] // 2 - 300, WINDOW_SIZE[1] // 2 - 240)
                        draw_text('People In This City Never Realise That He And Invincible Are Evil Criminal', font_intro , WHITE , screen , WINDOW_SIZE[0] // 2 - 370, WINDOW_SIZE[1] // 2 -207)
                        draw_text('If We End Him, This City Will Be Safe And People Will Get Their Happy Life Back', font_intro , WHITE , screen , WINDOW_SIZE[0] // 2 - 390, WINDOW_SIZE[1] // 2 - 174)
                        draw_text('But There Is A Lot Of Mercenary Around The City, He Probably Knew Thats We Are Coming For Him', font_intro , RED , screen , WINDOW_SIZE[0] // 2 - 480, WINDOW_SIZE[1] // 2 - 140)
                        draw_text('Get Ready For The Last Mission', font_main , YELLOW , screen , WINDOW_SIZE[0] // 2  - 265, WINDOW_SIZE[1] // 2 - 100 )
                        
                    if level == 5:
                        draw_text('Finally Now We Have End All Evil Criminial', font_main , WHITE , screen , WINDOW_SIZE[0] // 2 - 360 , WINDOW_SIZE[1] // 2 - 300 )
                        draw_text('But There Is A Letter Drop From Him, Read It To Know What He Wrote', font_intro , WHITE , screen , WINDOW_SIZE[0] // 2 - 340, WINDOW_SIZE[1] // 2 - 240)
                        draw_text('Dear Everyone, I Tried To Make The World That I Could Do Everything Like I Want', font_intro , YELLOW , screen , WINDOW_SIZE[0] // 2 - 380, WINDOW_SIZE[1] // 2 -207)
                        draw_text('But The Environment Changed Me To Be Bad Because Many Bad Things Exist In My Life', font_intro , YELLOW , screen , WINDOW_SIZE[0] // 2 - 375, WINDOW_SIZE[1] // 2 - 174)
                        draw_text('People Always Hide There Evil Inside There Mind And Show It When Nobody See It', font_intro , YELLOW , screen , WINDOW_SIZE[0] // 2 - 390, WINDOW_SIZE[1] // 2 - 140)
                        draw_text('Im Sorry For What I Have Done - The Chad', font_main , YELLOW , screen , WINDOW_SIZE[0] // 2  - 320, WINDOW_SIZE[1] // 2 - 100 )
                        
                    if nextbutton.draw(screen):
                        end_intro = True
                        start_intro = True
                        level += 1
                        bg_scroll = 0
                        world_data = reset_level()
                        if level <= MAX_LEVELS:
                            with open(f'level{level}_data.csv', newline='') as csvfile:
                                reader = csv.reader(csvfile, delimiter=',')
                                for x, row in enumerate(reader):
                                    for y, tile in enumerate(row):
                                        world_data[x][y] = int(tile)
                            world = World()
                            player, healthbar = world.process_data(world_data , watergroup , decorationgroup , itemboxgroup , exitgroup , enemygroup1 , enemygroup2 , bossgroup , itemboxes)
                    if exitbutton.draw(screen):
                        run = False
                    if soundbutton.draw(screen):
                        sound_on = not sound_on
                        if sound_on == True:
                            pygame.mixer.music.play(-1, 0.0 , 5000)# -1 = song loop fir ever , 0.0 = song delay , song fade in 5000 millisecond or 5 sec
                        else:
                            pygame.mixer.music.stop()

            if level > MAX_LEVELS:
                start_intro = False
                pygame.draw.rect(screen, BLACK , (0 ,0, WINDOW_SIZE[0], WINDOW_SIZE[1]))
                screen.blit(darknight ,  (0,0))
                draw_text('You Have Defeat All Evil In This Sin City', font_main , WHITE , screen , WINDOW_SIZE[0] // 2 - 330 , WINDOW_SIZE[1] // 2 - 300 )
                draw_text('In The Future, People Will Live Happily Forever', font_main , WHITE , screen , WINDOW_SIZE[0] // 2 - 380, WINDOW_SIZE[1] // 2 - 250)
                draw_text('Evil Is The Thing Thats People Cant See It Even Its Everywhere', font_main , WHITE , screen , WINDOW_SIZE[0] // 2 - 490, WINDOW_SIZE[1] // 2 -200)
                draw_text('Thank You For Playing', font_main , YELLOW , screen , WINDOW_SIZE[0] // 2  - 215, WINDOW_SIZE[1] // 2 - 150 )
                if exitbutton2.draw(screen):
                    run = False
                if soundbutton.draw(screen):
                    sound_on = not sound_on
                    if sound_on == True:
                        pygame.mixer.music.play(-1, 0.0 , 5000)# -1 = song loop fir ever , 0.0 = song delay , song fade in 5000 millisecond or 5 sec
                    else:
                        pygame.mixer.music.stop()
                if menubutton2.draw(screen):
                    startgame = False
                    mainstate = "main"
                    click_fx.play()
                            
        else:
            screen_scroll = 0
            if death_fade.fade(screen):
                draw_text('Game Over', font_main , YELLOW , screen , WINDOW_SIZE[0] // 2  - 100, WINDOW_SIZE[1] // 2 - 150 )
                if restartbutton.draw(screen):
                    click_fx.play()
                    death_fade.fade_counter = 0
                    start_intro = True
                    bg_scroll = 0
                    world_data = reset_level()
                    #load level and create
                    with open(f'level{level}_data.csv', newline='') as csvfile:
                        reader = csv.reader(csvfile, delimiter=',')
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                world_data[x][y] = int(tile)
                    world = World()
                    player, healthbar  = world.process_data(world_data, watergroup , decorationgroup , itemboxgroup , exitgroup , enemygroup1 , enemygroup2 , bossgroup , itemboxes)
                
                elif exitbutton.draw(screen):
                    run = False
                if soundbutton.draw(screen):
                    sound_on = not sound_on
                    if sound_on == True:
                        pygame.mixer.music.play(-1, 0.0 , 5000)# -1 = song loop fir ever , 0.0 = song delay , song fade in 5000 millisecond or 5 sec
                    else:
                        pygame.mixer.music.stop()


    for event in pygame.event.get():
        #quit game
        if event.type == pygame.QUIT:
            run = False
        #keyboard presses
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                moving_left = True
            if event.key == K_RIGHT:
                moving_right = True
            if event.key == K_UP and player.alive:
                player.jump = True
                jump_fx.play()
            if event.key == K_z:
                shoot = True
            if event.key == K_x:
                grenade = True
            if event.key == K_c:
                shoot2 = True
            if event.key == K_ESCAPE:
                if startgame == True:
                    mainstate = "pause"
                    startgame = False
                    click_fx.play()
                
        #keyboard button released
        #ไม่ให้คำสั่งทำงานไปเรื่อยๆไม่รู้จบ    
        if event.type == KEYUP:
            if event.key == K_LEFT:
                moving_left = False
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_z:
                shoot = False
            if event.key == K_x:
                grenade = False
                grenadethrown = False
            if event.key == K_c:
                shoot2 = False

    pygame.display.update()

pygame.quit()

