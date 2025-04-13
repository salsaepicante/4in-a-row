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
            self.draw_sound = pygame.mixer.Sound("github 4 in a row/sounds/losing_sound.wav")
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


    def escape_menu(self):
        self.overlay = pygame.Surface((width, height))
        self.overlay.fill((0, 0, 0))  # Black overlay
        self.overlay.set_alpha(70)  # 0-255 (higher = darker)
        self.screen.blit(self.overlay, (0, 0))

        resume_button = pygame.Rect(width//2 - 200, height//2 - 50, 400, 60)
        menu_button = pygame.Rect(width//2 - 200, height//2 + 50, 400, 60)
        restart_button = pygame.Rect(width//2 - 200, height//2 + 150, 400, 60)


        font = pygame.font.Font("github 4 in a row/fonts/arcade_font.ttf", 30)
        resume_text = font.render("RESUME GAME", True, white)
        quit_text = font.render("QUIT TO MENU", True, white)
        restart_text = font.render("RESTART GAME", True, white)
        pygame.draw.rect(self.screen, black, restart_button, border_radius=10)
        pygame.draw.rect(self.screen, black, resume_button, border_radius=10)
        pygame.draw.rect(self.screen, black, menu_button, border_radius=10)

        self.screen.blit(restart_text,(restart_button.x  + (restart_button.width - restart_text.get_width())//2,
            restart_button.y + (restart_button.height - restart_text.get_height())//2))
        self.screen.blit(resume_text, (resume_button.x + (resume_button.width - resume_text.get_width())//2,
            resume_button.y + (resume_button.height - resume_text.get_height())//2))
        self.screen.blit(quit_text, (menu_button.x + (menu_button.width - quit_text.get_width())//2, 
            menu_button.y + (menu_button.height - quit_text.get_height())//2))
        
        pygame.display.update()
        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_button.collidepoint(event.pos):
                        waiting_for_input = False
                        self.restart_board()
                    if resume_button.collidepoint(event.pos):
                        waiting_for_input = False
                        self.screen.fill(white)
                        self.draw_board()
                        for i in range(vrstice):
                            for j in range(stolpci):
                                if self.board[i][j] == 1:
                                    pygame.draw.circle(self.screen, red, (j * velikost_kvadrata + int(velikost_kvadrata/2), (vrstice - i) * velikost_kvadrata + int(velikost_kvadrata/2)), int(velikost_kvadrata/2 - 5))
                                elif self.board[i][j] == 2:
                                    pygame.draw.circle(self.screen, yellow, (j * velikost_kvadrata + int(velikost_kvadrata/2), (vrstice - i) * velikost_kvadrata + int(velikost_kvadrata/2)), int(velikost_kvadrata/2 - 5))
                        pygame.display.update()
                    elif menu_button.collidepoint(event.pos):
                        return "menu" 
                    
    def menu_endgame(self):
        self.overlay = pygame.Surface((width, height))
        self.overlay.fill((0, 0, 0)) 
        self.overlay.set_alpha(150)  
        self.screen.blit(self.overlay, (0, 0))
        draw = False
        restart_game_button = pygame.Rect(width//2 - 200, height//2 - 50, 400, 60)
        menu_button = pygame.Rect(width//2 - 200, height//2 + 50, 400, 60)
        win_button = pygame.image.load("github 4 in a row/slike/win_image.jpg")
        win_button = pygame.transform.scale(win_button,(width,100))
        font = pygame.font.Font("github 4 in a row/fonts/arcade_font.ttf", 30)
        resume_text = font.render("RESTART GAME", True, white)
        quit_text = font.render("QUIT TO MENU", True, white)
        if self.wining_move(2):
            win_text = font.render("RED PLAYER WINS",True, red)
        elif self.wining_move(1):
            win_text = font.render("YELLOW PLAYER WINS", True, yellow)
        else:
            win_text = font.render("DRAW",True,black)
            draw = True
        pygame.draw.rect(self.screen, black, restart_game_button, border_radius=10)
        pygame.draw.rect(self.screen, black, menu_button, border_radius=10)
        #self.screen.blit(win_button, (0,0))
        if draw:
            self.screen.blit(win_text,(275,30))
        else:
            self.screen.blit(win_text,(100,30) )
        self.screen.blit(resume_text, (restart_game_button.x + (restart_game_button.width - resume_text.get_width())//2,
                                restart_game_button.y + (restart_game_button.height - resume_text.get_height())//2))
        self.screen.blit(quit_text, (menu_button.x + (menu_button.width - quit_text.get_width())//2, 
                            menu_button.y + (menu_button.height - quit_text.get_height())//2))
        
        pygame.display.update()
        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_game_button.collidepoint(event.pos):
                        waiting_for_input = False
                        self.restart_board()
                    elif menu_button.collidepoint(event.pos):
                        return "menu" 
                    


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
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    esc = self.escape_menu()
                    if esc == "menu":
                        return "menu"
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
                                
                            end = self.menu_endgame()
                            if end == "menu":
                                return "menu"



                        if self.izenaceno():
                            try:
                                self.draw_sound.play()
                                pygame.mixer.music.stop()
                            except:
                                pass

                            end = self.menu_endgame()
                            if end == "menu":
                                return "menu"
                        else:
                            self.turn += 1
                            self.turn = self.turn % 2
                    
                    pygame.draw.circle(self.screen,red if self.turn == 0 else yellow,
                                      (stolpec * velikost_kvadrata + int(velikost_kvadrata/2), int(velikost_kvadrata/2)),
                                      int(velikost_kvadrata/2 - 5))
                        
                    pygame.display.update()
        
                    
            

if __name__ == "__main__":
    RUN = Code_1v1()
    RUN.run_game()






