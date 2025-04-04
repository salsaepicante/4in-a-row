import pygame
import sys
from menu import GameMenu
from connect4_1v1 import Code_1v1
from connect4_AI import Code_Ai, AI_difficulty
#import connect4_1v1
#import connect4_AI

main_menu = GameMenu()

if main_menu.run() == "1v1":
    game = Code_1v1()
    game.run_game()
elif main_menu.run() == "Ai":
    dificulty = AI_difficulty()
    dificulty.run()
    if dificulty == "easy":
        game = Code_Ai(difficulty="easy")
    elif dificulty == "hard":
        game = Code_Ai(difficulty="hard")

    game.run_game()

pygame.quit()