import sys
import pygame
import numpy as np
from menu import width, height, red, green, black, white,yellow

pygame.init()

pygame.mixer.init()
blue = (0,0,255)
stolpci = 7  #stolpci
vrstice = 6 #vrstice
velikost_kvadrata = 100


class Code_1v1:
    def __init__(self):
        pygame.display.set_caption("Connect 4:  1v1")
        self.screen = pygame.display.set_mode((width,height))
        self.screen.fill(white)
        self.board = np.zeros((vrstice,stolpci))
        #self.board= [[0]* stolpci for i in range(vrstice)]
        self.game_over = False
        self.turn = 0 # red = 1, yellow = 0
        self.reset_picture = pygame.image.load("github 4 in a row/slike/reset.png")
        self.reset_picture = pygame.transform.scale(self.reset_picture, (100, 100))
        
        self.load_sounds()
        self.play_background_music()
    
    def load_sounds(self):
        try:
            self.background_music = pygame.mixer.music.load("github 4 in a row/sounds/background_music.mp3")
            self.drop_sound = pygame.mixer.Sound("github 4 in a row/sounds/drop_sound.wav")
            self.win_sound = pygame.mixer.Sound("github 4 in a row/sounds/win_sound.wav")
        except Exception as e:
            print(f"Could not load sound files. Make sure they exist in the correct location. {e}")
            
    def play_background_music(self):
        try:
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.6) 
        except:
            print("Could not play background music")
            
    def drop_piece(self,row,col,piece):
        self.board[row][col] = piece
        try:
            self.drop_sound.play()
        except:
            pass
    
    def is_valid_location(self,stolpec):
        return self.board[vrstice -1][stolpec] == 0
        

    def naslednja_prosta_vrstica(self,stolpec):
        for i in range(vrstice):
            if self.board[i][stolpec] == 0:
                return i
        
    def draw_board(self):
        for stolpec in range(stolpci):
            for vrstica in range(1,vrstice +1):
                    pygame.draw.rect(self.screen,blue,(stolpec * velikost_kvadrata,vrstica * velikost_kvadrata,velikost_kvadrata,velikost_kvadrata))
                    pygame.draw.circle(self.screen,white,(int(stolpec *  velikost_kvadrata + velikost_kvadrata/2), int(vrstica * velikost_kvadrata  + velikost_kvadrata/2)), int(velikost_kvadrata/2 - 5))

    def wining_move(self,piece):
           
        # Horizontala
        for vrstica in range(vrstice):
            for stolpec in range(stolpci - 3):
                if self.board[vrstica][stolpec] == piece and self.board[vrstica][stolpec + 1] == piece and self.board[vrstica][stolpec + 2] == piece and self.board[vrstica][stolpec + 3] == piece:
                    return True
    
        # Vertikala
        for stolpec in range(stolpci):
            for vrstica in range(vrstice - 3):
                if self.board[vrstica][stolpec] == piece and self.board[vrstica + 1][stolpec] == piece and self.board[vrstica + 2][stolpec] == piece and self.board[vrstica + 3][stolpec] == piece:
                    return True
    
        # Diagonala 1
        for vrstica in range(vrstice - 3):
            for stolpec in range(stolpci - 3):
                if self.board[vrstica][stolpec] == piece and self.board[vrstica + 1][stolpec + 1] == piece and self.board[vrstica + 2][stolpec + 2] == piece and self.board[vrstica + 3][stolpec + 3] == piece:
                    return True
    
        # Diagonala 2
        for vrstica in range(3, vrstice):
            for stolpec in range(stolpci - 3):
                if self.board[vrstica][stolpec] == piece and self.board[vrstica - 1][stolpec + 1] == piece and self.board[vrstica - 2][stolpec + 2] == piece and self.board[vrstica - 3][stolpec + 3] == piece:
                    return True
    
        return False
    
    def restart_board(self):
        self.board = np.zeros((vrstice,stolpci))
        self.game_over = False
        self.turn = 0
        self.screen.fill(white)
        self.draw_board()
        pygame.display.update()
        self.play_background_music()

    def izenaceno(self):
        for i in self.board:
            for j in i:
                if j != 1 and j != 2:
                    return False
        return True


    def run_game(self):
        self.button_reset = pygame.Rect(600,0,100,100)
        self.draw_board()
        myfont = pygame.font.Font("github 4 in a row/fonts/arcade_font.ttf", 30)
        self.button_again = pygame.Rect(width//2-100, height//2, 200, 50)
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEMOTION:
                    posx = event.pos[0]
                    stolpec = min(posx // velikost_kvadrata, stolpci - 1)
                    pygame.draw.rect(self.screen,white,(0,0,width,velikost_kvadrata))
                    pygame.draw.circle(self.screen,red if self.turn == 0 else yellow,
                                      (stolpec * velikost_kvadrata + int(velikost_kvadrata/2), int(velikost_kvadrata/2)),
                                      int(velikost_kvadrata/2 - 5))
                    pygame.display.update()
                if  event.type == pygame.MOUSEBUTTONDOWN: 
                    
                    posx = event.pos[0]
                    stolpec = min(posx // velikost_kvadrata, stolpci - 1)
                    #print(stolpec) 
                    if 0 <= stolpec < stolpci and self.is_valid_location(stolpec):
                        vrstica = self.naslednja_prosta_vrstica(stolpec)
                        posx = event.pos[0]
                        self.drop_piece(vrstica,stolpec,1 if self.turn == 0 else 2)
                        pygame.draw.circle(self.screen,red if self.turn == 0 else yellow,(stolpec * velikost_kvadrata + int(velikost_kvadrata/2),(vrstice  - vrstica) * velikost_kvadrata + int(velikost_kvadrata/2)),int(velikost_kvadrata/2 - 5))  
                        pygame.display.update()
                        pygame.time.wait(300)
                        if self.wining_move(1 if self.turn == 0 else 2):
                            try:
                                self.win_sound.play()
                                pygame.mixer.music.stop()
                            except:
                                pass
                                
                            if self.turn == 0:
                                label = myfont.render("RED Player wins!!", 1, black)
                            else:
                                label = myfont.render("YELLOW Player wins!!", 1, black)
                            
                            pygame.draw.rect(self.screen,white,(0,0,width,velikost_kvadrata))
                            self.screen.blit(label, (40,10))
                            self.screen.blit(self.reset_picture,(self.button_reset))
                            pygame.display.update()
                            self.game_over = True
                            pygame.time.wait(1000)
                            waiting_for_input = True
                            while waiting_for_input:
                                for evt in pygame.event.get():
                                    if evt.type == pygame.QUIT:
                                        pygame.quit()
                                        sys.exit()
                                    if evt.type == pygame.MOUSEBUTTONDOWN:
                                        if self.button_reset.collidepoint(evt.pos):
                                            self.restart_board()
                                            waiting_for_input = False
                                            break
                                        else:
                                            pygame.quit()
                                            sys.exit()


                        if self.izenaceno():
                            label = myfont.render("DRAW!",1,black)
                            pygame.draw.rect(self.screen,white,(0,0,width,velikost_kvadrata))
                            self.screen.blit(self.reset_picture,(self.button_reset))
                            self.screen.blit(label, (40,10))
                            pygame.display.update()
                            self.game_over = True
                            pygame.time.wait(1000)
                            waiting_for_input = True
                            while waiting_for_input:
                                for evt in pygame.event.get():
                                    if evt.type == pygame.QUIT:
                                        pygame.quit()
                                        sys.exit()
                                    if evt.type == pygame.MOUSEBUTTONDOWN:
                                        if self.button_reset.collidepoint(evt.pos):
                                            self.restart_board()
                                            waiting_for_input = False
                                            break 
                                        else:
                                            pygame.quit()
                                            sys.exit()
                        else:
                            self.turn += 1
                            self.turn = self.turn % 2
                    
                    pygame.draw.circle(self.screen,red if self.turn == 0 else yellow,
                                      (stolpec * velikost_kvadrata + int(velikost_kvadrata/2), int(velikost_kvadrata/2)),
                                      int(velikost_kvadrata/2 - 5))
                        
                    pygame.display.update()
        
                    
            

"""if __name__ == "__main__":
    RUN = Code_1v1()
    RUN.run_game()"""






