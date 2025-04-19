import sys
import pygame
import numpy as np
from random import randint,random
import random
from menu import width, height, red, green, black, white,yellow,dark_blue

pygame.init()
pygame.mixer.init()
blue = (0,0,255)

#pomagal z tutorialom, le da sem jaz delal z objekti

stolpci = 7  #stolpci
vrstice = 6 #vrstice
velikost_kvadrata = 100
light_grey = (220,235,250)
difficulty = 4

class Code_Ai:
    def __init__(self,difficulty):
        if difficulty == 2:
            pygame.display.set_caption("Connect 4:  AI easy")
        elif difficulty == 5:
            pygame.display.set_caption("Connect 4:  AI hard")
        self.screen = pygame.display.set_mode((width,height))
        self.screen.fill(light_grey)
        self.board = np.zeros((vrstice,stolpci))
        #self.board= [[0]* stolpci for i in range(vrstice)]
        self.game_over = False
        self.turn_AI = 2
        self.turn_ME = 1
        self.turn = randint(self.turn_ME,self.turn_AI)
        self.reset_picture = pygame.image.load("github 4 in a row/slike/reset.png")
        self.reset_picture = pygame.transform.scale(self.reset_picture, (100, 100))
        self.search_depth = difficulty

        self.ai_stolpec = None
        self.ai_vrstica = None
        self.turns = False
        
        self.load_sounds()
        self.play_background_music()
    
    def load_sounds(self):
        try:
            self.background_music = pygame.mixer.music.load("github 4 in a row/sounds/background_music.mp3")
            self.drop_sound = pygame.mixer.Sound("github 4 in a row/sounds/drop_sound.wav")
            self.win_sound = pygame.mixer.Sound("github 4 in a row/sounds/win_sound.wav")
            self.lose_sound = pygame.mixer.Sound("github 4 in a row/sounds/losing_sound.wav")
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
    def drop_piece_for_AI(self,board,row,col,piece):
        board[row][col] = piece
        
        

    def is_valid_location(self,board, stolpec):
        return board[vrstice -1][stolpec] == 0
        

    def naslednja_prosta_vrstica(self,board, stolpec):
        for i in range(vrstice):
            if board[i][stolpec] == 0:
                return i
        return -1
    def draw_board(self):
        #plošča na kateri se igra
        for stolpec in range(stolpci):
            for vrstica in range(1,vrstice +1):
                    pygame.draw.rect(self.screen,blue,(stolpec * velikost_kvadrata,vrstica * velikost_kvadrata,velikost_kvadrata,velikost_kvadrata))
                    pygame.draw.circle(self.screen,light_grey,(int(stolpec *  velikost_kvadrata + velikost_kvadrata/2), int(vrstica * velikost_kvadrata  + velikost_kvadrata/2)), int(velikost_kvadrata/2 - 5))
                    pygame.draw.circle(self.screen,dark_blue,(int(stolpec *  velikost_kvadrata + velikost_kvadrata/2), int(vrstica * velikost_kvadrata  + velikost_kvadrata/2)), int(velikost_kvadrata/2 - 5) + 3, 5)
        pygame.time.wait(500)
    def wining_move(self,board,piece):
           
        # Horizontalno 
        for vrstica in range(vrstice):
            for stolpec in range(stolpci - 3):
                if board[vrstica][stolpec] == piece and board[vrstica][stolpec + 1] == piece and board[vrstica][stolpec + 2] == piece and board[vrstica][stolpec + 3] == piece:
                    return True
    
        # Vertikalno 
        for stolpec in range(stolpci):
            for vrstica in range(vrstice - 3):
                if board[vrstica][stolpec] == piece and board[vrstica + 1][stolpec] == piece and board[vrstica + 2][stolpec] == piece and board[vrstica + 3][stolpec] == piece:
                    return True
    
        # Diagonale pozitivna
        for vrstica in range(vrstice - 3):
            for stolpec in range(stolpci - 3):
                if board[vrstica][stolpec] == piece and board[vrstica + 1][stolpec + 1] == piece and board[vrstica + 2][stolpec + 2] == piece and board[vrstica + 3][stolpec + 3] == piece:
                    return True
    
        # Diagonale negativna
        for vrstica in range(3, vrstice):
            for stolpec in range(stolpci - 3):
                if board[vrstica][stolpec] == piece and board[vrstica - 1][stolpec + 1] == piece and board[vrstica - 2][stolpec + 2] == piece and board[vrstica - 3][stolpec + 3] == piece:
                    return True
    
        return False
    
    def restart_board(self):
        self.board = np.zeros((vrstice,stolpci))
        self.game_over = False
        self.turn = randint(self.turn_ME,self.turn_AI)
        self.screen.fill(white)
        self.draw_board()
        self.ai_stolpec = None
        self.ai_vrstica = None
        self.turns = False
        pygame.display.update()
        self.play_background_music()

    def izenaceno(self):
        for i in self.board:
            for j in i:
                if j != 1 and j != 2:
                    return False
        return True
    


    #za AI
    #
    #
    #
    #


    def get_valid_locations(self,board):
        valid_locations = []
        for col in range(stolpci):
            if self.is_valid_location( board, col):
                valid_locations.append(col)
        return valid_locations



    def evaluate_window(self,window,piece):
        score = 0
        self.opponent_piece = self.turn_ME
        if piece == self.turn_ME:
            self.opponent_piece = self.turn_AI
        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(0) == 1:
            score += 5
        elif window.count(piece) == 2 and window.count(0) == 2:
            score += 2
        
        if window.count(self.opponent_piece) == 3 and window.count(0) == 1:
            score -= 4
        return score
    
    def score_position(self,board,piece):
        score = 0
        self.center_stolpec = [int(i) for i in list(board[:,stolpci//2])]
        self.center_stevec = self.center_stolpec.count(piece)
        score += self.center_stevec * 3
        #horizontalno
        for vrstica in range(vrstice):
            vrstica_array = [int(i) for i in list(board[vrstica,:])]
            for stolpec in range(stolpci - 3):
                window = vrstica_array[stolpec:stolpec + 4]
                score += self.evaluate_window(window, piece)
        #vertikalno
        for stolpec in range(stolpci):
            stolpec_array = [int(i) for i in list(board[:,stolpec])]
            for vrstica in range(vrstice - 3):
                window = stolpec_array[vrstica:vrstica + 4]
                score += self.evaluate_window(window, piece)
        #diagonalno
        for vrstica in range(vrstice - 3):
            for stolpec in range(stolpci - 3):
                window = [board[vrstica + i][stolpec + i] for i in range(4)]
                score += self.evaluate_window(window, piece)

        for vrstica in range( vrstice - 3):
            for stolpec in range(stolpci - 3):
                window = [board[vrstica +3 - i][stolpec + i] for i in range(4)]
                score += self.evaluate_window(window, piece)
                
        return score
    #not used
    def pick_best_move(self,piece): #POMAGAL Z TUTORIALOM LE DA SEM SPREMENIL NEKAJ STVARI SAJ  DELAM Z OBJEKTNIM PROGRAMIRANJEM

        self.valid_locations = self.get_valid_locations(self.board)
        self.best_score = -10000
        self.best_col = random.choice(self.valid_locations)
        for col in self.valid_locations:
            row = self.naslednja_prosta_vrstica(self.board,col)
            temp_board = self.board.copy()
            self.drop_piece_for_AI(temp_board, row, col, piece)
            self.score = self.score_position(temp_board, piece)
            if self.score > self.best_score:
                self.best_score = self.score
                self.best_col = col

        return self.best_col
    
    def is_terminal_node(self, board):
        return self.wining_move(board, self.turn_ME) or self.wining_move(board, self.turn_AI) or len(self.get_valid_locations(board)) == 0
    
    def minimax(self,board, depth, alpha, beta, maximizingPlayer): #POMAGAL Z TUTORIALOM LE DA SEM SPREMENIL NEKAJ STVARI SAJ  DELAM Z OBJEKTNIM PROGRAMIRANJEM
        valid_locations = self.get_valid_locations(board)
        is_terminal = self.is_terminal_node(board)
        if depth == 0 or is_terminal:
            if is_terminal:
                if self.wining_move(board, self.turn_AI):
                    return (None, 100000000000000)
                elif self.wining_move(board, self.turn_ME):
                    return (None, -10000000000000)
                else: # Game is over, no more valid moves
                    return (None, 0)
            else: # Depth is zero
                return (None, self.score_position(board, self.turn_AI))
        if maximizingPlayer:
            value = -np.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = self.naslednja_prosta_vrstica(board, col)
                b_copy = board.copy()
                self.drop_piece_for_AI(b_copy, row, col, self.turn_AI)
                new_score = self.minimax(b_copy, depth-1, alpha, beta, False)[1]
                if new_score > value:
                    value = new_score
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return column, value

        else: # Minimizing player
            value = np.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = self.naslednja_prosta_vrstica(board, col)
                b_copy = board.copy()
                self.drop_piece_for_AI(b_copy, row, col, self.turn_ME)
                new_score = self.minimax(b_copy, depth-1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return column, value


    def redraw_board(self):
        self.draw_board()
        for i in range(vrstice):
            for j in range(stolpci):
                if self.board[i][j] == 1:
                    pygame.draw.circle(self.screen, red, (j * velikost_kvadrata + int(velikost_kvadrata/2), (vrstice - i) * velikost_kvadrata + int(velikost_kvadrata/2)), int(velikost_kvadrata/2 - 5))
                elif self.board[i][j] == 2:
                    pygame.draw.circle(self.screen, yellow, (j * velikost_kvadrata + int(velikost_kvadrata/2), (vrstice - i) * velikost_kvadrata + int(velikost_kvadrata/2)), int(velikost_kvadrata/2 - 5))
        pygame.display.update()
    
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
        self.screen.blit(restart_text, (restart_button.x + (restart_button.width - restart_text.get_width())//2,
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
                        self.redraw_board()
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
        if self.wining_move(self.board,self.turn_ME):
            win_text = font.render("YOU WON",True, red)
        elif self.wining_move(self.board,self.turn_AI):
            win_text = font.render("YOU LOST", True, yellow)
        else:
            win_text = font.render("DRAW",True,black)
            draw = True
        pygame.draw.rect(self.screen, black, restart_game_button, border_radius=10)
        pygame.draw.rect(self.screen, black, menu_button, border_radius=10)
        #self.screen.blit(win_button, (0,0))
        if draw:
            self.screen.blit(win_text,(275,30))
        else:
            self.screen.blit(win_text,(200,30) )
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
        myfont = pygame.font.Font("github 4 in a row/fonts/arcade_font.ttf", 40)
        self.button_again = pygame.Rect(width//2-100, height//2, 200, 50)
        stolpec = 0

        while not self.game_over:
            for event in pygame.event.get():
               
                #print(self.board)
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
                    pygame.draw.rect(self.screen,light_grey,(0,0,width,velikost_kvadrata))
                    pygame.draw.circle(self.screen,red,(stolpec * velikost_kvadrata + int(velikost_kvadrata/2), int(velikost_kvadrata/2)),
                                    int(velikost_kvadrata/2 - 5))
                    pygame.display.update()
                if self.turn == self.turn_ME:
                    if  event.type == pygame.MOUSEBUTTONDOWN: 
                            posx = event.pos[0]
                            stolpec = min(posx // velikost_kvadrata, stolpci - 1)
                            #print(stolpec) 
                            if 0 <= stolpec < stolpci and self.is_valid_location(self.board,stolpec):
                                vrstica = self.naslednja_prosta_vrstica(self.board,stolpec)
                                posx = event.pos[0]
                                self.drop_piece(vrstica,stolpec,1)
                                pygame.draw.circle(self.screen,red,(stolpec * velikost_kvadrata + int(velikost_kvadrata/2),(vrstice  - vrstica) * velikost_kvadrata + int(velikost_kvadrata/2)),int(velikost_kvadrata/2 - 5))  
                                self.turn = self.turn_AI
                                

                                if self.wining_move(self.board,self.turn_ME):
                                    # Play winning sound
                                    try:
                                        self.win_sound.play()
                                        pygame.mixer.music.stop()
                                    except:
                                        pass
                                    end = self.menu_endgame()
                                    if end == "menu":
                                        return "menu"   
                                if self.izenaceno():	
                                    end = self.menu_endgame()
                                    if end == "menu":
                                        return "menu"
                pygame.display.update()
            if self.turn == self.turn_AI:
                pygame.time.wait(500)
                if self.turns and self.ai_stolpec != None and self.ai_vrstica != None:
                    try:
                        pygame.draw.circle(self.screen,yellow,(self.ai_stolpec * velikost_kvadrata + int(velikost_kvadrata/2),(vrstice  - self.ai_vrstica) * velikost_kvadrata + int(velikost_kvadrata/2)),int(velikost_kvadrata/2 - 5),)
                    except:
                        pass

                if self.search_depth == 5:
                    stolpec,tocke = self.minimax(self.board,self.search_depth, -np.inf, np.inf, True)
                    print(f"AI chose column {stolpec} with score {tocke}")
                elif self.search_depth == 2:
                    stolpec = self.pick_best_move(self.turn_AI)

                    #print(stolpec) 

                if self.is_valid_location(self.board,stolpec):
                    vrstica = self.naslednja_prosta_vrstica(self.board, stolpec)    
                    self.drop_piece(vrstica,stolpec,self.turn_AI)
                    self.ai_vrstica = vrstica
                    self.ai_stolpec = stolpec
                    pygame.draw.circle(self.screen,yellow,(stolpec * velikost_kvadrata + int(velikost_kvadrata/2),(vrstice  - vrstica) * velikost_kvadrata + int(velikost_kvadrata/2)),int(velikost_kvadrata/2 - 5),)
                    pygame.draw.circle(self.screen,black,(stolpec * velikost_kvadrata + int(velikost_kvadrata/2),(vrstice  - vrstica) * velikost_kvadrata + int(velikost_kvadrata/2)),int(velikost_kvadrata/2 - 5),5)
                    self.turns = True
                    self.turn = self.turn_ME
                    
                    if self.wining_move(self.board,self.turn_AI):
                        
                        self.lose_sound.play()
                        pygame.mixer.music.stop()
                        
                        end = self.menu_endgame()
                        if end == "menu":
                            return "menu"
                        
                    if self.izenaceno():
                        end = self.menu_endgame()
                        if end == "menu":
                            return "menu"
                    
                    
                        
                                        
                        
                pygame.display.update()
    
                               
"""
if __name__ == "__main__":
    RUN = Code_Ai(difficulty)
    RUN.run_game()"""

