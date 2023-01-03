import os
import pygame
import pygame_gui
from typing import TypedDict, Iterable, Callable, TypeVar, Generic
import pygame_gui_xml.xmlast
import pygame_gui_xml.xmlparser
from pygame_gui_xml._config import is_valid_tag
import warnings

T = TypeVar("T")
class ParsingInfo(TypedDict):
    manager: pygame_gui.UIManager
    parent_element: pygame_gui.core.UIElement
    container: pygame_gui.core.IContainerLikeInterface

ParsingFunction = Callable[[pygame_gui_xml.xmlast.XMLNode, ParsingInfo], pygame_gui.core.UIElement]

def get_object_id(node: pygame_gui_xml.xmlast.XMLNode):
    object_id: str = node.attrs.get("id")
    class_id: str = node.attrs.get("class")
    if not object_id is None:
        if not object_id.startswith("#"):
            object_id = "#" + object_id
    if not class_id is None:
        if not class_id.startswith("@"):
            class_id = "@" + object_id
    return pygame_gui.core.ObjectID(object_id or "", class_id or "")

def parse_button(node: pygame_gui_xml.xmlast.XMLNode, info: ParsingInfo)  -> pygame_gui.elements.UIButton:
    if node.name == "button":
        rect = pygame.Rect(node.attrs["rect"])
        anchors = node.attrs.get("anchors") or {}
        objectid = get_object_id(node)
        tooltip = node.attrs.get("tooltip")
        return pygame_gui.elements.UIButton(relative_rect=rect, anchors=anchors, **info, text=node.text, object_id=objectid, tool_tip_text=tooltip)
    raise ValueError(f'Could not parse button, invalid node name {node}')

def parse_pygamegui(node: pygame_gui_xml.xmlast.XMLNode, info: ParsingInfo)  -> pygame_gui.core.UIContainer:
    if node.name == "pygamegui":
        rect = pygame.Rect((0, 0), info["manager"].window_resolution)
        return pygame_gui.core.UIContainer(relative_rect=rect, **info)
    raise ValueError(f'Could not parse pygamegui, invalid node name {node}')

def parse_image(node: pygame_gui_xml.xmlast.XMLNode, info: ParsingInfo) -> pygame_gui.elements.UIImage:
    if node.name == "image":
        rect = pygame.Rect(node.attrs["rect"])
        anchors = node.attrs.get("anchors") or {}
        objectid = get_object_id(node)
        surface = pygame.surface.Surface(rect[2:]).convert_alpha()
        surface.fill("White")
        if "src" in node.attrs:
            abspath = str(os.path.abspath(node.attrs["src"]))
            surface = pygame.image.load(abspath).convert_alpha()
        return pygame_gui.elements.UIImage(relative_rect=rect, image_surface=surface, **info, anchors=anchors, object_id=objectid)
    raise ValueError(f'Could not parse image, invalid node name {node}')

def parse_body(node: pygame_gui_xml.xmlast.XMLNode, info: ParsingInfo)  -> pygame_gui.core.UIContainer:
    if node.name == "body":
        rect = node.attrs.get("rect") or pygame.Rect((0, 0), info["manager"].window_resolution)
        return pygame_gui.core.UIContainer(relative_rect=rect, **info, anchors={})
    raise ValueError(f'Could not parse body, invalid node name {node}')

def parse_window(node: pygame_gui_xml.xmlast.XMLNode, info: ParsingInfo)  -> pygame_gui.elements.UIWindow:
    if node.name == "window":
        rect = pygame.Rect(node.attrs["rect"])
        title = node.attrs.get("title") or "Unnamed Window"
        objectid = get_object_id(node)
        resizable = node.attrs.get("resizable") or False
        return pygame_gui.elements.UIWindow(rect=rect, manager=info["manager"], window_display_title=title, resizable=resizable, object_id=objectid)
    raise ValueError(f'Could not parse button, invalid node name {node}')

def parse_panel(node: pygame_gui_xml.xmlast.XMLNode, info: ParsingInfo) -> pygame_gui.elements.UIPanel:
    if node.name == "panel":
        rect = pygame.Rect(node.attrs["rect"])
        objectid = get_object_id(node)
        anchors = node.attrs.get("anchors") or {}
        return pygame_gui.elements.UIPanel(rect, 1, **info, anchors=anchors, object_id=objectid)
    raise ValueError(f'Could not parse button, invalid node name {node}')

def parse_label(node: pygame_gui_xml.xmlast.XMLNode, info: ParsingInfo) -> pygame_gui.elements.UILabel:
    if node.name == "label":
        rect = pygame.Rect(node.attrs["rect"])
        objectid = get_object_id(node)
        anchors = node.attrs.get("anchors") or {}
        return pygame_gui.elements.UILabel(rect, text=node.text, **info, anchors=anchors, object_id=objectid)
    raise ValueError(f'Could not parse label, invalid node name {node}')

