import pygame
import sys
from menu import width, height, red, green, black, white,yellow


class AI_difficulty:
    def __init__(self):
        pygame.display.set_caption("Choose AI difficulty")
        self.screen = pygame.display.set_mode((width,height))
        self.font = pygame.font.Font("github 4 in a row/fonts/arcade_font.ttf",30)
        self.screen = pygame.display.set_mode((width,height))

        #ozadje
        self.background = pygame.image.load("github 4 in a row/slike/background.jpg")
        self.background = pygame.transform.scale(self.background, (width,height)) 
        #gumbi za izbor načina igre
        self.button_easy = pygame.Rect((width)-(width*0.75) ,(height / 2)-(height*0.3)/2,width*0.2,height*0.1)
        self.button_hard = pygame.Rect((width)-(width*0.45) ,(height / 2)-(height*0.3)/2,width*0.2,height*0.1)
        self.game_mode = None  # način igre dam na None
    
    #za ozadje
    def set_background(self):
        self.screen.blit(self.background,(0,0))


    #narišem gumbe in besedilo na zaslon
    def buttons(self):
        #pygame.draw.rect(self.screen,black,self.button_easy)
        #pygame.draw.rect(self.screen,black,self.button_hard)
        self.text_easy = self.font.render("EASY",True,green)
        self.text_hard = self.font.render("HARD",True,red)
        self.text_choose = self.font.render("Choose AI difficulty",True,white)

        self.screen.blit(self.text_choose, (width/2 - self.text_choose.get_width()/2, 60))
        self.screen.blit(self.text_easy, (self.button_easy.x + 5, self.button_easy.y  + 15))
        self.screen.blit(self.text_hard, (self.button_hard.x + 5, self.button_hard.y + 15))
    


    def izberi_mode(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.button_easy.collidepoint(event.pos):
                    self.difficulty = "easy"
                    return False
                if self.button_hard.collidepoint(event.pos):
                    self.difficulty = "hard"
                    return False
        return True

    def run(self):
        running = True
        while running:
            self.set_background()
            self.buttons()
            pygame.display.update()
            running = self.izberi_mode()
        return self.difficulty