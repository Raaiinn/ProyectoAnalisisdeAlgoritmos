import sys
import time
from controller.Game import Game
from view import PlayerFactory, Utils
from view.CombatView import CombatView
import pygame
from assets.button import Button

pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/Background.png")

CR = pygame.image.load("assets/Character.png").convert_alpha()
Box = pygame.image.load("assets/BattleBox.png").convert_alpha()

def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)
count=0

class Main:

    def __init__(self):
        self.player = PlayerFactory.createPlayer()
        self.game = Game(self.player)

    def start(self):
        self.initCombatView()
        self.initWinOrLoseView()
        self.game.start()

    def initCombatView(self):
        self.game.nextMonsterNameSubject.subscribe(
            lambda monster: self.clearScreenAndNextMonster(monster)
        )


    def initWinOrLoseView(self):
        self.game.gameResult.subscribe(
            lambda result: self.winView() if result else self.loseView()
        )

    def winView(self) -> None:
        print("You win!")
        while True:
            SCREEN.blit(BG, (0, 0))

            MENU_TEXT = get_font(50).render("You win!", True, "#b68f40")
            MENU_RECT = MENU_TEXT.get_rect(center=(690, 100))

            SCREEN.blit(MENU_TEXT, MENU_RECT)
            pygame.display.update()
            time.sleep(5)
            pygame.quit()
            sys.exit()

        exit()

    def loseView(self) -> None:
        print("You lose...")
        while True:
            SCREEN.blit(BG, (0, 0))

            MENU_TEXT = get_font(50).render("You lose...", True, "#b68f40")
            MENU_RECT = MENU_TEXT.get_rect(center=(690, 100))

            SCREEN.blit(MENU_TEXT, MENU_RECT)
            pygame.display.update()
            time.sleep(5)
            pygame.quit()
            sys.exit()
            pygame.display.update()
        exit()

    def clearScreenAndNextMonster(self, monsterName: str) -> None:
        Utils.clear()

        CombatView(self.game, self.player, monsterName).fight()



if __name__ == '__main__':
    Utils.clear()
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(50).render("Welcome to Dungeon game!", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(690, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 350),
                             text_input="PLAY", font=get_font(40), base_color="#d7fcd4", hovering_color="Black")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 500),
                             text_input="QUIT", font=get_font(40), base_color="#d7fcd4", hovering_color="Black")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    Main().start()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()
