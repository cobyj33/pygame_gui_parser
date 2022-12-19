import os
import bs4
from typing import Any, Callable, TypedDict, Iterable, TypeVar, Generic, Union
import pygame
import pygame_gui
import pygame_gui_xml.ast as xmlast
from pygame_gui_xml._util import is_num_str
from collections import deque
from pygame_gui_xml._config import is_valid_anchor, get_valid_tags, get_element_tags



def validate_range(data: str) -> bool:
    split = [ string for string in data.split(" ") if len(string) > 0 ]
    if len(split) == 2 and all([ is_num_str(string) for string in split ]):
        numericals = tuple([ float(string) for string in split ])
        return numericals[0] < numericals[1]
    return False

def get_range(data: str) -> tuple[float, float]:
    split = [ string for string in data.split(" ") if len(string) > 0 ]
    if len(split) == 2:
        if all([ is_num_str(string) for string in split ]):
            numericals = tuple([ float(string) for string in split ])
            if numericals[0] < numericals[1]:
                return numericals
    raise ValueError(f' Could not parse range data for range {data} ')
    
def validate_hover_distance(data: str) -> bool:
    split = [ string for string in data.split(" ") if len(string) > 0 ]
    if len(split) == 2 and all([ xmlast.is_int_str(string) for string in split ]):
        return all([ int(string) > 0 for string in split ])
    return False

def get_hover_distance(data: str) -> tuple[int, int]:
    split = [ string for string in data.split(" ") if len(string) > 0 ]
    if len(split) == 2 and all([ xmlast.is_int_str(string) for string in split ]):
        numerics = [ int(string) for string in split ]
        if all([ num > 0 for num in numerics ]):
            return tuple(numerics)
    raise ValueError(f'Could not get Hover Distance, invalid data string {data}')

vec4 = tuple[int, int, int, int]
def validate_rect(data: str) -> bool:
    return all([ is_num_str(string) for string in data.split(" ") ]) and len(data.split(" ")) == 4

def get_tag_rect(data: str) -> vec4:
    splitted = data.split(" ")
    if all([ is_num_str(splitstring) for splitstring in splitted]):
        rect = [float(data) for data in splitted]
        datapoints = len(rect)
        if datapoints == 4:
            return tuple(rect)
    raise ValueError(f'Could not parse rect data {data}')


def validate_anchors(data: str) -> bool:
    return all([ is_valid_anchor(anchor) for anchor in data.split(" ") ])

def get_anchors(data: str) -> dict[str, str]:
    positioning = [ selection.strip() for selection in data.split(" ") ]
    positioning = [ position for position in positioning if is_valid_anchor(position) ]
    print(positioning)
    anchors: dict[str, str] = {}
    for position in positioning:
        anchors[position] = position
    return anchors

def get_class_id(data: str) -> bool:
    if not data[0] == "@":
        return "@" + data
    return data

def get_object_id(data: str) -> bool:
    if not data[0] == "#":
        return "#" + data
    return data


rect = xmlast.XMLAttributeParserSchema[vec4]("rect", True, get_tag_rect, validate_rect)
anchors = xmlast.XMLAttributeParserSchema[dict[str, str]]("anchors", False, get_anchors, validate_anchors)
resizable = xmlast.XMLBoolAttributeParserSchema( "resizable", False)
selected = xmlast.XMLBoolAttributeParserSchema("selected", False)
src = xmlast.XMLAttributeParserSchema[str]("src", True, lambda data: data, lambda data: os.path.exists(os.path.abspath(data)) )
multiselect = xmlast.XMLBoolAttributeParserSchema("multiselect", False)
title = xmlast.XMLStringAttributeParserSchema("title", False)
start = xmlast.XMLFloatAttributeParserSchema("start", False)
starting = xmlast.XMLBoolAttributeParserSchema("start", False)
range_value = xmlast.XMLAttributeParserSchema[tuple[float, float]]("range", False, get_range, validate_range)
click_increment = xmlast.XMLIntAttributeParserSchema("click-increment", False)
placeholder = xmlast.XMLStringAttributeParserSchema("placeholder", False)
initial = xmlast.XMLStringAttributeParserSchema("initial", False)
hover_distance = xmlast.XMLAttributeParserSchema[tuple[int, int]]("hover-distance", False, get_hover_distance, validate_hover_distance)
id_attr = xmlast.XMLAttributeParserSchema("id", False, get_object_id, lambda _: True)
class_attr = xmlast.XMLAttributeParserSchema("class", False, get_class_id, lambda _: True)
tooltip_attr = xmlast.XMLStringAttributeParserSchema("tooltip", False);

pygamegui = xmlast.XMLTagParserSchema("pygamegui", [], get_valid_tags())


head = xmlast.XMLTagParserSchema("head", [], ["themes"])
themes = xmlast.XMLTagParserSchema("themes", [], ["theme"])
theme = xmlast.XMLTagParserSchema("theme", [], [])

body = xmlast.XMLTagParserSchema("body", [rect], get_element_tags())
window = xmlast.XMLTagParserSchema("window", [rect, title, id_attr, class_attr, resizable], get_element_tags())
panel = xmlast.XMLTagParserSchema("panel", [rect, anchors, id_attr, class_attr], get_element_tags())

button = xmlast.XMLTagParserSchema("button", [rect, anchors, id_attr, class_attr, tooltip_attr], [])
image = xmlast.XMLTagParserSchema("image", [src, rect, anchors, id_attr, class_attr], [])
label = xmlast.XMLTagParserSchema("label", [rect, anchors, id_attr, class_attr], [])
textbox = xmlast.XMLTagParserSchema("textbox", [rect, anchors, id_attr, class_attr], [])
statusbar = xmlast.XMLTagParserSchema("statusbar", [rect, anchors, id_attr, class_attr], [])

selectionlist = xmlast.XMLTagParserSchema("selectionlist", [rect, anchors, id_attr, class_attr], ["item"])
item = xmlast.XMLTagParserSchema("item", [selected], [])

horizontalslider = xmlast.XMLTagParserSchema("horizontalslider", [rect, anchors, start, range_value, click_increment, id_attr, class_attr], [])
dropdownmenu = xmlast.XMLTagParserSchema("dropdownmenu", [rect, anchors, id_attr, class_attr], ["option"])
option = xmlast.XMLTagParserSchema("option", [starting], [])

textentryline = xmlast.XMLTagParserSchema("textentryline", [ rect, anchors, placeholder, initial, id_attr, class_attr ], [])
textentrybox = xmlast.XMLTagParserSchema("textentrybox", [rect, anchors, initial, id_attr, class_attr], [])
tooltip = xmlast.XMLTagParserSchema("tooltip", [anchors, hover_distance, id_attr, class_attr], [])

schemas: list[xmlast.XMLTagParserSchema] = [pygamegui, head, themes, theme, body, button, image, window, panel, label, textbox, statusbar, selectionlist, item, horizontalslider, dropdownmenu, option, textentryline, textentrybox, tooltip]

def parse_pygame_xml(file: str) -> xmlast.XMLNode:
    with open(file, "r") as f:
        doc = bs4.BeautifulSoup(f, "lxml-xml")
        parser = xmlast.XMLParser(schemas)
        node = parser.get_ast(doc)
        node.attrs["path"] = file
        print(node.attrs)
        return node
    raise ValueError(f'Could not open file {file}')        