def parse_textbox(node: pygame_gui_xml.xmlast.XMLNode, info: ParsingInfo) -> pygame_gui.elements.UITextBox:
    if node.name == "textbox":
        rect = pygame.Rect(node.attrs["rect"])
        anchors = node.attrs.get("anchors") or {}
        objectid = get_object_id(node)
        return pygame_gui.elements.UITextBox(node.text, rect, **info, anchors=anchors, object_id=objectid)
    raise ValueError(f'Could not parse textbox, invalid node name {node}')

def parse_statusbar(node: pygame_gui_xml.xmlast.XMLNode, info: ParsingInfo) -> pygame_gui.elements.UIStatusBar:
    if node.name == "statusbar":
        rect = pygame.Rect(node.attrs["rect"])
        anchors = node.attrs.get("anchors") or {}
        objectid = get_object_id(node)
        return pygame_gui.elements.UIStatusBar(rect, **info, anchors=anchors, object_id=objectid)
    raise ValueError(f'Could not parse statusbar, invalid node name {node}')

def parse_selectionlist(node: pygame_gui_xml.xmlast.XMLNode, info: ParsingInfo) -> pygame_gui.elements.UISelectionList:
    if node.name == "selectionlist":
        rect = pygame.Rect(node.attrs["rect"])
        anchors = node.attrs.get("anchors") or {}
        objectid = get_object_id(node)
        multiselect = node.attrs.get("multiselect") or False
        items = [ child for child in node.children if child.name == "item" ]
        selected = [ item.text for item in items if item.attrs.get("selected") == True ]

        return pygame_gui.elements.UISelectionList(rect, item_list=[item.text for item in items],  **info, anchors=anchors, allow_multi_select=multiselect, default_selection=selected, object_id=objectid)
    raise ValueError(f'Could not parse selectionlist, invalid node name {node}')

def parse_horizontalslider(node: pygame_gui_xml.xmlast.XMLNode, info: ParsingInfo) -> pygame_gui.elements.UIHorizontalSlider:
    if node.name == "horizontalslider":
        rect = pygame.Rect(node.attrs["rect"])
        anchors = node.attrs.get("anchors") or {}
        objectid = get_object_id(node)
        start_value = node.attrs.get("start") or 0
        range_value = node.attrs.get("range") or (0, 100)
        click_increment = node.attrs.get("click-increment") or 1

        return pygame_gui.elements.UIHorizontalSlider(rect, start_value=start_value, value_range=range_value, **info, anchors=anchors, click_increment=click_increment, object_id=objectid)
    raise ValueError(f'Could not parse horizontalslider, invalid node name {node}')

def parse_dropdownmenu(node: pygame_gui_xml.xmlast.XMLNode, info: ParsingInfo) -> pygame_gui.elements.UIDropDownMenu:
    if node.name == "dropdown" or node.name == "dropdownmenu":
        rect = pygame.Rect(node.attrs["rect"])
        anchors = node.attrs.get("anchors") or {}
        objectid = get_object_id(node)
        options = [ child for child in node.children if child.name == "option" ]
        if len(options) == 0:
            return pygame_gui.elements.UIDropDownMenu([], "", rect, **info, anchors=anchors)
        starting_option = next([ option.text for option in options if option.attrs.get("start") == True], options[0].text)
        return pygame_gui.elements.UIDropDownMenu([ option.text for option in options ], starting_option, rect, **info, anchors=anchors, object_id=objectid)
    raise ValueError(f'Could not parse dropdown, invalid node name {node}')

def parse_textentryline(node: pygame_gui_xml.xmlast.XMLNode, info: ParsingInfo) -> pygame_gui.elements.UITextEntryLine:
    if node.name == "textentryline":
        rect = pygame.Rect(node.attrs["rect"])
        anchors = node.attrs.get("anchors") or {}
        objectid = get_object_id(node)
        placeholder = node.attrs.get("placeholder") or "" 
        initial = node.attrs.get("initial") or ""
        return pygame_gui.elements.UITextEntryLine(rect, **info, anchors=anchors, placeholder_text=placeholder, initial_text=initial, object_id=objectid)
    raise ValueError(f'Could not parse textentryline, invalid node name {node}')

def parse_textentrybox(node: pygame_gui_xml.xmlast.XMLNode, info: ParsingInfo) -> pygame_gui.elements.UITextEntryBox:
    if node.name == "textentrybox":
        rect = pygame.Rect(node.attrs["rect"])
        anchors = node.attrs.get("anchors") or {}
        objectid = get_object_id(node)
        initial = node.attrs.get("initial") or ""
        return pygame_gui.elements.UITextEntryBox(rect, **info, anchors=anchors, initial_text=initial, object_id=objectid)
    raise ValueError(f'Could not parse textentrybox, invalid node name {node}')

def parse_tooltip(node: pygame_gui_xml.xmlast.XMLNode, info: ParsingInfo) -> pygame_gui.elements.UITooltip:
    if node.name == "tooltip":
        anchors = node.attrs.get("anchors") or {}
        objectid = get_object_id(node)
        hover_distance = node.attrs.get("hover-distance") or (5, 5)
        return pygame_gui.elements.UITooltip(node.text, hover_distance, info["manager"], info["parent_element"], anchors=anchors, object_id=objectid)
    raise ValueError(f'Could not parse tooltip, invalid node name {node}')

