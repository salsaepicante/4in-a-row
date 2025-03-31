import sys
import pygame
import numpy as np
from main import width, height, red, green, black, white,yellow

pygame.init()
# Initialize the mixer for playing sounds and music
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
        
        # Load sounds and music
        self.load_sounds()
        # Start playing background music
        self.play_background_music()
    
    def load_sounds(self):
        try:
            # Load background music - replace 'background_music.mp3' with your music file
            self.background_music = pygame.mixer.music.load('background_music.mp3')
            # Load sound effects - replace these with your sound files
            self.drop_sound = pygame.mixer.Sound('drop_sound.wav')
            self.win_sound = pygame.mixer.Sound('win_sound.wav')
        except:
            print("Could not load sound files. Make sure they exist in the correct location.")
            
    def play_background_music(self):
        try:
            pygame.mixer.music.play(-1)  # -1 means loop indefinitely
            pygame.mixer.music.set_volume(0.6) 
        except:
            print("Could not play background music")
            
    def drop_piece(self,row,col,piece):
        self.board[row][col] = piece
        # Play drop sound when a piece is placed
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
        myfont = pygame.font.SysFont("monospace", 50)
        while not self.game_over:
            for event in pygame.event.get():
                #print(self.board)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEMOTION:
                    posx = event.pos[0]
                    # Calculate which column the mouse is over
                    stolpec = min(posx // velikost_kvadrata, stolpci - 1)
                    pygame.draw.rect(self.screen,white,(0,0,width,velikost_kvadrata))
                    # Draw at the center of the column instead of exact mouse position
                    pygame.draw.circle(self.screen,red if self.turn == 0 else yellow,
                                      (stolpec * velikost_kvadrata + int(velikost_kvadrata/2), int(velikost_kvadrata/2)),
                                      int(velikost_kvadrata/2 - 5))
                    pygame.display.update()
                if  event.type == pygame.MOUSEBUTTONDOWN:   
                    posx = event.pos[0]
                    stolpec = min(posx // velikost_kvadrata, stolpci - 1)
                    print(stolpec) 
                    if 0 <= stolpec < stolpci and self.is_valid_location(stolpec):
                        vrstica = self.naslednja_prosta_vrstica(stolpec)
                        posx = event.pos[0]
                        self.drop_piece(vrstica,stolpec,1 if self.turn == 0 else 2)
                        pygame.draw.circle(self.screen,red if self.turn == 0 else yellow,(stolpec * velikost_kvadrata + int(velikost_kvadrata/2),(vrstice  - vrstica) * velikost_kvadrata + int(velikost_kvadrata/2)),int(velikost_kvadrata/2 - 5))  
                       
                        if self.winig_move(1 if self.turn == 0 else 2):
                            # Play winning sound
                            try:
                                self.win_sound.play()
                                # Stop background music when someone wins
                                pygame.mixer.music.stop()
                            except:
                                pass
                                
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
                    
            pygame.display.update()

if __name__ == "__main__":
    RUN = Code_1v1()
    RUN.run_game()






