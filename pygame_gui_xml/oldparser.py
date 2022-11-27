import os
import bs4
from typing import Any, Callable, TypedDict, Iterable, TypeVar, Generic, Union
import pygame
import pygame_gui
import pygame_gui_xml.xmlast as xml
from xmlconstants import *



from collections import deque

ParsingFunction = Callable[[bs4.Tag, pygame_gui.UIManager, pygame_gui.core.UIElement | None, pygame_gui.core.IContainerLikeInterface | None], pygame_gui.core.UIElement]

# VALID XML TYPES: string, int, bool, float
# VALID XML AGGREGATE TYPES: list[string], list[int], list[bool], list[float]


T = TypeVar("T")

def validate_range(data: str) -> bool:
    split = [ string for string in data.split(" ") if len(string) > 0 ]
    if len(split) == 2 and all([ xml.is_num(string) for string in split ]):
        numericals = tuple([ float(string) for string in split ])
        return numericals[0] < numericals[1]
    return False

def get_range(data: str) -> tuple[float, float]:
    split = [ string for string in data.split(" ") if len(string) > 0 ]
    if len(split) == 2:
        if all([ xml.is_num(string) for string in split ]):
            numericals = tuple([ float(string) for string in split ])
            if numericals[0] < numericals[1]:
                return numericals
    raise ValueError(f' Could not parse range data for range {data} ')
    

vec4 = tuple[int, int, int, int]
def validate_rect(data: str) -> bool:
    print("Validate Rect Data: ", data)
    return all([ xml.is_num(string) for string in data.split(" ") ]) and len(data.split(" ")) == 4

def get_tag_rect(data: str) -> vec4:
    splitted = data.split(" ")
    if all([ xml.is_num(splitstring) for splitstring in splitted]):
        rect = [float(data) for data in splitted]
        datapoints = len(rect)
        if datapoints == 4:
            return tuple(rect)
    raise ValueError(f'Could not parse rect data {data}')


def validate_anchors(data: str) -> bool:
    return all([ anchor in validAnchors for anchor in data.split(" ") ])

def get_anchors(data: str) -> dict[str, str]:
    positioning = [ selection.strip() for selection in data.split(" ") ]
    positioning = [ position for position in positioning if position in validAnchors ]
    print(positioning)
    anchors: dict[str, str] = dict()
    for position in positioning:
        anchors[position] = position
    return anchors
    return {}

rect = xml.XMLAttributeParserSchema[vec4]("rect", True, get_tag_rect, validate_rect)
anchors = xml.XMLAttributeParserSchema[dict[str, str]]("anchors", False, get_anchors, validate_anchors)
resizable = xml.XMLBoolAttributeParserSchema( "resizable", False)
selected = xml.XMLBoolAttributeParserSchema("selected", False)
src = xml.XMLAttributeParserSchema[str]("src", True, lambda data: data, lambda data: os.path.exists(os.path.abspath(data)) )
multiselect = xml.XMLBoolAttributeParserSchema("multiselect", False)
title = xml.XMLStringAttributeParserSchema("title", False)
start = xml.XMLFloatAttributeParserSchema("start", False)
range_value = xml.XMLAttributeParserSchema[tuple[float, float]]("range", False, get_range, validate_range)
click_increment = xml.XMLIntAttributeParserSchema("click-increment", False)

pygamegui = xml.XMLTagParserSchema("pygamegui", [], validTags)


head = xml.XMLTagParserSchema("head", [], ["themes"])
themes = xml.XMLTagParserSchema("themes", [], ["theme"])
theme = xml.XMLTagParserSchema("theme", [], [])

body = xml.XMLTagParserSchema("body", [rect], elementTags)
button = xml.XMLTagParserSchema("button", [rect, anchors], [])
image = xml.XMLTagParserSchema("image", [src, rect, anchors], [])
window = xml.XMLTagParserSchema("window", [title], elementTags)
panel = xml.XMLTagParserSchema("panel", [rect, anchors], [])
label = xml.XMLTagParserSchema("label", [rect, anchors], [])
textbox = xml.XMLTagParserSchema("textbox", [rect, anchors], [])
statusbar = xml.XMLTagParserSchema("statusbar", [rect, anchors], [])

selectionlist = xml.XMLTagParserSchema("selectionlist", [rect, anchors], ["item"])
item = xml.XMLTagParserSchema("item", [selected], [])

horizontalslider = xml.XMLTagParserSchema("horizontalslider", [rect, anchors, start, range_value, click_increment], [])


schemas: list[xml.XMLTagParserSchema] = [pygamegui, head, themes, theme, body, button, image, window, panel]

