import pygame
import pygame_gui
import pygame_gui_xml.xmlast as xmlast
from typing import Callable
import warnings

# Basically, there are some types when it comes to elements, containers


class GUITreeElement():
    def __init__(self, elementName: str):
        self._elementName = elementName
        self._container: GUITreeElement | None = None
        self._window: GUITreeElement | None = None
        self._parent: GUITreeElement | None = None
        self._children = list[GUITreeElement] = []
        self._events: dict[pygame.event.Event, dict[str, Callable]] = {}
        self._bindedevents: dict[str, pygame.event.Event] = {}

    def bind_event(self, _id: str, event: pygame.event.Event):
        if _id in self._events:
            warnings.warn("Overwriting binded user event " + _id + ", already present in GUI Element", UserWarning)

        if event in self._events:
            self._events[event][_id] = event
        else:
            self._events[event] = {_id: event}
        self._bindedevents[_id] = event

    def unbind_event(self, _id: str):
        if _id in self._bindedevents:
            eventType = self._bindedevents[_id]
            del self._events[eventType][_id]
            del self._bindedevents[_id]

class GUITree():
    """Think of it as the DOM Tree"""
    def __init__(self, node: xmlast.XMLNode):
        self._id_dict: dict[str, list[pygame_gui.core.UIElement]] = {}
        self._class_dict: dict[str, list[pygame_gui.core.UIElement]] = {}

    def get_element_by_object_id(self, objID: pygame_gui.core.ObjectID) -> list[pygame_gui.core.UIElement]:
        return [ elem for elem in self.get_element_by_class(objID.class_id) if elem in self.get_element_by_id(objID.object_id) ] 

    def get_element_by_class(self, _class: str) -> list[pygame_gui.core.UIElement]:
        return self._class_dict.get(_class) or []
    
    def get_element_by_id(self, _id: str) -> list[pygame_gui.core.UIElement]:
        return self._id_dict.get(_id) or []