import enum
from typing import TypedDict

class GUIElementTypes(enum.Flag):
    CONTAINER = enum.auto()
    WINDOW = enum.auto()

class ElementTagMetaData(TypedDict):
    elementType: GUIElementTypes


_validAnchors: list[str] = ["left", "right", "top", "bottom", "center", "centerx", "centery"]
_otherTags: list[str] = ["body", "pygamegui", "head", "themes", "theme"]
_elementTags: dict[str, ElementTagMetaData] = { 
 "image": {
    "elementType": GUIElementTypes.CONTAINER & GUIElementTypes.WINDOW
 },
 "button":  {},
 "dropdownmenu":  {},
 "horizontalslider":  {},
 "window":  {},
 "statusbar":  {},
 "selectionlist":  {},
 "worldspacehealthbar":  {}, 
 "screenspacehealthbar":  {},
 "label":  {},
 "panel":  {},
 "textbox":  {},
 "textentryline":  {}, 
 "textentrybox":  {},
 "tooltip":  {}
}
# may add these later ["messagewindow", "consolewindow", "confirmationdialog", "colorpickerdialog", "filedialog"]
_validTags: set[str] = set[str](list(_elementTags.keys()) + _otherTags)

def is_valid_tag(strdata: str) -> bool:
    return strdata in _validTags

def is_element_tag(strdata: str) -> bool:
    return strdata in _elementTags

def is_non_element_tag(strdata: str) -> bool:
    return strdata in _otherTags

def is_valid_anchor(strdata: str) -> bool:
    return strdata in _validAnchors

def get_valid_anchor_tags() -> list[str]:
    return list(_validAnchors)

def get_element_tags() -> list[str]:
    return list(_elementTags)

def get_non_element_tags() -> list[str]:
    return list(_otherTags)

def get_valid_tags() -> list[str]:
    return list(_validTags)