parser = xml.XMLParser([])


# def parse_button(tag: bs4.Tag, info: ParsingInfo)  -> pygame_gui.elements.UIButton:
#     if tag.name == "button":
#         rect = get_tag_rect(tag)
#         strings = tag.strings
#         # print("Parent: ", parent, "Container: ", container)
#         return pygame_gui.elements.UIButton(relative_rect=rect, **info, text="".join(strings), anchors=get_anchors(tag))
#     raise ValueError(f'Could not parse button, invalid tag name ${tag}')

# def parse_pygamegui(tag: bs4.Tag, info: ParsingInfo)  -> pygame_gui.elements.UIButton:
#     if tag.name == "pygamegui":
#         rect = pygame.Rect((0, 0), info["manager"].window_resolution)
#         if "rect" in tag:
#             rect = get_tag_rect(tag)
#         return pygame_gui.core.UIContainer(relative_rect=rect, **info, anchors=get_anchors(tag))
#     raise ValueError(f'Could not parse pygamegui, invalid tag name ${tag}')

# def parse_image(tag: bs4.Tag, info: ParsingInfo) -> pygame_gui.elements.UIButton:
#     if tag.name == "image":
#         rect = get_tag_rect(tag)
#         surface = pygame.surface.Surface(rect[2:]).convert_alpha()
#         surface.fill("White")
#         if "src" in tag.attrs:
#             abspath = str(os.path.abspath(tag["src"]))
#             surface = pygame.image.load(abspath)
#         return pygame_gui.elements.UIImage(relative_rect=rect, image_surface=surface, **info, anchors=get_anchors(tag))
#     raise ValueError(f'Could not parse image, invalid tag name ${tag}')

# def parse_body(tag: bs4.Tag, info: ParsingInfo)  -> pygame_gui.elements.UIButton:
#     if tag.name == "body":
#         rect = pygame.Rect((0, 0), info["manager"].window_resolution)
#         if "rect" in tag:
#             rect = get_tag_rect(tag)
#         return pygame_gui.core.UIContainer(relative_rect=rect, **info, anchors=get_anchors(tag))
#     raise ValueError(f'Could not parse body, invalid tag name ${tag}')

# def parse_window(tag: bs4.Tag, info: ParsingInfo)  -> pygame_gui.elements.UIButton:
#     if tag.name == "window":
#         rect = get_tag_rect(tag)
#         title = get_str_attr(tag, "title", "Unnamed Window")
#         resizable = get_bool_attr(tag, "resizable", False)
#         return pygame_gui.elements.UIWindow(rect=rect, manager=info["manager"], window_display_title=title, resizable=resizable)
#     raise ValueError(f'Could not parse button, invalid tag name ${tag}')

# def parse_panel(tag: bs4.Tag, info: ParsingInfo) -> pygame_gui.elements.UIPanel:
#     if tag.name == "panel":
#         rect = get_tag_rect(tag)
#         anchors = get_anchors(tag)
#         return pygame_gui.elements.UIPanel(rect, 1, **info, anchors=anchors)
#     raise ValueError(f'Could not parse button, invalid tag name ${tag}')

# def parse_label(tag: bs4.Tag, info: ParsingInfo) -> pygame_gui.elements.UILabel:
#     if tag.name == "label":
#         rect = get_tag_rect(tag)
#         anchors = get_anchors(tag)
#         strings = [ string for string in list(tag.strings) if len(string) > 0 ]
#         return pygame_gui.elements.UILabel(rect, text="".join(strings), **info, anchors=anchors)
#     raise ValueError(f'Could not parse label, invalid tag name ${tag}')

# def parse_textbox(tag: bs4.Tag, info: ParsingInfo) -> pygame_gui.elements.UITextBox:
#     if tag.name == "textbox":
#         rect = get_tag_rect(tag)
#         anchors = get_anchors(tag)
#         strings = tag.strings
#         return pygame_gui.elements.UITextBox("".join(strings), rect, **info, anchors=anchors)
#     raise ValueError(f'Could not parse textbox, invalid tag name ${tag}')

# def parse_statusbar(tag: bs4.Tag, info: ParsingInfo) -> pygame_gui.elements.UIStatusBar:
#     if tag.name == "statusbar":
#         rect = get_tag_rect(tag)
#         anchors = get_anchors(tag)
#         return pygame_gui.elements.UIStatusBar(rect, **info, anchors=anchors)
#     raise ValueError(f'Could not parse statusbar, invalid tag name ${tag}')

