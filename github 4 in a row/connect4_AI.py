import sys
import pygame
import numpy as np
from random import randint,random
import random

from menu import width, height, red, green, black, white,yellow

pygame.init()
pygame.mixer.init()
blue = (0,0,255)
stolpci = 7  #stolpci
vrstice = 6 #vrstice
velikost_kvadrata = 100

class AI_difficulty:
    def __init__(self):
        pygame.display.set_caption("Choose AI difficulty")
        self.screen = pygame.display.set_mode((width,height))
        self.font = pygame.font.Font(None,50)
        self.screen = pygame.display.set_mode((width,height))

        #ozadje
        self.background = pygame.image.load("github 4 in a row/slike/background.jpg")
        self.background = pygame.transform.scale(self.background, (width,height)) 
        #gumbi za izbor načina igre
        self.button_easy = pygame.Rect((width / 2)-(width*0.3)/2 ,(height / 2)-(height*0.1)/2,width*0.3,height*0.1)
        self.button_hard = pygame.Rect((width / 2)-(width*0.3)/2 ,(height / 2)-(height*0.5)/2,width*0.3,height*0.1)
        self.game_mode = None  # način igre dam na None
    
    #za ozadje
    def set_background(self):
        self.screen.blit(self.background,(0,0))


    #narišem gumbe in besedilo na zaslon
    def buttons(self):
        pygame.draw.rect(self.screen,black,self.button_easy)
        pygame.draw.rect(self.screen,black,self.button_hard)
        text_easy = self.font.render("EASY",True,white)
        text_hard = self.font.render("HARD",True,white)

        self.screen.blit(text_easy, (self.button_easy.x + 10, self.button_easy.y + 30))
        self.screen.blit(text_hard, (self.button_hard.x + 5, self.button_hard.y + 30))
    


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
            pygame.display.flip()
            running = self.izberi_mode()
        return self.difficulty


difficulty = AI_difficulty()
difficulty = difficulty.run()


