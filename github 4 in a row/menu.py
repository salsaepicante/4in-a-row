import pygame
import sys
import numpy as np

pygame.init()
pygame.mixer.init()
#barve
white = (255,255,255)
green = (0,255,0)
red = (255,0,0)
black = (0,0,0)
yellow = (255,255,0)
dark_blue = (0, 0, 190)

#dimenzije

height, width = 700, 700




class GameMenu:
    def __init__(self):
        pygame.display.set_caption("chose a game mode")
        self.font = pygame.font.Font("github 4 in a row/fonts/arcade_font.ttf",30)
        self.screen = pygame.display.set_mode((width,height))

        
        self.connect4_title = pygame.image.load("github 4 in a row/slike/title_4.png")
        self.connect4_title = pygame.transform.scale(self.connect4_title, (width * 0.5,height * 0.5))
        self.background = pygame.image.load("github 4 in a row/slike/background.jpg")
        self.background = pygame.transform.scale(self.background, (width,height)) 
     
        self.button1v1 = pygame.Rect((width / 2)-(width*0.4)/2 ,(height)-(height*0.3),width*0.4,height*0.1)
        self.buttonAi = pygame.Rect((width / 2)-(width*0.4)/2 ,(height)-(height*0.45),width*0.4,height*0.1)
        #self.buttonAi = pygame.Rect()
        self.game_mode = None 
        self.menu_music()  

    def menu_music(self):
        pygame.mixer.music.load("github 4 in a row/sounds/intro.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

    def set_background(self):
        self.screen.blit(self.background,(0,0))


    def buttons(self):
        
        #pygame.draw.rect(self.screen,black,self.button1v1)
        #pygame.draw.rect(self.screen,black,self.buttonAi)
        self.text_1v1 = self.font.render("2 players",True,white)
        self.text_Ai = self.font.render("Versus Ai",True,white)
        self.screen.blit(self.connect4_title,(width/2 - self.connect4_title.get_width()/2, 20))
        self.screen.blit(self.text_1v1, (self.button1v1.x  + 15 , self.button1v1.y  + 15))
        self.screen.blit(self.text_Ai, (self.buttonAi.x  + 15, self.buttonAi.y  + 15))
    


    def izberi_mode(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.button1v1.collidepoint(event.pos):
                    self.game_mode = "1v1"
                    return False
                if self.buttonAi.collidepoint(event.pos):
                    self.game_mode = "Ai"
                    return False
        return True

    def run(self):
        running = True
        while running:
            self.set_background()
            self.buttons()
            pygame.display.flip()
            running = self.izberi_mode()
        return self.game_mode

"""menu = GameMenu()
selected_mode = menu.run()
pygame.quit()


print(selected_mode)



pygame.quit()"""