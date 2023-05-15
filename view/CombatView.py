import sys
import typing
from typing import List
import time
from enums.Action import Action
from view import Utils

import pygame
from assets.button import Button

pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/BattleBG.png")
CR = pygame.image.load("assets/Character.png").convert_alpha()
CRD = pygame.image.load("assets/CharacterDamage.png").convert_alpha()
GB = pygame.image.load("assets/Goblin.png").convert_alpha()

Box = pygame.image.load("assets/BattleBox.png").convert_alpha()

Grey = pygame.image.load("assets/BattleBoxGrey.png").convert_alpha()


def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)


if typing.TYPE_CHECKING:
    from logic.fighter.Player import Player
    from controller.Game import Game


class CombatView:

    def __init__(self, game: 'Game', player: 'Player', monsterName: str):
        self.player = player
        self.monsterName = monsterName
        self.game = game

    def fight(self) -> None:
        SCREEN.blit(BG, (0, 0))
        SCREEN.blit(CR, (0, 0))
        SCREEN.blit(Box, (0, 0))

        MENU_TEXT = get_font(20).render("New enemy about to appear", True, "#000000")
        MENU_RECT = MENU_TEXT.get_rect(center=(500, 600))

        SCREEN.blit(MENU_TEXT, MENU_RECT)
        pygame.display.update()
        time.sleep(2)

        SCREEN.blit(BG, (0, 0))
        SCREEN.blit(CR, (0, 0))
        SCREEN.blit(GB, (0, 0))
        SCREEN.blit(Box, (0, 0))

        MENU_TEXT = get_font(20).render(self.monsterName.__str__() + " has appeared!\n", True, "#000000")
        MENU_RECT = MENU_TEXT.get_rect(center=(500, 600))

        SCREEN.blit(MENU_TEXT, MENU_RECT)
        pygame.display.update()
        time.sleep(2)

        while not self.game.currentMonsterIsDead():

            SCREEN.blit(BG, (0, 0))
            SCREEN.blit(CR, (0, 0))
            SCREEN.blit(GB, (0, 0))
            SCREEN.blit(Box, (0, 0))

            MENU_TEXT = get_font(20).render('{} is attacking!'.format(self.monsterName), True, "#000000")
            MENU_RECT = MENU_TEXT.get_rect(center=(500, 600))

            SCREEN.blit(MENU_TEXT, MENU_RECT)
            pygame.display.update()
            time.sleep(2)

            State = self.game.currentMonsterAttackPlayer()
            if State.__contains__('dodged the attack!'):

                SCREEN.blit(BG, (0, 0))
                SCREEN.blit(CR, (0, 0))
                SCREEN.blit(GB, (0, 0))
                SCREEN.blit(Box, (0, 0))

                MENU_TEXT = get_font(20).render(State, True, "#000000")
                MENU_RECT = MENU_TEXT.get_rect(center=(500, 600))

                SCREEN.blit(MENU_TEXT, MENU_RECT)
                pygame.display.update()
                time.sleep(2)

            else:
                SCREEN.blit(BG, (0, 0))
                SCREEN.blit(CRD, (0, 0))
                SCREEN.blit(GB, (0, 0))
                SCREEN.blit(Box, (0, 0))

                MENU_TEXT = get_font(20).render(State, True, "#000000")
                MENU_RECT = MENU_TEXT.get_rect(center=(500, 600))

                SCREEN.blit(MENU_TEXT, MENU_RECT)
                pygame.display.update()
                time.sleep(2)
            self.playerTurn()
        SCREEN.blit(BG, (0, 0))
        SCREEN.blit(CR, (0, 0))
        SCREEN.blit(Box, (0, 0))

        MENU_TEXT = get_font(20).render("Monster killed", True, "#000000")
        MENU_RECT = MENU_TEXT.get_rect(center=(500, 600))

        SCREEN.blit(MENU_TEXT, MENU_RECT)
        pygame.display.update()
        time.sleep(2)


    def playerTurn(self) -> None:

        SCREEN.blit(BG, (0, 0))
        SCREEN.blit(CR, (0, 0))
        SCREEN.blit(GB, (0, 0))
        SCREEN.blit(Box, (0, 0))

        MENU_TEXT = get_font(20).render(self.player.__str__(), True, "#000000")
        MENU_RECT = MENU_TEXT.get_rect(center=(500, 600))

        SCREEN.blit(MENU_TEXT, MENU_RECT)
        pygame.display.update()
        time.sleep(2)
        self.displayMenu()
        return

    def displayMenu(self) -> None:
        while True:
            SCREEN.blit(BG, (0, 0))
            SCREEN.blit(CR, (0, 0))
            SCREEN.blit(GB, (0, 0))
            SCREEN.blit(Box, (0, 0))
            SCREEN.blit(pygame.image.load("assets/BattleBoxGrey.png").convert_alpha(), (0, 0))
            MENU_MOUSE_POS = pygame.mouse.get_pos()

            PLAY_BUTTON = Button(image=pygame.image.load("assets/Attack Button.png"), pos=(272, 597),
                                 text_input="Attack", font=get_font(40), base_color="#d7fcd4", hovering_color="Black")
            HEAL_BUTTON = Button(image=pygame.image.load("assets/Heal Button.png"), pos=(647, 597),
                                 text_input="Heal", font=get_font(40), base_color="#d7fcd4", hovering_color="Black")
            QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Button.png"), pos=(1019, 597),
                                 text_input="Escape", font=get_font(40), base_color="#d7fcd4", hovering_color="Black")

            for button in [PLAY_BUTTON, HEAL_BUTTON, QUIT_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(SCREEN)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        State2 = self.game.playerAttackCurrentMonster()
                        if State2.__contains__('received damage'):
                            SCREEN.blit(BG, (0, 0))
                            SCREEN.blit(CR, (0, 0))
                            SCREEN.blit(pygame.image.load("assets/GoblinDamage.png").convert_alpha(), (0, 0))
                            SCREEN.blit(Box, (0, 0))
                            MENU_MOUSE_POS = pygame.mouse.get_pos()

                            MENU_TEXT = get_font(20).render(State2, True, "#000000")
                            MENU_RECT = MENU_TEXT.get_rect(center=(500, 600))

                            SCREEN.blit(MENU_TEXT, MENU_RECT)
                            pygame.display.update()
                            time.sleep(2)
                            SCREEN.blit(BG, (0, 0))
                            SCREEN.blit(CR, (0, 0))
                            SCREEN.blit(GB, (0, 0))
                            SCREEN.blit(Box, (0, 0))

                            MENU_TEXT = get_font(20).render('{}'.format(self.monsterName), True,
                                                            "#000000")
                            MENU_RECT = MENU_TEXT.get_rect(center=(500, 600))

                            SCREEN.blit(MENU_TEXT, MENU_RECT)
                            pygame.display.update()
                            time.sleep(2)
                        else:
                            SCREEN.blit(BG, (0, 0))
                            SCREEN.blit(CR, (0, 0))
                            SCREEN.blit(GB, (0, 0))
                            SCREEN.blit(Box, (0, 0))
                            MENU_MOUSE_POS = pygame.mouse.get_pos()

                            MENU_TEXT = get_font(20).render(State2, True, "#000000")
                            MENU_RECT = MENU_TEXT.get_rect(center=(500, 600))

                            SCREEN.blit(MENU_TEXT, MENU_RECT)
                            pygame.display.update()
                            time.sleep(2)
                            SCREEN.blit(BG, (0, 0))
                            SCREEN.blit(CR, (0, 0))
                            SCREEN.blit(GB, (0, 0))
                            SCREEN.blit(Box, (0, 0))

                            MENU_TEXT = get_font(20).render('{}'.format(self.monsterName), True,
                                                            "#000000")
                            MENU_RECT = MENU_TEXT.get_rect(center=(500, 600))

                            SCREEN.blit(MENU_TEXT, MENU_RECT)
                            pygame.display.update()
                            time.sleep(2)
                    if HEAL_BUTTON.checkForInput(MENU_MOUSE_POS):
                        SCREEN.blit(BG, (0, 0))
                        SCREEN.blit(pygame.image.load("assets/CharacterHeal.png").convert_alpha(), (0, 0))
                        SCREEN.blit(GB, (0, 0))
                        SCREEN.blit(Box, (0, 0))

                        MENU_TEXT = get_font(20).render(self.player.name + ' self heals.', True, "#000000")
                        MENU_RECT = MENU_TEXT.get_rect(center=(500, 600))

                        SCREEN.blit(MENU_TEXT, MENU_RECT)
                        pygame.display.update()
                        time.sleep(2)
                        self.player.selfHeal()
                        SCREEN.blit(BG, (0, 0))
                        SCREEN.blit(CR, (0, 0))
                        SCREEN.blit(GB, (0, 0))
                        SCREEN.blit(Box, (0, 0))
                        MENU_MOUSE_POS = pygame.mouse.get_pos()

                        MENU_TEXT = get_font(20).render(self.player.__str__(), True, "#000000")
                        MENU_RECT = MENU_TEXT.get_rect(center=(500, 600))

                        SCREEN.blit(MENU_TEXT, MENU_RECT)
                        pygame.display.update()
                        time.sleep(2)
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        pygame.quit()
                        sys.exit()
            pygame.display.update()
        return
