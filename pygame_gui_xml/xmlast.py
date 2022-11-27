import bs4
from typing import Generic, TypeVar, Union, Callable, Iterable, Any, TypedDict
from collections import deque
from pygame_gui_xml.xmlconstants import *


T = TypeVar("T")

def is_num(string: str) -> bool:
    try:
        float(string)
        return True
    except ValueError:
        return False

def is_bool_attr(data: str) -> bool:
    return data in rejection or data in confirmation

def is_int_str(string: str) -> bool:
    return is_num(string) and all([ char.isdigit() or char == "-" for char in string ])

def get_num_tuple_attr(tag: bs4.Tag, attrname: str, length: int, default: tuple[int | float, ...]) -> tuple[int | float, ...]:
    if attrname in tag.attrs:
        values = [ string for string in tag[attrname].split(" ") if len(string) > 0 ]
        if all([ is_num(value) for value in values ]):
            numerics = [ int(value) if is_int_str(value) else float(value) for value in values ]
            return tuple(numerics)
    return default

def get_bool_attr(data: str) -> bool:
    if data.lower() in rejection:
        return False
    elif data.lower() in confirmation:
        return True
    raise ValueError(f'Data {data} could not be casted to a boolean while fetching attribute')

def get_num_attr(data: str) -> float | int:
    if is_num(data):
        if is_int_str(data):
            return int(data)
        else:
            return float(data)
    raise ValueError(f'Could not get num from {data}')


def get_str_attr(tag: bs4.Tag, attrname: str, default: str, accepted: Iterable[str] = []) -> str:
    res = default
    
    if attrname in tag.attrs:
        if len(accepted) == 0:
            res = tag[attrname]
        elif tag[attrname] in accepted:
                res = tag[attrname]
    return res

def get_str_list(tag, attrname: str) -> list[str]:
    if attrname in tag.attrs:
        return [ string for string in tag[attrname].split(" ") if len(string) > 0 ]
    return []

class TagDetails(TypedDict):
    name: str
    attrs: dict[str, str]
    text: str
    parents: list[str]
    children: list[str]

def get_tag_details(tag: bs4.Tag) -> TagDetails:
    return {
        "name": tag.name,
        "attrs": tag.attrs,
        "text": tag.text,
        "parents": [ parent.name for parent in tag.parents ],
        "children": [ child.name for child in tag.children if isinstance(child, bs4.Tag) ]
    }


class XMLNode():
    def __init__(self, name: str, attrs: dict[str, Any], text: str, parent: Union["XMLNode", None], children: list["XMLNode"]):
        self.name = name
        self.attrs = attrs
        self.text = text
        self.parent = parent
        self.children = children

    def find(self, name: str) -> Union["XMLNode", None]:
        for child in self.children:
            if child.name == name:
                return child
        for child in self.children:
            result = child.find(name)
            if not result is None:
                return result
        return None

    def find_all(self, name: str) -> Iterable["XMLNode"]:
        found: list["XMLNode"] = [child for child in self.children if child.name == name]
        for child in self.children:
            found.extend(child.find_all(name))
        return found

    def find_all_with_attrs(self, attrs: Iterable[str]) -> Iterable["XMLNode"]:
        found: list["XMLNode"] = [child for child in self.children if all([attr in child.attrs for attr in attrs])]
        for child in self.children:
            found.extend(child.find_all_with_attrs(attrs))
        return found


    def __str__(self) -> str:
        return f'XMLNode {self.name}: {{ attrs: {self.attrs}, text: {self.text}, parent: {self.parent.name if not self.parent is None else "None"}, children: {[ child.name for child in self.children ]}    }}'

class XMLAttributeParserSchema(Generic[T]):
    def __init__(self, name: str, required: bool, parserfunc: Callable[[str], T], validator: Callable[[str], bool]):
        self.name = name
        self.type = T
        self.required = required
        self.parserfunc = parserfunc
        self.validator = validator