parsingFunctions: dict[str, ParsingFunction] = {
    "button": parse_button,
    "pygamegui": parse_pygamegui,
    "window": parse_window,
    "body": parse_body,
    "image": parse_image,
    "panel": parse_panel,
    "label": parse_label,
    "textbox": parse_textbox,
    "statusbar": parse_statusbar,
    "selectionlist": parse_selectionlist,
    "horizontalslider": parse_horizontalslider,
    "dropdownmenu": parse_dropdownmenu,
    "textentrybox": parse_textentrybox,
    "textentryline": parse_textentryline,
    "tooltip": parse_tooltip
}

pygame_gui.core.ObjectID()

# def parse_xml_node(node: xmlast.XMLNode, info: ParsingInfo) -> pygame_gui.core.UIElement:
    # objectid = get_object_id(node)

def parse_node(node: pygame_gui_xml.xmlast.XMLNode, info: ParsingInfo):
    # print("Current Tag: ", tag)
    if is_valid_tag(node.name):
        if node.name in parsingFunctions:
            pygameGUIElement = parsingFunctions[node.name](node, info)
            # print(pygameGUIElement, isinstance(pygameGUIElement, pygame_gui.core.IContainerLikeInterface))
            nextContainer = pygameGUIElement if isinstance(pygameGUIElement, pygame_gui.core.IContainerLikeInterface) else info["container"]
            nextInfo: ParsingInfo = {
                "manager": info["manager"],
                "parent_element": pygameGUIElement,
                "container": nextContainer 
            }

            for child in node.children:
                parse_node(child, nextInfo)
        else:
            print(f'Could not find corresponding parsing function for node {node}')
    else:
        print(f'Could not parse node {node}, seen as invalid')


def parse_xml_tree(manager: pygame_gui.UIManager, node: pygame_gui_xml.xmlast.XMLNode, themes: Iterable[str], use_themes_in_file: bool = True):
    info: ParsingInfo = {
        "manager": manager,
        "parent_element": None,
        "container": None 
    }

    if use_themes_in_file:
        for theme in themes:
            abspath = str(os.path.abspath(theme))
            print("Loading Theme", abspath)
            manager.get_theme().load_theme(abspath)

        themesNode = node.find("themes")
        if not themesNode is None:
            importedThemes = [theme.text.strip() for theme in themesNode.find_all("theme")]
            print(node)
            if "path" in node.attrs:
                for theme in importedThemes:
                    abspath = str(os.path.join(os.path.abspath( os.path.dirname(node.attrs["path"]) ), theme ))
                    print("Loading Theme", abspath)
                    manager.get_theme().load_theme(abspath)


    top = node.find("body")
    if top is None:
        raise ValueError("Could not parse PygameGUI XML: XML Node Tree has no body")

    parse_node(top, info)
    


class GUIState(Generic[T]):
    def __init__(self, value: T):
        self._value = value
        self._subscribed: dict[str, Callable[[T], None]] = {}

    def subscribe(self, _id: str, callback: Callable[[T], None]):
        if _id in self._subscribed:
            warnings.warn("Attempting to subscribe a new callback which has already been subscribed to")
        self._subscribed[_id] = callback

    def unsubscribe(self, _id: str):
        del self._subscribed[_id] 

    def _fire(self):
        for callback in self._subscribed.values():
            callback(self._value)
    
    def set(self, value: T):
        self._value = value

    def get(self) -> T:
        return self._value

class GUI():
    def __init__(self, source: str, *themes: str, use_themes_in_file: bool = True):
        self.source = source
        self.themes = themes
        self.use_themes_in_file = use_themes_in_file
        self.manager = pygame_gui.UIManager(pygame.display.get_window_size())
        self.nodetree: pygame_gui_xml.xmlast.XMLNode = pygame_gui_xml.xmlparser.parse_pygame_xml(source)
        parse_xml_tree(self.manager, self.nodetree, self.themes, self.use_themes_in_file)

    def construct(self):
        self.manager.clear_and_reset()
        self.manager.set_window_resolution(pygame.display.get_window_size())
        parse_xml_tree(self.manager, self.nodetree, self.themes, self.use_themes_in_file)

    def process_events(self, event: pygame.event.Event):
        if event.type == pygame.VIDEORESIZE:
            lastSize = self.manager.window_resolution
            scale = ( event.size[0] / lastSize[0], event.size[1] / lastSize[1] )
            nodesWithRect = self.nodetree.find_all_with_attrs(["rect"])
            for node in nodesWithRect:
                rect = node.attrs["rect"]
                node.attrs["rect"] = ( rect[0] * scale[0], rect[1] * scale[1], rect[2] * scale[0], rect[3] * scale[1] )
            self.construct()

        self.manager.process_events(event)
    
    def update(self, dt: float):
        self.manager.update(dt)

    def draw_ui(self, target: pygame.surface.Surface):
        self.manager.draw_ui(target)
