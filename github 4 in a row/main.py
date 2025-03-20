import pygame
import sys
import numpy as np

pygame.init()

#barve
white = (255,255,255)
green = (0,255,0)
red = (255,0,0)
black = (0,0,0)
yellow = (255,255,0)
#dimenzije

height, width = 700, 700




class GameMenu:
    def __init__(self):
        pygame.display.set_caption("chose a game mode")
        self.font = pygame.font.Font(None,50)
        self.screen = pygame.display.set_mode((width,height))

        #ozadje
        self.background = pygame.image.load("slike/background.jpg")
        self.background = pygame.transform.scale(self.background, (width,height))  # Prilagodi velikost
        #gumbi za izbor načina igre
        self.button1v1 = pygame.Rect((width / 2)-(width*0.3)/2 ,(height / 2)-(height*0.1)/2,width*0.3,height*0.1)
        self.buttonAi = pygame.Rect((width / 2)-(width*0.3)/2 ,(height / 2)-(height*0.5)/2,width*0.3,height*0.1)
        self.game_mode = None  # način igre dam na None
    
    #za ozadje
    def set_background(self):
        self.screen.blit(self.background,(0,0))


    #narišem gumbe in besedilo na zaslon
    def buttons(self):
        pygame.draw.rect(self.screen,black,self.button1v1)
        pygame.draw.rect(self.screen,black,self.buttonAi)
        text_1v1 = self.font.render("2 players",True,white)
        text_Ai = self.font.render("versus Ai",True,white)

        self.screen.blit(text_1v1, (self.button1v1.x + 10, self.button1v1.y + 30))
        self.screen.blit(text_Ai, (self.buttonAi.x + 5, self.buttonAi.y + 30))
    


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

menu = GameMenu()
selected_mode = menu.run()
pygame.quit()






pygame.quit()