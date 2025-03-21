
import sys
import pygame
import numpy as np
from main import width, height, red, green, black, white,yellow

pygame.init()
blue = (0,0,255)
stolpci = 6  #stolpci
vrstice = 7 #vrstice
velikost_kvadrata = 100


class Code_1v1:
    def __init__(self):
        pygame.display.set_caption("Connect 4:  1v1")
        self.screen = pygame.display.set_mode((width,height))
        self.screen.fill(white)
        self.board = np.zeros((stolpci,vrstice))
        #self.board= [[0]* rows for i in range(collumn)]
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
        for vrstica in range(vrstice):
            for stolpec in range(1,stolpci +1):
                    pygame.draw.rect(self.screen,blue,(vrstica * velikost_kvadrata,stolpec * velikost_kvadrata,velikost_kvadrata,velikost_kvadrata))
                    pygame.draw.circle(self.screen,white,(int(vrstica *  velikost_kvadrata + velikost_kvadrata/2), int(stolpec * velikost_kvadrata  + velikost_kvadrata/2)), int(velikost_kvadrata/2 - 5))

    def winig_move(self,piece):
        #horizontalno
        for stolpec in range(stolpci):
             for vrstica in range(vrstice - 3):
                if self.board[stolpec][vrstica] == piece and self.board[stolpec][vrstica + 1] == piece and self.board[stolpec][vrstica + 2] == piece and self.board[stolpec][vrstica +3 ] == piece:
                    return True
        #vertikalno                           
        for stolpec in range(stolpci - 3):
            for vrstica in range(vrstice):
                if self.board[stolpec][vrstica] == piece and self.board[stolpec + 1][vrstica] == piece and self.board[stolpec + 2][vrstica] == piece and self.board[stolpec + 3][vrstica] == piece:
                    return True
        #poševno naprej
        for vrstica in range(vrstice - 3):
            for stolpec in range(stolpci - 3):
                if self.board[vrstica][stolpec] == piece and self.board[vrstica + 1][stolpec +1] == piece and self.board[vrstica + 2][stolpec + 2] == piece and self.board[vrstica + 3][stolpec + 3] == piece:
                    return True
        #poševno nazaj
        for vrstica in range(vrstice - 3):
            for stolpec in range(3,stolpci):
                if self.board[vrstica][stolpec] == piece and self.board[vrstica +1][stolpec -1] == piece and self.board[vrstica +2][stolpec -2] == piece and self.board[vrstica +3][stolpec - 3]:
                    return True
        return False
    
    def run_game(self):
        self.draw_board()
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            

if __name__ == "__main__":
    RUN = Code_1v1()
    RUN.draw_board()
    RUN.run_game()



                


