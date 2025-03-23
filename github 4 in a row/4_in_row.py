
import sys
import pygame
import numpy as np
from main import width, height, red, green, black, white,yellow

pygame.init()
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
    def drop_piece(self,row,col,piece):
        self.board[row][col] = piece
    
    def is_valid_location(self,stolpec):
        return self.board[vrstice -1][stolpec] == 0
        

    def naslednja_prosta_vrstica(self,stolpec):
        for i in range(vrstice):
            if self.board[i][stolpec] == 0:
                return i
        
    def draw_board(self):
        #plošča na kateri se igra
        for stolpec in range(stolpci):
            for vrstica in range(1,vrstice +1):
                    pygame.draw.rect(self.screen,blue,(stolpec * velikost_kvadrata,vrstica * velikost_kvadrata,velikost_kvadrata,velikost_kvadrata))
                    pygame.draw.circle(self.screen,white,(int(stolpec *  velikost_kvadrata + velikost_kvadrata/2), int(vrstica * velikost_kvadrata  + velikost_kvadrata/2)), int(velikost_kvadrata/2 - 5))

    def winig_move(self,piece):
           
        # Horizontal check
        for vrstica in range(vrstice):
            for stolpec in range(stolpci - 3):
                if self.board[vrstica][stolpec] == piece and self.board[vrstica][stolpec + 1] == piece and self.board[vrstica][stolpec + 2] == piece and self.board[vrstica][stolpec + 3] == piece:
                    return True
    
        # Vertical check
        for stolpec in range(stolpci):
            for vrstica in range(vrstice - 3):
                if self.board[vrstica][stolpec] == piece and self.board[vrstica + 1][stolpec] == piece and self.board[vrstica + 2][stolpec] == piece and self.board[vrstica + 3][stolpec] == piece:
                    return True
    
        # Diagonal (positive slope)
        for vrstica in range(vrstice - 3):
            for stolpec in range(stolpci - 3):
                if self.board[vrstica][stolpec] == piece and self.board[vrstica + 1][stolpec + 1] == piece and self.board[vrstica + 2][stolpec + 2] == piece and self.board[vrstica + 3][stolpec + 3] == piece:
                    return True
    
        # Diagonal (negative slope)
        for vrstica in range(3, vrstice):
            for stolpec in range(stolpci - 3):
                if self.board[vrstica][stolpec] == piece and self.board[vrstica - 1][stolpec + 1] == piece and self.board[vrstica - 2][stolpec + 2] == piece and self.board[vrstica - 3][stolpec + 3] == piece:
                    return True
    
        return False
    
    def run_game(self):
        self.draw_board()
        myfont = pygame.font.SysFont("monospace", 75)
        while not self.game_over:
            for event in pygame.event.get():
                print(self.board)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEMOTION:
                    posx = event.pos[0]
                    pygame.draw.rect(self.screen,white,(0,0,width,velikost_kvadrata))
                    pygame.draw.circle(self.screen,red if self.turn == 0 else yellow,(event.pos[0],int(velikost_kvadrata/2)),int(velikost_kvadrata/2 - 5))
                    pygame.display.update()
                if  event.type == pygame.MOUSEBUTTONDOWN:
                    posx = event.pos[0]
                    stolpec = min(posx // velikost_kvadrata, stolpci - 1) 
                    if 0 <= stolpec < stolpci and self.is_valid_location(stolpec):
                        vrstica = self.naslednja_prosta_vrstica(stolpec)
                        posx = event.pos[0]
                        self.drop_piece(vrstica,stolpec,1 if self.turn == 0 else 2)
                        #pygame.draw.circle(self.screen,red if self.turn == 0 else yellow,(stolpec * velikost_kvadrata + int(velikost_kvadrata/2),(ne dela) * velikost_kvadrata + int(velikost_kvadrata/2)),int(velikost_kvadrata/2 - 5))
                        pygame.draw.circle(self.screen,red if self.turn == 0 else yellow,(stolpec * velikost_kvadrata + int(velikost_kvadrata/2),(vrstice  - vrstica) * velikost_kvadrata + int(velikost_kvadrata/2)),int(velikost_kvadrata/2 - 5))  
                       
                        if self.winig_move(1 if self.turn == 0 else 2):
                            if self.turn == 0:
                                label = myfont.render("Player 1 wins!!", 1, red)
                            else:
                                label = myfont.render("Player 2 wins!!", 1, yellow)
                            

                            pygame.draw.rect(self.screen,white,(0,0,width,velikost_kvadrata))
                            self.screen.blit(label, (40,10))
                            pygame.display.update()
                            pygame.time.wait(10000)
                            self.game_over = True
                    self.turn += 1
                    self.turn = self.turn % 2
                    #self.draw_board()

            pygame.display.update()

if __name__ == "__main__":
    RUN = Code_1v1()
    
    RUN.run_game()



                


