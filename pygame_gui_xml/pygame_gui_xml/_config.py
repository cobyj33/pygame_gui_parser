
_validAnchors = ["left", "right", "top", "bottom", "center", "centerx", "centery"]
_otherTags = ["body", "pygamegui", "head", "themes", "theme"]
_elementTags = ["image", "button", "dropdownmenu", "horizontalslider", "window", "statusbar", "selectionlist", "worldspacehealthbar", "screenspacehealthbar", "label", "panel", "textbox", "textentryline", "textentrybox", "tooltip"]
# may add these later ["messagewindow", "consolewindow", "confirmationdialog", "colorpickerdialog", "filedialog"]
_validTags = set(_elementTags + _otherTags)

def is_valid_tag(strdata: str):
    return strdata in _validTags

def is_element_tag(strdata: str):
    return strdata in _elementTags

def is_non_element_tag(strdata: str):
    return strdata in _otherTags

def is_valid_anchor(strdata: str):
    return strdata in _validAnchors

def get_valid_anchor_tags():
    return list(_validAnchors)

def get_element_tags():
    return list(_elementTags)

def get_non_element_tags():
    return list(_otherTags)

def get_valid_tags():
    return list(_validTags)