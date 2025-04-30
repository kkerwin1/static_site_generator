from textnode import TextNode, TextType

import re

def split_delimiter_at_start(text, delimiter, text_type):
    """
    Called by split_nodes_delimiter() when delimiter occurs at
    beginning of text.

    :param text: Text to evaluate.
    :type text: str, required

    :param delimiter: A string delimiter
    :type delimiter: str, required

    :param text_type: TextType to convert to
    :type text_type: TextType, required

    :returns: A list of TextNodes
    :rtype: list[TextNode]

    :raises SyntaxError: If an unpaired delimiter is found
    """

    new_nodes = []
    dLength = len(delimiter)
    try:
        # Search for second delimiter
        text.index(delimiter, dLength)
    except ValueError:
        raise SyntaxError("invalid Markdown syntax: unpaired delimiter")
    
    text_list = text.split(delimiter, 2)

    # text_list[0] is an empty string in this instance
    selected_text = text_list[1]
    new_nodes.append(TextNode(selected_text, text_type))
    
    # Search stub node for any more delimiters
    stub_node = TextNode(text_list[2], TextType.NORMAL_TEXT)
    if delimiter in text_list[2]:
        split_stub_nodes = split_nodes_delimiter([stub_node], delimiter, text_type)
        new_nodes.extend(split_stub_nodes)
    else:
        new_nodes.append(stub_node)
    return new_nodes

def split_delimiter_at_end(text, delimiter, text_type):
    """
    Called by split_nodes_delimiter() when delimiter occurs at
    end of text.

    :param text: Text to evaluate.
    :type text: str, required

    :param delimiter: A string delimiter
    :type delimiter: str, required

    :param text_type: TextType to convert to
    :type text_type: TextType, required

    :returns: A list of TextNodes
    :rtype: list[TextNode]

    :raises SyntaxError: If an unpaired delimiter is found
    """

    new_nodes = []
    dLength = len(delimiter)

    # Search for second delimiter
    count = text.count(delimiter, 0, len(text)-dLength)
    if count == 0:
        raise SyntaxError("invalid Markdown syntax: unpaired delimiter")
    elif count == 1:            
        text_list = text.split(delimiter)
        new_nodes.append(TextNode(text_list[0], TextType.NORMAL_TEXT))
        new_nodes.append(TextNode(text_list[1], text_type))
    else:
        i = 0
        index = 0
        while i < count:
            index = text.index(delimiter, index, len(text)-dLength)
            i += 1
        stub_text = text[0:index]
        selected_text = text[index:(len(text)-dLength+1)]
        stub_node = TextNode(stub_text, TextType.NORMAL_TEXT)
        split_nodes = split_nodes_delimiter([stub_node])
        new_nodes.extend(split_nodes)
        selected_node = TextNode(selected_text, text_type)
        new_nodes.append(selected_node)
    return new_nodes

