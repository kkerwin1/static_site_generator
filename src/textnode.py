from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    """
    Represents the type of text.
    """

    NORMAL_TEXT = 1
    BOLD_TEXT = 2
    ITALIC_TEXT = 3
    CODE_TEXT = 4
    LINK = 5
    IMAGE = 6

class TextNode:
    def __init__(self, text, text_type, url=None):
        """
        Represents a text node.

        :param text: Represents text
        :type: str, required

        :param text_type: Represents the type of text
        :type text_type: TextType, required

        :param url: Represents a URL
        :type url: str, optional
        """

        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other):
        return (
            self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url
        )
    
    def __repr__(self):
        repr_string = f"TextNode({self.text}, {self.text_type.value}, {self.url})"
        return repr_string

def text_node_to_html_node(text_node):
    """
    Converts a TextNode to a LeafNode.

    :param text_node: TextNode to be converted
    :type text_node: TextNode, required

    :returns: A LeafNode
    :rtype: LeafNode

    :raises Exception: If not provided with a TextNode
    """
    
    match text_node.text_type:
        case TextType.NORMAL_TEXT:
            leaf_node = LeafNode(None, text_node.text)
        case TextType.BOLD_TEXT:
            leaf_node = LeafNode("b", text_node.text)
        case TextType.ITALIC_TEXT:
            leaf_node = LeafNode("i", text_node.text)
        case TextType.CODE_TEXT:
            leaf_node = LeafNode("code", text_node.text)
        case TextType.LINK:
            leaf_node = LeafNode(
                "a", text_node.text, props={"href": text_node.url}
            )
        case TextType.IMAGE:
            leaf_node = LeafNode(
                "img", "", props={
                    "src": text_node.url,
                    "alt": text_node.text,
                }
            )
        case _:
            raise Exception("not a TextNode")
    return leaf_node