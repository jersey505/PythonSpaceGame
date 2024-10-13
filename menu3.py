import pygame, sys, os
from button import Button

pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")

BG = pygame.image.load("images/background.png")


def get_font(size):
    return pygame.font.SysFont('aerial', size)

def get_font2(size):
    return pygame.font.SysFont('calibri', size)


def play():
    os.system('pgzrun finalgame.py')
    exit()



def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        OPTIONS_TEXT = get_font(23).render("CONTROLS: " "WASD TO MOVE, " "F TO PICK UP ITEMS, " "E TO USE ITEMS, " "Q TO DROP ITEMS, " "TAB TO USE OTHER ITEMS, ""AND CLICK SPACE NEAR OBJECTS TO INSPECT THEM", True, "White")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(640, 660),
                              text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()


def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(50).render("MAIN MENU",  True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 120))
        MENU_TEXT2 = get_font2(50).render("MISSION PYTHON: ESCAPE", True, "#FF00FF")
        MENU_RECT2 = MENU_TEXT.get_rect(center=(475, 50))

        PLAY_BUTTON = Button(image=pygame.image.load("images/Play Rect.png"), pos=(640, 250),
                             text_input="PLAY", font=get_font(75), base_color="#000000", hovering_color="White")

        OPTIONS_BUTTON = Button(image=pygame.image.load("images/Options Rect.png"), pos=(640, 400),
                                text_input="CONTROLS", font=get_font(75), base_color="#000000", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("images/Quit Rect.png"), pos=(640, 550),
                             text_input="QUIT", font=get_font(75), base_color="#000000", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)
        SCREEN.blit(MENU_TEXT2, MENU_RECT2)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

sounds.steelmusic.play()

main_menu()