# def parse_selectionlist(tag: bs4.Tag, info: ParsingInfo) -> pygame_gui.elements.UISelectionList:
#     if tag.name == "selectionlist":
#         rect = get_tag_rect(tag)
#         anchors = get_anchors(tag)
#         multiselect = get_bool_attr(tag, "multiselect", False)
#         item_list = tag.find_all("item")
#         selected = [ item for item in item_list if "selected" in item.attrs ]
#         selectedStrings = [ "".join(list(item.strings)) for item in selected if item["selected"] in confirmation ]
#         selectedStrings = [ selectedString for selectedString in selectedStrings if len(selectedString) > 0 ]

#         stringlists = [ list(item.strings) for item in item_list ]
#         strings = [ "".join(stringlist) for stringlist in stringlists if len(stringlist) > 0 ]
#         return pygame_gui.elements.UISelectionList(rect, item_list=strings,  **info, anchors=anchors, allow_multi_select=multiselect, default_selection=selectedStrings)
#     raise ValueError(f'Could not parse selectionlist, invalid tag name ${tag}')

# def parse_horizontalslider(tag: bs4.Tag, info: ParsingInfo) -> pygame_gui.elements.UIHorizontalSlider:
#     if tag.name == "horizontalslider":
#         rect = get_tag_rect(tag)
#         anchors = get_anchors(tag)
#         start_value = get_num_attr(tag, "start", 0)
#         range_value = get_num_tuple_attr(tag, "range", 2, (0, 100))
#         click_increment = get_num_attr(tag, "click-increment", 1)

#         print(start_value, range_value, click_increment)
        
#         return pygame_gui.elements.UIHorizontalSlider(rect, start_value=start_value, value_range=range_value, **info, anchors=anchors, click_increment=click_increment)
#     raise ValueError(f'Could not parse horizontalslider, invalid tag name ${tag}')

# def parse_dropdownmenu(tag: bs4.Tag, info: ParsingInfo) -> pygame_gui.elements.UIDropDownMenu:
#     if tag.name == "dropdown" or tag.name == "dropdownmenu":
#         rect = get_tag_rect(tag)
#         anchors = get_anchors(tag)

#         options_list = [ "".join(list(option.strings)) for option in tag.find_all("option") if len(list(option.strings)) > 0 ]
#         print(options_list)
#         if len(options_list) == 0:
#             return pygame_gui.elements.UIDropDownMenu([], "", rect, **info, anchors=anchors)
#         starting_option = options_list[0]
#         starting_option_overrides = [ "".join(list(option.strings)) for option in tag.find_all("option") if len(list(option.strings)) > 0 and "start" in option.attrs and option["start"] in confirmation  ]

#         if len(starting_option_overrides) > 0:
#             starting_option = starting_option_overrides[0]
        
#         return pygame_gui.elements.UIDropDownMenu(options_list, starting_option, rect, **info, anchors=anchors)
#     raise ValueError(f'Could not parse dropdown, invalid tag name ${tag}')

# def parse_textentryline(tag: bs4.Tag, info: ParsingInfo) -> pygame_gui.elements.UITextEntryLine:
#     if tag.name == "textentryline":
#         rect = get_tag_rect(tag)
#         anchors = get_anchors(tag)
#         placeholder = get_str_attr(tag, "placeholder", "")
#         initial = get_str_attr(tag, "initial", "")
#         return pygame_gui.elements.UITextEntryLine(rect, **info, anchors=anchors, placeholder_text=placeholder, initial_text=initial)
#     raise ValueError(f'Could not parse textentryline, invalid tag name ${tag}')

# def parse_textentrybox(tag: bs4.Tag, info: ParsingInfo) -> pygame_gui.elements.UITextEntryBox:
#     if tag.name == "textentrybox":
#         rect = get_tag_rect(tag)
#         anchors = get_anchors(tag)
#         initial = get_str_attr(tag, "initial", "")
#         return pygame_gui.elements.UITextEntryBox(rect, **info, anchors=anchors, initial_text=initial)
#     raise ValueError(f'Could not parse textentrybox, invalid tag name ${tag}')

# def parse_tooltip(tag: bs4.Tag, info: ParsingInfo) -> pygame_gui.elements.UITooltip:
#     if tag.name == "tooltip":
#         anchors = get_anchors(tag)
#         text = "".join(tag.strings)
#         hover_distance = get_num_tuple_attr(tag, "hover-distance", 2, (5, 5))

#         return pygame_gui.elements.UITooltip(text, hover_distance, info["manager"], info["parent_element"], anchors=anchors)
#     raise ValueError(f'Could not parse tooltip, invalid tag name ${tag}')


