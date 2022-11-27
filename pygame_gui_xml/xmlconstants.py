confirmation = ["true", "yes", "y", "enable", "enabled", "t"]
rejection = ["false", "f", "no", "n", "disabled", "disable"]
validAnchors = ["left", "right", "top", "bottom", "center", "centerx", "centery"]

otherTags = ["body", "pygamegui", "head", "themes", "theme"]
elementTags = ["image", "button", "dropdownmenu", "horizontalslider", "window", "statusbar", "selectionlist", "worldspacehealthbar", "screenspacehealthbar", "label", "panel", "textbox", "textentryline", "textentrybox", "tooltip"]
# may add these later ["messagewindow", "consolewindow", "confirmationdialog", "colorpickerdialog", "filedialog"]
validTags = set(elementTags + otherTags)
confirmation = set(["true", "yes", "y", "enable", "enabled", "t"])
rejection = set(["false", "f", "no", "n", "disabled", "disable"])