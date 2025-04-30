import unittest
from src.htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node1 = HTMLNode(tag="a", value="link", props={"href": "google.com"})
        node2 = HTMLNode(tag="img", props={
            "href": "cnn.com",
            "test": "value",
        })
        node3 = HTMLNode(props={
            "target": "value",
            "test": "value2",
            "another_test": "value3",
        })
        node4 = HTMLNode()

        self.assertEqual(node1.props_to_html(), 'href="google.com"')
        self.assertEqual(node2.props_to_html(), 'href="cnn.com" test="value"')
        self.assertEqual(node3.props_to_html(),
            'target="value" test="value2" another_test="value3"'
        )
        self.assertEqual(node4.props_to_html(), "")

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(), 
            '<a href="https://www.google.com">Click me!</a>'
        )

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
    )

if __name__ == "__main__":
    unittest.main()