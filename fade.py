import pygame

WINDOW_SIZE = (1200 , 800)

class ScreenFade():
    def __init__(self , direction , colour , speed):
        self.direction = direction
        self.colour = colour
        self.speed = speed
        self.fade_counter = 0

    def fade(self,screen):
        fade_complete = False
        self.fade_counter += self.speed

        if self.direction == 1:#whole screen fade
            pygame.draw.rect(screen, self.colour , (0 - self.fade_counter,0, WINDOW_SIZE[0] // 2, WINDOW_SIZE[1]))#เริ่ม xy จบ xy
            pygame.draw.rect(screen, self.colour , (WINDOW_SIZE[0] // 2 + self.fade_counter,0, WINDOW_SIZE[0], WINDOW_SIZE[1]))#เริ่ม xy จบ xy
            pygame.draw.rect(screen, self.colour , (0 , 0- self.fade_counter, WINDOW_SIZE[0] , WINDOW_SIZE[1]//2))#เริ่ม xy จบ xy
            pygame.draw.rect(screen, self.colour , (0,WINDOW_SIZE[1]//2 + self.fade_counter, WINDOW_SIZE[0] , WINDOW_SIZE[1]))#เริ่ม xy จบ xy
            
        if self.direction == 2: #vertical screen fade down
            pygame.draw.rect(screen, self.colour , (0,0, WINDOW_SIZE[0], 0 + self.fade_counter))
        if self.fade_counter >= WINDOW_SIZE[0]:
            fade_complete = True
        
        return fade_complete