def split_delimiter_in_middle(text, delimiter, text_type):
    """
    Called by split_nodes_delimiter() when delimiter occurs in
    middle of text.

    :param text: Text to evaluate.
    :type text: str, required

    :param delimiter: A string delimiter
    :type delimiter: str, required

    :param text_type: TextType to convert to
    :type text_type: TextType, required

    :returns: A list of TextNodes
    :rtype: list[TextNode]

    :raises SyntaxError: If an unpaired delimiter is found
    """

    i = text.index(delimiter)
    new_nodes = []
    dLength = len(delimiter)

    try:
        text.index(delimiter, i+dLength)
    except ValueError:
        raise SyntaxError("invalid Markdown syntax: unpaired delimiter")
    
    text_list = text.split(delimiter, 2)
    first_slice = text_list[0]
    selected_text = text_list[1]
    stub_text = text_list[2]
    new_nodes.append(TextNode(first_slice, TextType.NORMAL_TEXT))
    new_nodes.append(TextNode(selected_text, text_type))
    stub_node = TextNode(stub_text, TextType.NORMAL_TEXT)
    if delimiter in stub_text:
        split_nodes = split_nodes_delimiter([stub_node], delimiter, text_type)
        new_nodes.extend(split_nodes)
    else:
        new_nodes.append(TextNode(text_list[2], TextType.NORMAL_TEXT))
    return new_nodes

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """
    Create a list of TextNodes

    :param old_nodes: A list of previously-made TextNodes, that have 
    not yet been evaluated for the presence of inline nodes
    :type old_nodes: list[TextNode], required

    :param delimiter: A string delimiter
    :type delimiter: str, required

    :param text_type: TextType to convert to
    :type text_type: TextType, required

    :returns: A list of TextNodes
    :rtype: list[TextNode]

    :raises SyntaxError: If an unpaired delimiter is found
    """

    new_nodes = []
    for old_node in old_nodes:
        text = old_node.text

        # Node already flagged as another TextType.
        # Append to new_nodes and move one to next node.
        if old_node.text_type != TextType.NORMAL_TEXT:
            new_nodes.append(old_node)
        
        # Node does not contain delimiter. Append to
        # new_nodes and move on to next node.
        elif delimiter not in text:
            new_nodes.append(old_node)

        # Line starts with delimiter, so we will only get
        # a two-member list.
        elif text.startswith(delimiter):
            node_list = split_delimiter_at_start(text, delimiter, text_type)
            new_nodes.extend(node_list)
            
        # Line ends with delimiter, so we will only get
        # a two-member list.
        elif text.endswith(delimiter):
            node_list = split_delimiter_at_end(text, delimiter, text_type)
            new_nodes.extend(node_list)

        # Delimiter occurs in the middle of the line,
        # so we will get a three-member list.
        else:
            node_list = split_delimiter_in_middle(text, delimiter, text_type)
            new_nodes.extend(node_list)

    return new_nodes

def split_multi_delimiters(old_nodes):
    """
    Iterate over old_nodes for all delimiters. For testing purposes.

    :param old_nodes: A list of previously-made TextNodes, that have 
    not yet been evaluated for the presence of inline nodes
    :type old_nodes: list[TextNode], required

    :returns: A list of TextNodes
    :rtype: list[TextNode]
    """

    delimiter_dict = {
        "**": TextType.BOLD_TEXT,
        "_": TextType.ITALIC_TEXT,
        "`": TextType.CODE_TEXT,
    }

    for delimiter in delimiter_dict:
        text_type = delimiter_dict[delimiter]
        old_nodes = split_nodes_delimiter(old_nodes, delimiter, text_type)
    return old_nodes

def split_nodes_image(old_nodes):
    """
    Iterate over old_nodes. Convert nodes of TextType.NORMAL_TEXT
    to nodes of TextType.IMAGE

    :param old_nodes: A list of previously-made TextNodes, that have
    not yet been evaluated for the presence of inline image nodes
    :type old_nodes: list[TextNode], required

    :returns: A list of TextNodes of type TextType.IMAGE
    :rtype: list[TextNode]
    """

    new_nodes = []
    for old_node in old_nodes:
        text = old_node.text

        # Node already flagged as another TextType.
        # Append to new_nodes and move on to next node.
        if old_node.text_type != TextType.NORMAL_TEXT:
            new_nodes.append(old_node)
            continue
        
        # "!" not in text; therefore not a Markdown image tag
        # Append to new_nodes and move on to next node.
        if "!" not in text:
            new_nodes.append(old_node)
            continue
        
        while len(text) > 0:
            sections = []
            try:
                _match = extract_markdown_images(text)[0]
                alt_text = _match[0]
                url = _match[1]
                sections = text.split(f"![{alt_text}]({url})")
                
            # _match not found in text. Process text into text_noe
            except IndexError:
                text_node = TextNode(text, TextType.NORMAL_TEXT)
                new_nodes.append(text_node)

                # End while loop with empty text string
                text = ""
                continue

            # _match occurred at beginning of text;
            # append TextNode for _match to new_nodes list
            if len(sections[0]) == 0:
                image_node = TextNode(alt_text, TextType.IMAGE, url)
                new_nodes.append(image_node)

                # Re-run while loop with remaining text
                text = sections[1]
                
            # _match occurred in middle of line
            else:
                # Create text_node for first chunk
                text_node = TextNode(sections[0], TextType.NORMAL_TEXT)
                new_nodes.append(text_node)

                # Create image_node for second chunk
                image_node = TextNode(alt_text, TextType.IMAGE, url)
                new_nodes.append(image_node)
                    
                # Re-run while loop with remaining text
                try:
                    text = sections[1]
                except IndexError:
                    # _match occurred at end of line
                    # End while loop with empty text string
                    text = ""
    return new_nodes

