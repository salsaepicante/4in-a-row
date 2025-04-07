import pygame
import sys
from menu import GameMenu
from connect4_1v1 import Code_1v1
from connect4_AI import Code_Ai
from choose_AI_game_mode import AI_difficulty

main_menu = GameMenu()
menu_choice = main_menu.run()  

if menu_choice == "1v1":
    game = Code_1v1()
    game.run_game()
elif menu_choice == "Ai":
    difficulty_selector = AI_difficulty()
    difficulty = difficulty_selector.run()  
    if difficulty == "easy":
        game = Code_Ai(difficulty=2)
        game.run_game()
    elif difficulty == "hard":
        game = Code_Ai(difficulty=5)
        game.run_game()

pygame.quit()
print("Konec")  