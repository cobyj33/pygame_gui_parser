import pygame
import pygame_gui


class GUITree():
    """Think of it as the DOM Tree"""
    def __init__(self, manager: pygame_gui.UIManager):
        self.manager = manager