def split_nodes_links(old_nodes):
    """
    Iterate over old_nodes. Convert nodes of TextType.NORMAL_TEXT
    to nodes of TextType.LINK

    :param old_nodes: A list of previously-made TextNodes, that have
    not yet been evaluated for the presence of inline link nodes
    :type old_nodes: list[TextNode], required

    :returns: A list of TextNodes of type TextType.LINK
    :rtype: list[TextNode]
    """

    new_nodes = []
    for old_node in old_nodes:
        text = old_node.text

        # Node already flagged as another TextType.
        # Append to new_nodes and move one to next node.
        if old_node.text_type != TextType.NORMAL_TEXT:
            new_nodes.append(old_node)
            continue
        
        # "[" not in text; therefore not a Markdown link tag
        # Append to new_nodes and move on to next node.
        if "[" not in text:
            new_nodes.append(old_node)
            continue

        while len(text) > 0:
            sections = []
            try:
                _match = extract_markdown_links(text)[0]
                link_text = _match[0]
                url = _match[1]
                sections = text.split(f"[{link_text}]({url})")
                
            # _match not found in text. Process text into text_node
            except IndexError:
                text_node = TextNode(text, TextType.NORMAL_TEXT)
                new_nodes.append(text_node)

                # End while loop with empty text string
                text = ""
                continue

            # _match occurred at beginning of text;
            # append TextNode for _match to new_nodes list
            if len(sections[0]) == 0:
                link_node = TextNode(link_text, TextType.LINK, url)
                new_nodes.append(link_node)

                # Re-run while loop with remaining text
                text = sections[1]
                
            # _match occurred in middle or at end of line
            else:
                # Create text_node for first chunk
                text_node = TextNode(sections[0], TextType.NORMAL_TEXT)
                new_nodes.append(text_node)

                # Create link_node for second chunk
                link_node = TextNode(link_text, TextType.LINK, url)
                new_nodes.append(link_node)
                    
                # Re-run while loop with remaining text
                try:
                    text = sections[1]
                except IndexError:
                    # _match occurred at end of line
                    # End while loop with empty text string
                    text = ""
    return new_nodes

def extract_markdown_images(text):
    """
    Extract images from Markdown text.

    :param text: Markdown text to be parsed.
    :type text: str, required

    :returns: A list of tuples, each tuple containing the image's 
    alt_text and url
    :rtype: list[(str, str)]
    """

    regex = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(regex, text)
    return matches

def extract_markdown_links(text):
    """
    Extract links from Markdown text.

    :param text: Markdown text to be parsed.
    :type text: str, required

    :returns: A list of tuples, each tuple containing the links's 
    text and url
    :rtype: list[(str, str)]
    """

    regex = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(regex, text)
    return matches

def text_to_textnodes(text):
    """
    Convert raw text to appropriate TextNodes.

    :param text: Raw text to convert
    :type text: str

    :returns: A list of nodes
    :rtype: list[TextNode]
    """
    
    node_list = [TextNode(text, TextType.NORMAL_TEXT)]
    node_list = split_multi_delimiters(node_list)
    node_list = split_nodes_image(node_list)
    node_list = split_nodes_links(node_list)
    return node_list