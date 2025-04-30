class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        """
        Object representing an HTML node.

        :param tag: Represents the HTML tag name (eg. "p", "a", "h1", etc)
        :type tag: str, optional

        :param value: Represents the value of the HTML tag (eg. the text inside a paragraph)
        :type value: str, optional

        :param children: Represents children of this node
        :type children: list[HTMLNode], optional

        :param props: Represents the attributes of the HTML tag (eg. a link <a> tag might have {"href": "www.google.com"})
        :type props: dict{str: str}, optional
        """

        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
        self.parent = None
    
    def __repr__(self):
        repr_string = f'{self.__class__.__name__}("{self.tag}", "{self.value}", "{self.children}", "{self.props}")'
        return repr_string
    
    def to_html(self):
        """
        Function to convert this node to HTML. Implemented by child classes.

        :raises NotImplementedError: Implemented by child classes
        """

        raise NotImplementedError
    
    def props_to_html(self):
        """
        Function to convert self.props in HTML.
        
        :returns: string representation of self.props
        :rtype: str
        """

        props_string = ""
        if self.props:
            item_list = list(self.props.items())
            for i in range(0, len(item_list)):
                item = item_list[i]
                attribute, value = item
                if i == len(self.props.items())-1:
                    # last item in list; no space after item
                    item_string = f'{attribute}="{value}"'
                else:
                    # not last item in list; include space after item
                    item_string = f'{attribute}="{value}" '
                props_string += item_string
        return props_string
    
    def set_parent(self, parent):
        """
        Set the parent of this node.

        :param parent: An HTMLNode object that is the parent of this node.
        :type parent: ParentNode, required
        """

        self.parent = parent
    
    def is_child(self):
        """
        :returns: Boolean representing whether this node is the child of another node.
        :rtype: bool
        """

        if self.parent:
            return True
        else:
            return False

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        """
        Represents an HTMLNode without any children.

        :param tag: Reepresents the HTML tag name (eg. "p", "a", "h1", etc)
        :type tag: str, required

        :param value: Represents the value of the HTML tag (eg. the text inside a paragraph)
        :type value: str, required

        :param props: Represents the attributes of the HTML tag (eg. a link <a> tag might have {"href": "www.google.com"})
        :type props: dict{str: str}, optional
        """

        self.tag = tag
        self.value = value
        self.props = props

        super().__init__(tag, value, None, props)

    def to_html(self):
        """
        Convert node to HTML code.

        :returns: A string representing the node in HTML
        :rtype: str
        """

        if not self.tag:
            html_string = self.value
        elif self.props:
            props_string = self.props_to_html()
            html_string = f'<{self.tag} {props_string}>{self.value}</{self.tag}>'
        else:
            html_string = f'<{self.tag}>{self.value}</{self.tag}>'
        return html_string

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        """
        Represents an HTMLNode containing children.

        :param tag: Represents the HTML tag name (eg. "p", "a", "h1", etc)
        :type tag: str, required

        :param children: Represents children of this node
        :type children: list[HTMLNode], required

        :param props: Represents the attributes of the HTML tag (eg. a link <a> tag might have {"href": "www.google.com"})
        :type props: dict{str: str}, optional
        """

        self.tag = tag
        self.children = children
        self.props = props

        super().__init__(tag, None, children, props)

        for child in self.children:
            child.set_parent(self)
    
    def to_html(self):
        """
        Converts node and children to HTML.

        :raises ValueError: If node does not possess a value or children.

        :returns: string representing HTML of self and children.
        :rtype: str
        """

        if not self.tag:
            raise ValueError
        if not self.children:
            raise ValueError("ParentNode does not possess any children")
        
        html_string = ""
        if self.props:
            props_string = self.props_to_html()
            html_string = f'<{self.tag} {props_string}>'
            for child in self.children:
                html_string += child.to_html()
            html_string += f'</{self.tag}>'
        else:
            html_string = f'<{self.tag}>'
            for child in self.children:
                html_string += child.to_html()
            html_string += f'</{self.tag}>'
        return html_string
