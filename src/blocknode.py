from enum import Enum
from htmlnode import ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
from inlinenode import text_to_textnodes

import re

heading_regex = re.compile(r"^(#+) (.*)$")
ordered_list_regex = re.compile(r"^(\d+)\. (.*)$")

class BlockType(Enum):
    PARAGRAPH = 1
    HEADING = 2
    CODE = 3
    QUOTE = 4
    UNORDERED_LIST = 5
    ORDERED_LIST = 6

def markdown_to_blocks(markdown):
    """
    Converts a string of raw markdown text to a list of strings.

    :param markdown: Raw markdown string
    :type markdown: str, required

    :returns: A list of strings, each string representing a block
    :rtype: list[str]
    """

    blocks = markdown.split("\n\n")
    new_blocks = []
    for block in blocks:
        # strip leading/trailing whitespace
        block = block.strip()
        if block != "":
            new_blocks.append(block)
    return new_blocks

def block_to_block_type(block):
    """
    Provided a block, return the BlockType.

    :param block: A string representing a block
    :type block: str, required

    :returns: A BlockType
    :rtype: BlockType

    :raises SyntaxError: If Markdown syntax is invalid
    """
    
    line_list = block.split("\n")
    first_char = line_list[0][0]

    match first_char:
        # Heading
        case "#":
            hashes_string = heading_regex.match(block)[1]
            hash_count = hashes_string.count("#")
            if hash_count > 6:
                raise SyntaxError("Invalid Markdown Syntax: more than six # characters in a heading")
            elif not block[hash_count].isspace():
                raise SyntaxError("Invalid Markdown Syntax: First character after string of #'s in a heading must be a space")
            else:
                return BlockType.HEADING
        
        # Code
        case "`":
            # Confirm that this is a code block: three "`" characters
            if block.find("```") == 0:
                # Confirm the presence of closing tags
                if block.find("```", 3) > -1:
                    return BlockType.CODE
                else:
                    raise SyntaxError('Invalid Markdown Syntax: no closing code tags ("```")')
            # Not a code block: doesn't have three "`" characters
            else:
                return BlockType.PARAGRAPH
    
        # Quote
        case ">":
            for line in line_list:
                if line[0] != ">":
                    raise SyntaxError('Invalid Markdown Syntax: all lines in a quote block must begin with a ">" character')
            return BlockType.QUOTE
        
        # Unordered List
        case "-":
            for line in line_list:
                if line[0] != "-":
                    raise SyntaxError('Invalid Markdown Syntax: all lines in an unordered list block must begin with a "-" character')
                elif not line[1].isspace():
                    raise SyntaxError('Invalid Markdown Syntax: all lines in an unordered list block must have a space after the "-" character')
            return BlockType.UNORDERED_LIST
        
        case _:
            # Ordered List
            if first_char == "1":
                line_int = 1
                for line in line_list:
                    _match = ordered_list_regex.match(line)
                    if not _match:
                        raise SyntaxError('Invalid Markdown Syntax: invalid ordered list syntax')
                    elif (int(_match[1]) != line_int):
                        raise SyntaxError("Invalid Markdown Syntax: Ordered list ordinal must increment by precisely 1 on each line")
                    else:
                        line_int += 1
                return BlockType.ORDERED_LIST
                    
            # Paragraph
            else:
                return BlockType.PARAGRAPH

def text_to_children(text):
    """
    Given a text block, first parse for TextNodes, then convert
    each TextNode to a LeafNode(HTMLNode). Return the list of HTMLNodes.

    :param text: A text string block
    :type: str, required

    :returns: A list of child LeafNodes
    :rtype: list[LeafNode]
    """

    text = text.replace("\n", " ")
    child_list = []
    text_node_list = text_to_textnodes(text)
    for text_node in text_node_list:
        child_html_node = text_node_to_html_node(text_node)
        child_list.append(child_html_node)
    return child_list

def markdown_to_html_node(text):
    """
    Given text from a markdown file, generate an HTMLNode tree.

    :param text: A full markdown file
    :type text: str, required

    :returns: An HTMLNode tree
    :rtype: HTMLNode
    """

    block_node_list = []
    blocks = markdown_to_blocks(text)
    for block in blocks:
        block_type = block_to_block_type(block)

        match block_type:
            case BlockType.PARAGRAPH:
                child_nodes = text_to_children(block)
                paragraph_node = ParentNode("p", child_nodes)
                block_node_list.append(paragraph_node)

            case BlockType.HEADING:
                text_list = block.split()
                hashes = text_list[0]
                hash_num = len(hashes)
                tag = f"h{hash_num}"
                block = block.lstrip("#").lstrip()
                child_nodes = text_to_children(block)
                heading_node = ParentNode(tag, child_nodes)
                block_node_list.append(heading_node)
            
            case BlockType.CODE:
                lstripped = block.lstrip("`").lstrip()
                text = lstripped.rstrip("`").rstrip()
                code_text_node = TextNode(text, TextType.CODE_TEXT)
                code_node = text_node_to_html_node(code_text_node)
                pre_node = ParentNode("pre", [code_node])
                block_node_list.append(pre_node)

            case BlockType.QUOTE:
                quote_text = ""
                line_list = block.split("\n")
                for i in range(0, len(line_list)):
                    line = line_list[i]
                    line_text = line.lstrip(">").lstrip()
                    quote_text += line_text
                    # Add line breaks between all lines
                    # (except after the last line)
                    if i <= len(line_list)-2:
                        quote_text += "<br>"
                child_nodes = text_to_children(quote_text)
                quote_node = ParentNode("blockquote", child_nodes)
                block_node_list.append(quote_node)

            case BlockType.UNORDERED_LIST:
                li_node_list = []
                line_list = block.split("\n")
                for line in line_list:
                    line_text = line.lstrip("-").lstrip()
                    line_nodes = text_to_children(line_text)
                    li_node = ParentNode("li", line_nodes)
                    li_node_list.append(li_node)
                ul_node = ParentNode("ul", li_node_list)
                block_node_list.append(ul_node)

            case BlockType.ORDERED_LIST:
                li_node_list = []
                line_list = block.split("\n")
                for line in line_list:
                    text = ordered_list_regex.match(line)[2]
                    line_nodes = text_to_children(text)
                    li_node = ParentNode("li", line_nodes)
                    li_node_list.append(li_node)
                ol_node = ParentNode("ol", li_node_list)
                block_node_list.append(ol_node)
                
    top_level_node = ParentNode("div", block_node_list)
    return top_level_node

