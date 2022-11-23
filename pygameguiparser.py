import sys
import os
import bs4
from typing import Any, Callable
import pygame
import pygame_gui

ParsingFunction = Callable[[bs4.Tag, pygame_gui.UIManager, pygame_gui.core.UIElement | None, pygame_gui.core.IContainerLikeInterface | None], pygame_gui.core.UIElement]
confirmation = ["true", "yes", "y", "enable", "enabled", "t"]
rejection = ["false", "f", "no", "n", "disabled", "disable"]

validAnchors = ["left", "right", "top", "bottom", "center", "centerx", "centery"]
def get_anchors(tag: bs4.Tag) -> dict[str, str]:
    if "anchors" in tag.attrs:
        positioning = [ selection.strip() for selection in tag["anchors"].split(" ") ]
        positioning = [ position in validAnchors for position in positioning ]
        anchors: dict[str, str] = dict()
        for position in positioning:
            anchors[position] = position
        return anchors
    return {}

def get_tag_rect(tag: bs4.Tag) -> pygame.Rect:
    if "rect" in tag.attrs:
        string = tag["rect"]
        splitted = string.split(" ")
        if all([splitstring.isnumeric() for splitstring in splitted]):
            rect = [float(data) for data in splitted]
            datapoints = len(rect)
            if datapoints == 4:
                # print(rect)
                return pygame.Rect(rect)
            else:
                raise ValueError(f'Error while parsing tag {tag.name} from {tag.parents} for rect attribute: Needed 4 positional arguments for rect, found {datapoints}')
        else:
            raise ValueError(f'Error while parsing tag {tag.name} from {tag.parents} for rect attribute: Not all arguments in rect position ({splitted}) are numerical')
    else:
        raise ValueError(f'Error while parsing tag {tag.name} from {tag.parents} for rect attribute: no rect attribute found (attributes found: {tag.attrs})')

def parse_button(tag: bs4.Tag, manager: pygame_gui.UIManager, parent: pygame_gui.core.UIElement | None, container: pygame_gui.core.IContainerLikeInterface | None)  -> pygame_gui.elements.UIButton:
    if tag.name == "button":
        rect = get_tag_rect(tag)
        strings = tag.strings
        # print("Parent: ", parent, "Container: ", container)
        return pygame_gui.elements.UIButton(relative_rect=rect, manager=manager, parent_element=parent, text="".join(strings), container=container, anchors=get_anchors(tag))
    raise ValueError(f'Could not parse button, invalid tag name ${tag}')

def parse_pygamegui(tag: bs4.Tag, manager: pygame_gui.UIManager, parent: pygame_gui.core.UIElement | None, container: pygame_gui.core.IContainerLikeInterface | None)  -> pygame_gui.elements.UIButton:
    if tag.name == "pygamegui":
        rect = pygame.Rect((0, 0), manager.window_resolution)
        if "rect" in tag:
            rect = get_tag_rect(tag)
        return pygame_gui.core.UIContainer(relative_rect=rect, manager=manager, parent_element=parent, container=container, anchors=get_anchors(tag))
    raise ValueError(f'Could not parse pygamegui, invalid tag name ${tag}')

def parse_image(tag: bs4.Tag, manager: pygame_gui.UIManager, parent: pygame_gui.core.UIElement | None, container: pygame_gui.core.IContainerLikeInterface | None) -> pygame_gui.elements.UIButton:
    if tag.name == "image":
        rect = get_tag_rect(tag)
        surface = pygame.surface.Surface(rect[2:]).convert_alpha()
        surface.fill("White")
        if "src" in tag.attrs:
            abspath = str(os.path.abspath(tag["src"]))
            surface = pygame.image.load(abspath)
        return pygame_gui.elements.UIImage(relative_rect=rect, image_surface=surface, manager=manager, container=container, parent_element=parent, anchors=get_anchors(tag))
    raise ValueError(f'Could not parse image, invalid tag name ${tag}')

def parse_body(tag: bs4.Tag, manager: pygame_gui.UIManager, parent: pygame_gui.core.UIElement | None, container: pygame_gui.core.IContainerLikeInterface | None)  -> pygame_gui.elements.UIButton:
    if tag.name == "body":
        rect = pygame.Rect((0, 0), manager.window_resolution)
        if "rect" in tag:
            rect = get_tag_rect(tag)
        return pygame_gui.core.UIContainer(relative_rect=rect, manager=manager, parent_element=parent, container=container, anchors=get_anchors(tag))
    raise ValueError(f'Could not parse body, invalid tag name ${tag}')

