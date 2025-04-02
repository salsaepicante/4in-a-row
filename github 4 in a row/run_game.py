import pygame
import sys
from menu import GameMenu
#from connect4_1v1 import Code1v1
#from connect4_AI import CodeAi
import connect4_1v1
import connect4_AI

main_menu = GameMenu()
if main_menu.run() == "1v1":
    game = Code1v1()
    game.run()
elif main_menu.run() == "Ai":
    game = CodeAi()
    game.run()

pygame.quit()