#
#AI code
#class
#
class Code_Ai:
    def __init__(self,difficulty):
        pygame.display.set_caption("Connect 4:  AI")
        self.screen = pygame.display.set_mode((width,height))
        self.screen.fill(white)
        self.board = np.zeros((vrstice,stolpci))
        #self.board= [[0]* stolpci for i in range(vrstice)]
        self.game_over = False
        self.turn_AI = 2
        self.turn_ME = 1
        self.turn = randint(self.turn_ME,self.turn_AI)
        self.reset_picture = pygame.image.load("github 4 in a row/slike/reset.png")
        self.reset_picture = pygame.transform.scale(self.reset_picture, (100, 100))
        if difficulty == "easy":
            self.search_depth = 3
        else:
            self.search_depth = 5
        
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
    def drop_piece_for_AI(self,board,row,col,piece):
        board[row][col] = piece
        try:
            self.drop_sound.play()
        except:
            pass

    def is_valid_location(self,stolpec):
        return self.board[vrstice -1][stolpec] == 0
        

    def naslednja_prosta_vrstica(self,stolpec):
        if stolpec == None:
            stolpec = 3
        for i in range(vrstice):
            if self.board[i][stolpec] == 0:
                return i
        return -1
    def draw_board(self):
        #plošča na kateri se igra
        for stolpec in range(stolpci):
            for vrstica in range(1,vrstice +1):
                    pygame.draw.rect(self.screen,blue,(stolpec * velikost_kvadrata,vrstica * velikost_kvadrata,velikost_kvadrata,velikost_kvadrata))
                    pygame.draw.circle(self.screen,white,(int(stolpec *  velikost_kvadrata + velikost_kvadrata/2), int(vrstica * velikost_kvadrata  + velikost_kvadrata/2)), int(velikost_kvadrata/2 - 5))

    def wining_move(self,piece):
           
        # Horizontalno 
        for vrstica in range(vrstice):
            for stolpec in range(stolpci - 3):
                if self.board[vrstica][stolpec] == piece and self.board[vrstica][stolpec + 1] == piece and self.board[vrstica][stolpec + 2] == piece and self.board[vrstica][stolpec + 3] == piece:
                    return True
    
        # Vertikalno 
        for stolpec in range(stolpci):
            for vrstica in range(vrstice - 3):
                if self.board[vrstica][stolpec] == piece and self.board[vrstica + 1][stolpec] == piece and self.board[vrstica + 2][stolpec] == piece and self.board[vrstica + 3][stolpec] == piece:
                    return True
    
        # Diagonale pozitivna
        for vrstica in range(vrstice - 3):
            for stolpec in range(stolpci - 3):
                if self.board[vrstica][stolpec] == piece and self.board[vrstica + 1][stolpec + 1] == piece and self.board[vrstica + 2][stolpec + 2] == piece and self.board[vrstica + 3][stolpec + 3] == piece:
                    return True
    
        # Diagonale negativna
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
    
    def get_valid_locations(self):
        self.valid_locations = []
        for col in range(stolpci):
            if self.is_valid_location( col):
                self.valid_locations.append(col)
        return self.valid_locations



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
        self.score = 0
        self.center_stolpec = [int(i) for i in list(self.board[:,stolpci//2])]
        self.center_stevec = self.center_stolpec.count(piece)
        self.score += self.center_stevec * 1
        #horizontalno
        for vrstica in range(vrstice):
            vrstica_array = [int(i) for i in list(self.board[vrstica,:])]
            for stolpec in range(stolpci - 3):
                window = vrstica_array[stolpec:stolpec + 4]
                self.score += self.evaluate_window(window, piece)
        #vertikalno
        for stolpec in range(stolpci):
            stolpec_array = [int(i) for i in list(self.board[:,stolpec])]
            for vrstica in range(vrstice - 3):
                window = stolpec_array[vrstica:vrstica + 4]
                self.score += self.evaluate_window(window, piece)
        #diagonalno
        for vrstica in range(vrstice - 3):
            for stolpec in range(stolpci - 3):
                window = [self.board[vrstica + i][stolpec + i] for i in range(4)]
                self.score += self.evaluate_window(window, piece)

        for vrstica in range( vrstice - 3):
            for stolpec in range(stolpci - 3):
                window = [self.board[vrstica +3 - i][stolpec + i] for i in range(4)]
                self.score += self.evaluate_window(window, piece)
                
        return self.score
    
    def pick_best_move(self,piece):

        self.valid_locations = self.get_valid_locations()
        self.best_score = -10000
        self.best_col = random.choice(self.valid_locations)
        for col in self.valid_locations:
            row = self.naslednja_prosta_vrstica(col)
            temp_board = self.board.copy()
            self.drop_piece_for_AI(temp_board, row, col, piece)
            self.score = self.score_position(temp_board, piece)
            if self.score > self.best_score:
                self.best_score = self.score
                self.best_col = col

        return self.best_col
    """
    def minimax(self,depth, alpha, beta, maximizingPlayer):
        self.valid_locations = [c for c in range(stolpci) if self.is_valid_location(c)]
        is_terminal = self.wining_move(self.turn_ME) or self.wining_move(self.turn_AI) or len(self.valid_locations) == 0

        if depth == 0 or is_terminal:
            if is_terminal:
                if self.wining_move(2):
                    return (None, 1000000000)
                elif self.wining_move(1):
                    return (None, -1000000000)
                else:
                    return (None, 0)
            else:
                return (None, self.state_of_the_game(self.turn_AI) + self.state_of_the_game(self.turn_ME))
    
        if maximizingPlayer:
            self.value = -np.inf
            self.stolpec = self.valid_locations[0]
            for stolpec in self.valid_locations:
                vrstica = self.naslednja_prosta_vrstica(stolpec)
                if vrstica == -1:
                    continue
                board_copy = self.board.copy()
                board_copy[vrstica][stolpec] = self.turn_AI
                self.temp_board = self.board.copy()
                self.temp_board[vrstica][stolpec] = self.turn_AI
                self.new_score = self.minimax(depth - 1, alpha, beta, False)[1]
                self.board = self.temp_board.copy()
                if self.new_score > self.value:
                    self.value = self.new_score
                    self.stolpec = stolpec
                alpha = max(alpha, self.value)
                if alpha >= beta:
                    break
            return self.stolpec , self.value
        else:
            self.value = np.inf
            self.stolpec = self.valid_locations[0]
            for stolpec in self.valid_locations:
                vrstica = self.naslednja_prosta_vrstica(stolpec)
                self.temp_board = self.board.copy()
                self.temp_board[vrstica][stolpec] = self.turn_ME
                self.new_score = self.minimax(depth - 1, alpha, beta, True)[1]
                self.board = self.temp_board.copy()
                if self.new_score < self.value:
                    self.value = self.new_score
                    self.stolpec = stolpec
                beta = min(beta, self.value)
                if alpha >= beta:
                    break
            return self.stolpec, self.value"""
    def run_game(self):
        self.button_reset = pygame.Rect(600,0,100,100)
        self.draw_board()
        myfont = pygame.font.SysFont("monospace", 50)
        self.button_again = pygame.Rect(width//2-100, height//2, 200, 50)
        stolpec = 0
        while not self.game_over:
            for event in pygame.event.get():
               
                #print(self.board)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if self.turn == self.turn_ME:
                    if event.type == pygame.MOUSEMOTION:
                        posx = event.pos[0]
                        
                        stolpec = min(posx // velikost_kvadrata, stolpci - 1)
                        pygame.draw.rect(self.screen,white,(0,0,width,velikost_kvadrata))
                        pygame.draw.circle(self.screen,red,(stolpec * velikost_kvadrata + int(velikost_kvadrata/2), int(velikost_kvadrata/2)),
                                        int(velikost_kvadrata/2 - 5))
                        pygame.display.update()
                    if  event.type == pygame.MOUSEBUTTONDOWN: 
                            posx = event.pos[0]
                            stolpec = min(posx // velikost_kvadrata, stolpci - 1)
                            #print(stolpec) 
                            if 0 <= stolpec < stolpci and self.is_valid_location(stolpec):
                                vrstica = self.naslednja_prosta_vrstica(stolpec)
                                posx = event.pos[0]
                                self.drop_piece(vrstica,stolpec,1)
                                pygame.draw.circle(self.screen,red if self.turn == 0 else yellow,(stolpec * velikost_kvadrata + int(velikost_kvadrata/2),(vrstice  - vrstica) * velikost_kvadrata + int(velikost_kvadrata/2)),int(velikost_kvadrata/2 - 5))  
                                self.turn = self.turn_AI
                                if self.wining_move(1):
                                    # Play winning sound
                                    try:
                                        self.win_sound.play()
                                        pygame.mixer.music.stop()
                                    except:
                                        pass
                                        
                                    
                                    label = myfont.render("RED Player wins!!", 1, black)
                                    
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
                pygame.display.update()
            if self.turn == self.turn_AI:
                pygame.time.wait(500)
                stolpec = self.pick_best_move(2)
                
                print(f"AI chose column {stolpec} with score ")
                print(f"Evaluated {len(self.valid_locations)} valid columns")
                    #print(stolpec) 
                if self.is_valid_location(stolpec):
                    if stolpec == None:
                        stolpec = 3
                    vrstica = self.naslednja_prosta_vrstica(stolpec)    

                    self.drop_piece(vrstica,stolpec,2)
                    pygame.draw.circle(self.screen,red if self.turn == 0 else yellow,(stolpec * velikost_kvadrata + int(velikost_kvadrata/2),(vrstice  - vrstica) * velikost_kvadrata + int(velikost_kvadrata/2)),int(velikost_kvadrata/2 - 5))
                    self.turn = self.turn_ME
                    
                    if self.wining_move(2):
                                    try:
                                        self.win_sound.play()
                                        pygame.mixer.music.stop()
                                    except:
                                        pass
                                    
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
                        
                pygame.display.update()
    
                    
            

if __name__ == "__main__":
    difficulty = AI_difficulty()
    difficulty = difficulty.run()
    RUN = Code_Ai(difficulty)
    RUN.run_game()





