import bs4
from typing import Generic, TypeVar, Union, Callable, Iterable, Any, TypedDict
from collections import deque

confirmation = ["true", "yes", "y", "enable", "enabled", "t"]
rejection = ["false", "f", "no", "n", "disabled", "disable"]

T = TypeVar("T")

def is_num(string: str) -> bool:
    try:
        float(string)
        return True
    except ValueError:
        return False

def is_int_str(string: str) -> bool:
    return is_num(string) and all([ char.isdigit() or char == "-" for char in string ])

def get_num_tuple_attr(tag: bs4.Tag, attrname: str, length: int, default: tuple[int | float, ...]) -> tuple[int | float, ...]:
    if attrname in tag.attrs:
        values = [ string for string in tag[attrname].split(" ") if len(string) > 0 ]
        if all([ is_num(value) for value in values ]):
            numerics = [ int(value) if is_int_str(value) else float(value) for value in values ]
            return tuple(numerics)
    return default

def get_bool_attr(tag: bs4.Tag, attrname: str, default: bool) -> bool:
    res = default
    
    if attrname in tag.attrs:
        if default == True:
            res = tag[attrname].lower() in rejection
        elif default == False:
            res = tag[attrname].lower() in confirmation
    return res

def get_num_attr(tag: bs4.Tag, attrname: str, default: float | int) -> float | int:
    if attrname in tag.attrs:
        if is_num(tag[attrname]):
            if is_int_str(tag[attrname]):
                return int(tag[attrname])
            else:
                return float(tag[attrname])
    return default


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

    def __str__(self) -> str:
        return f'XMLNode {self.name}: {{ attrs: {self.attrs}, text: {self.text}, parent: {self.parent.name if not self.parent == None else "None"}, children: {[ child.name for child in self.children ]}    }}'

class XMLAttributeParserSchema(Generic[T]):
    def __init__(self, name: str, required: bool, default: T | None, parserfunc: Callable[[str], T], validator: Callable[[str], bool]):
        self.name = name
        self.type = T
        self.required = required
        self.default = default
        self.parserfunc = parserfunc
        self.validator = validator


class XMLTagParserSchema():
    def __init__(self, name: str, attrSchema: Iterable[XMLAttributeParserSchema], acceptedChildren: Iterable[str]):
        self.name = name
        self.attrSchema = dict([ ( schema.name, schema ) for schema in attrSchema ])
        self.acceptedChildren = set(acceptedChildren)

    def validate(self, tag: bs4.Tag):
        return all([ child.name in self.acceptedChildren for child in tag.children if isinstance(child, bs4.Tag) ]) and all([ attribute in self.attrSchema for attribute in tag.attrs.keys() ]) and all([ self.attrSchema[attribute].validator(tag[attribute]) for attribute in tag.attrs.keys() ])

# XMLAttributeParserSchema[tuple[int, int, int, int]]("rect", True, None, get_tag_rect)
# XMLAttributeParserSchema[int]()
# XMLTagParserSchema("panel", )


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
                node = XMLNode(current.name, nodeAttrs, current.text, parent, [])
                node.children = [ self.get_ast_node(child, node) for child in current.children if isinstance(child, bs4.Tag) ]
                return node
            else:
                raise ValueError(f'XML Parser Error: Could not validate tag {get_tag_details(current)} according to given schema')
        else:
            raise ValueError(f'XML Parser Error: Could not find tag {get_tag_details(current)} in tag schema for parser ')


    def get_ast(self, top: bs4.Tag) -> XMLNode:
        return self.get_ast_node(top, None)

vec4 = tuple[int, int, int, int]

def validate_rect(data: str) -> bool:
    print("Validate Rect Data: ", data)
    return all([ is_num(string) for string in data.split(" ") ]) and len(data.split(" ")) == 4

def get_tag_rect(data: str) -> vec4:
    splitted = data.split(" ")
    if all([ is_num(splitstring) for splitstring in splitted]):
        rect = [float(data) for data in splitted]
        datapoints = len(rect)
        if datapoints == 4:
            return tuple(rect)
    raise ValueError(f'Could not parse rect data {data}')


if __name__ == "__main__":
    xml = bs4.BeautifulSoup("<panel rect='0 0 100 100'> <name>Jacoby</name> </panel>", "lxml-xml")
    print(xml)
    rect = XMLAttributeParserSchema[vec4]("rect", True, None, get_tag_rect, validate_rect)
    panel = XMLTagParserSchema("panel", [rect], ["name"])
    name = XMLTagParserSchema("name", [], [])
    parser = XMLParser([panel, name])
    head = parser.get_ast(xml)
    
    queue: deque[XMLNode] = deque([head])
    while len(queue) > 0:
        node = queue.pop()
        print(node)
        queue.extend(node.children)