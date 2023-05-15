from logic.fighter.Player import Player
import pygame
import pygame_gui
import sys

pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Name")

BG = pygame.image.load("assets/Background.png")


def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)


manager = pygame_gui.UIManager((1600, 900))

text_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((300, 275), (700, 50)), manager=manager,
                                                 object_id='#main_text_entry')

clock = pygame.time.Clock()


def createPlayer() -> 'Player':
    while True:

        UI_REFRESH_RATE = clock.tick(60) / 1000
        SCREEN.blit(BG, (0, 0))
        MENU_TEXT = get_font(50).render("What is your name?:", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if (event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and
                    event.ui_object_id == '#main_text_entry'):
                return Player(event.text)
            manager.process_events(event)
        SCREEN.blit(MENU_TEXT, MENU_RECT)
        manager.update(UI_REFRESH_RATE)

        manager.draw_ui(SCREEN)

        pygame.display.update()
    """name = input('What is your name?: ')"""
