import xml.parser
import pygame
import pygame_gui

class GUI():
    def __init__(self, source: str, *themes: str, use_themes_in_file: bool = True):
        self.source = source
        self.themes = themes
        self.use_themes_in_file = use_themes_in_file
        self.manager = xml.parser.parse_xml(self.source, *self.themes, use_themes_in_file=self.use_themes_in_file)

        
    def construct(self):
        self.manager = xml.parser.parse_xml(self.source, *self.themes, use_themes_in_file=self.use_themes_in_file)

    def process_events(self, event: pygame.event.Event):
        if event.type == pygame.VIDEORESIZE:
            self.manager.set_window_resolution(pygame.display.get_window_size())

        self.manager.process_events(event)
    
    def update(self, dt: float):
        self.manager.update(dt)

    def draw_ui(self, target: pygame.surface.Surface):
        self.manager.draw_ui(target)