def parse_window(tag: bs4.Tag, manager: pygame_gui.UIManager, parent: pygame_gui.core.UIElement | None, container: pygame_gui.core.IContainerLikeInterface | None)  -> pygame_gui.elements.UIButton:
    if tag.name == "window":
        rect = get_tag_rect(tag)
        # print(tag.attrs)
        title = "Unnamed Window"
        resizable = False
        if "title" in tag.attrs:
            title = tag["title"]
        if "resizable" in tag.attrs:
            if tag["resizable"].lower() in confirmation:
                resizable = True
        return pygame_gui.elements.UIWindow(rect=rect, manager=manager, window_display_title=title, resizable=resizable)
    raise ValueError(f'Could not parse button, invalid tag name ${tag}')


# def parse_button(tag: bs4.Tag, manager: pygame_gui.UIManager, parent: pygame_gui.core.UIElement | None)  -> pygame_gui.elements.UIButton:
#     if tag.name == "button":
#         rect = get_tag_rect(tag)
#         return pygame_gui.elements.UIButton(relative_rect=rect)
#     raise ValueError(f'Could not parse button, invalid tag name ${tag}')

validTags = ["body", "image", "pygamegui", "button", "dropdownmenu", "horizontalslider", "window", "progressbar", "selectionlist", "worldspacehealthbar", "screenspacehealthbar", "image", "label", "panel", "textbox", "container", "textentryline", "tooltip", "messagewindow", "consolewindow", "confirmationdialog", "colorpickerdialog", "filedialog"]
parsingFunctions: dict[str, ParsingFunction] = {
    "button": parse_button,
    "pygamegui": parse_pygamegui,
    "window": parse_window,
    "body": parse_body,
    "image": parse_image
}



def parse_tag(tag: bs4.Tag, manager: pygame_gui.UIManager, parent: pygame_gui.core.UIElement | None, container: pygame_gui.core.IContainerLikeInterface | None):
    # print("Current Tag: ", tag)
    if tag.name in validTags:
        if tag.name in parsingFunctions:
            pygameGUIElement = parsingFunctions[tag.name](tag, manager, parent, container)
            # print(pygameGUIElement, isinstance(pygameGUIElement, pygame_gui.core.IContainerLikeInterface))
            nextContainer = pygameGUIElement if isinstance(pygameGUIElement, pygame_gui.core.IContainerLikeInterface) else container
            childTags = [ childTag for childTag in tag.children if not isinstance(childTag, bs4.NavigableString) ]
            for child in childTags:
                parse_tag(child, manager, pygameGUIElement, nextContainer)

class GUI():
    def __init__(self, source: str, *themes: str, use_themes_in_file: bool = True):
        self.manager = pygame_gui.UIManager(pygame.display.get_window_size())
        for theme in themes:
            self.manager.get_theme().load_theme(theme)

        
        with open(source, "r") as f:
            content = "".join(f.readlines());
            xml = bs4.BeautifulSoup(content, "lxml-xml")
            if use_themes_in_file:
                themesTag = xml.find("themes")
                if not themesTag == None:
                    themes = [theme.string for theme in xml.find_all("theme")]
                    themes = [ theme.strip() for theme in themes ]
                    for theme in themes:
                        abspath = str(os.path.abspath(theme))
                        print("Loading Theme", abspath)
                        self.manager.get_theme().load_theme(abspath)
                
            parent = pygame_gui.core.UIContainer(relative_rect=pygame.Rect((0, 0), self.manager.window_resolution), manager=self.manager)
            parse_tag(xml.body, self.manager, parent, None)
            

    def process_events(self, event: pygame.event.Event):
        if event.type == pygame.VIDEORESIZE:
            self.manager.set_window_resolution(pygame.display.get_window_size())
        self.manager.process_events(event)
    
    def update(self, dt: float):
        self.manager.update(dt)

    def draw_ui(self, target: pygame.surface.Surface):
        self.manager.draw_ui(target)