# def parse_button(tag: bs4.Tag, manager: pygame_gui.UIManager, parent: pygame_gui.core.UIElement | None)  -> pygame_gui.elements.UIButton:
#     if tag.name == "button":
#         rect = get_tag_rect(tag)
#         return pygame_gui.elements.UIButton(relative_rect=rect)
#     raise ValueError(f'Could not parse button, invalid tag name ${tag}')

# parsingFunctions: dict[str, ParsingFunction] = {
#     "button": parse_button,
#     "pygamegui": parse_pygamegui,
#     "window": parse_window,
#     "body": parse_body,
#     "image": parse_image,
#     "panel": parse_panel,
#     "label": parse_label,
#     "textbox": parse_textbox,
#     "statusbar": parse_statusbar,
#     "selectionlist": parse_selectionlist,
#     "horizontalslider": parse_horizontalslider,
#     "dropdownmenu": parse_dropdownmenu,
#     "textentrybox": parse_textentrybox,
#     "textentryline": parse_textentryline,
#     "tooltip": parse_tooltip
# }

# def parse_xml_node(node: XMLNode) -> pygame_gui.core.UIElement:
#     rect = 


# def parse_tag(tag: bs4.Tag, info: ParsingInfo):
#     # print("Current Tag: ", tag)
#     if tag.name in validTags:
#         if tag.name in parsingFunctions:

#             pygameGUIElement = parsingFunctions[tag.name](tag, info)
#             # print(pygameGUIElement, isinstance(pygameGUIElement, pygame_gui.core.IContainerLikeInterface))
#             nextContainer = pygameGUIElement if isinstance(pygameGUIElement, pygame_gui.core.IContainerLikeInterface) else info["container"]
#             childTags = [ childTag for childTag in tag.children if not isinstance(childTag, bs4.NavigableString) ]
#             nextInfo: ParsingInfo = {
#                 "manager": info["manager"],
#                 "parent_element": pygameGUIElement,
#                 "container": nextContainer 
#             }

#             for child in childTags:
#                 parse_tag(child, nextInfo)
#         else:
#             print(f'Could not find corresponding parsing function for tag {tag.name}')
#     else:
#         print(f'Could not parse tag {tag.name}, seen as invalid')

def parse_xml(source: str, *themes: str, use_themes_in_file: bool = True) -> pygame_gui.UIManager:
    manager = pygame_gui.UIManager(pygame.display.get_window_size())
    for theme in themes:
        manager.get_theme().load_theme(theme)

    with open(source, "r") as f:
        content = "".join(f.readlines());
        xml = bs4.BeautifulSoup(content, "lxml-xml")

        if use_themes_in_file:
            themesTag = xml.find("themes")
            if not themesTag is None:
                themes = [theme.string for theme in xml.find_all("theme")]
                themes = [ theme.strip() for theme in themes ]
                for theme in themes:
                    abspath = str(os.path.abspath(theme))
                    print("Loading Theme", abspath)
                    manager.get_theme().load_theme(abspath)
            
        parent = pygame_gui.core.UIContainer(relative_rect=pygame.Rect((0, 0), manager.window_resolution), manager=manager)
        startingInfo: ParsingInfo = {
            "manager": manager,
            "parent_element": parent,
            "container": None
        }

        parse_tag(xml.body, startingInfo)
    return manager

# def parse_xml_tree(tree: XMLNode) -> pygame_gui.UIManager:
#     manager = pygame_gui.UIManager(pygame.display.get_window_size())
#     queue: deque[XMLNode] = deque(tree)

#     for theme in themes:
#         manager.get_theme().load_theme(theme)

#     with open(source, "r") as f:
#         content = "".join(f.readlines());
#         xml = bs4.BeautifulSoup(content, "lxml-xml")

#         if use_themes_in_file:
#             themesTag = xml.find("themes")
#             if not themesTag is None:
#                 themes = [theme.string for theme in xml.find_all("theme")]
#                 themes = [ theme.strip() for theme in themes ]
#                 for theme in themes:
#                     abspath = str(os.path.abspath(theme))
#                     print("Loading Theme", abspath)
#                     manager.get_theme().load_theme(abspath)
            
#         parent = pygame_gui.core.UIContainer(relative_rect=pygame.Rect((0, 0), manager.window_resolution), manager=manager)
#         startingInfo: ParsingInfo = {
#             "manager": manager,
#             "parent_element": parent,
#             "container": None
#         }

#         parse_tag(xml.body, startingInfo)
#     return manager