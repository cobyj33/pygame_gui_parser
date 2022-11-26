import pygame
import pygame_gui
import pygameguiparser

pygame.init()
DEFAULT_GAME_WIDTH = 800
DEFAULT_GAME_HEIGHT = 600
DEFAULT_GAME_SIZE = (DEFAULT_GAME_WIDTH, DEFAULT_GAME_HEIGHT)
screen = pygame.display.set_mode(DEFAULT_GAME_SIZE, pygame.RESIZABLE)
pygame.display.set_caption("Pygame GUI Markup Testing")
clock = pygame.time.Clock()
RUNNING = True

manager = pygame_gui.UIManager(DEFAULT_GAME_SIZE)
# window = pygame_gui.core.UIContainer(pygame.Rect((0, 0), DEFAULT_GAME_SIZE), manager)
# hello_button = pygame_gui.elements.UIButton(pygame.Rect(0, 0, 200, 100), "Hello World", manager, window, "Click Me", anchors={"center": "center"}, allow_double_clicks=True)


background = pygame.surface.Surface(DEFAULT_GAME_SIZE).convert_alpha()
TRANSPARENT = pygame.color.Color(0, 0, 0, 0)
background.fill("White")

DELTA_TIME = 0
FRAMERATE = 60

gui = pygameguiparser.GUI("mainmenu.xml")

while RUNNING:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
        if event.type == pygame.WINDOWRESIZED:
            background = pygame.surface.Surface(pygame.display.get_window_size()).convert_alpha()
            background.fill("White")
        # if event.type == pygame_gui.UI_BUTTON_PRESSED:
        #     if event.ui_element == hello_button:
        #         print("Hello World")
        # if event.type == pygame_gui.UI_BUTTON_DOUBLE_CLICKED:
        #     if event.ui_element == hello_button:
        #         print("Hello World X2")
        # manager.process_events(event)
        gui.process_events(event)
    
    # manager.update(DELTA_TIME)
    gui.update(DELTA_TIME)

    screen.blit(background, (0, 0))
    # manager.draw_ui(screen)
    gui.draw_ui(screen)

    pygame.display.update()
    DELTA_TIME = clock.tick(FRAMERATE)