class XMLBoolAttributeParserSchema(XMLAttributeParserSchema[bool]):
    def __init__(self, name: str, required: bool):
        super().__init__(name, required, get_bool_attr, is_bool_attr)

class XMLStringAttributeParserSchema(XMLAttributeParserSchema[str]):
    def __init__(self, name: str, required: bool):
        super().__init__(name, required, lambda data: data, lambda _: True)

class XMLIntAttributeParserSchema(XMLAttributeParserSchema[int]):
    def __init__(self, name: str, required: bool):
        super().__init__(name, required, lambda integer: get_num_attr(integer), is_int_str)

class XMLFloatAttributeParserSchema(XMLAttributeParserSchema[float]):
    def __init__(self, name: str, required: bool):
        super().__init__(name, required, lambda num: get_num_attr(num), is_num)


class XMLTagParserSchema():
    def __init__(self, name: str, attrSchema: Iterable[XMLAttributeParserSchema], acceptedChildren: Iterable[str]):
        self.name = name
        self.attrSchema = dict([ ( schema.name, schema ) for schema in attrSchema ])
        self.acceptedChildren = set(acceptedChildren)

    def validate(self, tag: bs4.Tag):
        return all([ child.name in self.acceptedChildren for child in tag.children if isinstance(child, bs4.Tag) ]) and all([ attribute in self.attrSchema for attribute in tag.attrs.keys() ]) and all([ self.attrSchema[attribute].validator(tag[attribute]) for attribute in tag.attrs.keys() ])


class XMLParser():
    def __init__(self, tagSchemas: Iterable[XMLTagParserSchema]):
        self.tagSchemas = dict([ (tagSchema.name, tagSchema) for tagSchema in tagSchemas ])
        if not "[document]" in self.tagSchemas:
            self.tagSchemas["[document]"] = XMLTagParserSchema("[document]", [], list(self.tagSchemas.keys()) )

    def get_ast_node(self, current: bs4.Tag, parent: XMLNode | None) -> XMLNode:
        if current.name in self.tagSchemas:
            nodeAttrs: dict[str, Any] = {}
            schema = self.tagSchemas[current.name]

            if schema.validate(current):
                for attr in current.attrs:
                    if attr in schema.attrSchema:
                        if schema.attrSchema[attr].validator(current[attr]):
                            nodeAttrs[attr] = schema.attrSchema[attr].parserfunc(current[attr])
                        else:
                            raise ValueError(f'XML Parser Error: Could not validate attribute {attr} in schema for tag {get_tag_details(current)}')
                    else:
                        raise ValueError(f'XML Parser Error: Could not find attribute {attr} in schema for tag {get_tag_details(current)} ')
                text = "" if str(current.string) is None else str(current.string)
                node = XMLNode(current.name, nodeAttrs, text, parent, [])
                node.children = [ self.get_ast_node(child, node) for child in current.children if isinstance(child, bs4.Tag) ]
                return node
            else:
                raise ValueError(f'XML Parser Error: Could not validate tag {get_tag_details(current)} according to given schema')
        else:
            raise ValueError(f'XML Parser Error: Could not find tag {get_tag_details(current)} in tag schema for parser ')


    def get_ast(self, top: bs4.Tag) -> XMLNode:
        return self.get_ast_node(top, None)

vec4 = tuple[int, int, int, int]

def print_xml_node_tree(head: XMLNode):
    queue: deque[XMLNode] = deque([head])
    while len(queue) > 0:
        node = queue.pop()
        print(node)
        queue.extend(node.children)


if __name__ == "__main__":
    xml = bs4.BeautifulSoup("<panel id='3'> <name>Jacoby</name> </panel>", "lxml-xml")
    print(xml)
    id = XMLIntAttributeParserSchema("id", True)
    panel = XMLTagParserSchema("panel", [id], ["name"])
    name = XMLTagParserSchema("name", [], [])
    parser = XMLParser([panel, name])
    head = parser.get_ast(xml)
    
    print_xml_node_tree(head)