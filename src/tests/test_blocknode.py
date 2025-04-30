import unittest

from src.blocknode import (
    markdown_to_blocks, block_to_block_type, text_to_children, markdown_to_html_node
)

from src.htmlnode import LeafNode
from src.blocknode import BlockType

class TestBlocknode(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        
        result = markdown_to_blocks(md)
        expected = [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ]

        self.assertListEqual(result, expected)

class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        text1 = "### test"
        result1 = block_to_block_type(text1)
        expected1 = BlockType.HEADING
        self.assertEqual(result1, expected1)

        text2 = "######## test"
        with self.assertRaises(SyntaxError):
            block_to_block_type(text2)
        
        text3 = "###test"
        with self.assertRaises(SyntaxError):
            block_to_block_type(text3)
    
    def test_code(self):
        text1 = [
            "```",
            "some code",
            "```"
        ]
        block1 = "\n".join(text1)
        result1 = block_to_block_type(block1)
        expected1 = BlockType.CODE
        self.assertEqual(result1, expected1)

        text2 = [
            "```",
            "some code",
        ]
        block2 = "\n".join(text2)
        with self.assertRaises(SyntaxError):
            block_to_block_type(block2)
        
        block3 = "`some not code`"
        result3 = block_to_block_type(block3)
        expected3 = BlockType.PARAGRAPH
        self.assertEqual(result3, expected3)
    
    def test_quote(self):
        text1 = [
            "> one",
            "> two",
            "> three",
        ]
        block1 = "\n".join(text1)
        result1 = block_to_block_type(block1)
        expected1 = BlockType.QUOTE
        self.assertEqual(result1, expected1)

        text2 = [
            "> one",
            "two",
            "> three",
        ]
        block2 = "\n".join(text2)
        with self.assertRaises(SyntaxError):
            block_to_block_type(block2)
        
    def test_unordered_list(self):
        text1 = [
            "- one",
            "- two",
            "- three",
        ]
        block1 = "\n".join(text1)
        result1 = block_to_block_type(block1)
        expected1 = BlockType.UNORDERED_LIST
        self.assertEqual(result1, expected1)

        text2 = [
            "- one",
            "-two",
            "- three",
        ]
        block2 = "\n".join(text2)
        with self.assertRaises(SyntaxError):
            block_to_block_type(block2)
        
        text3 = [
            "- one",
            "two",
            "- three",
        ]
        block3 = "\n".join(text3)
        with self.assertRaises(SyntaxError):
            block_to_block_type(block3)
    
    def test_ordered_list(self):
        text1 = [
            "1. one",
            "2. two",
            "3. three",
            "4. four",
            "5. five",
            "6. six",
            "7. seven",
            "8. eight",
            "9. nine",
            "10. ten",
        ]
        block1 = "\n".join(text1)
        result1 = block_to_block_type(block1)
        expected1 = BlockType.ORDERED_LIST
        self.assertEqual(result1, expected1)

        text2 = [
            "1. one",
            "2. two",
            "3. three",
            "4. four",
            "5. five",
            "6. six",
            "7. seven",
            "8. eight",
            "9. nine",
            "10. ten",
            "12. twelve"
        ]
        block2 = "\n".join(text2)
        with self.assertRaises(SyntaxError):
            block_to_block_type(block2)
        
        text3 = [
            "1. one",
            "2. two",
            "3. three",
            "4. four",
            "5. five",
            "6. six",
            "7. seven",
            "8. eight",
            "9. nine",
            "ten",
        ]
        block3 = "\n".join(text3)
        with self.assertRaises(SyntaxError):
            block_to_block_type(block3)
        
        text4 = [
            "1. one",
            "2. two",
            "3. three",
            "4. four",
            "5. five",
            "6. six",
            "7. seven",
            "8. eight",
            "9. nine",
            "10 ten",
        ]
        block4 = "\n".join(text4)
        with self.assertRaises(SyntaxError):
            block_to_block_type(block4)
    
    def test_paragraph(self):
        text = [
            "this is",
            "a",
            "paragraph",
        ]
        block = "\n".join(text)
        result = block_to_block_type(block)
        expected = BlockType.PARAGRAPH
        self.assertEqual(result, expected)

class TestTextToChildren(unittest.TestCase):
    def test_normal_text(self):
        result = text_to_children("This is a text node")[0]
        expected = LeafNode(None, "This is a text node")
        self.assertEqual(result.tag, expected.tag)
        self.assertEqual(result.value, expected.value)
        self.assertEqual(result.props, expected.props)
    
    def test_bold_text(self):
        result = text_to_children("**This is a bold node**")[0]
        expected = LeafNode("b", "This is a bold node")
        self.assertEqual(result.tag, expected.tag)
        self.assertEqual(result.value, expected.value)
        self.assertEqual(result.props, expected.props)
    
    def test_italic_text(self):
        result = text_to_children("_This is an italic node_")[0]
        expected = LeafNode("i", "This is an italic node")
        self.assertEqual(result.tag, expected.tag)
        self.assertEqual(result.value, expected.value)
        self.assertEqual(result.props, expected.props)
    
    def test_link_text(self):
        result = text_to_children("[This is a link node](url)")[0]
        expected = LeafNode("a", "This is a link node", props={"href": "url"})
        self.assertEqual(result.tag, expected.tag)
        self.assertEqual(result.value, expected.value)
        self.assertEqual(result.props, expected.props)
    
    def test_code_text(self):
        result = text_to_children("`This is a code node`")[0]
        expected = LeafNode("code", "This is a code node")
        self.assertEqual(result.tag, expected.tag)
        self.assertEqual(result.value, expected.value)
        self.assertEqual(result.props, expected.props)
    
    def test_image_text(self):
        result = text_to_children("![This is an image node](url)")[0]
        expected = LeafNode("img", "", {"src": "url", "alt": "This is an image node"})
        self.assertEqual(result.tag, expected.tag)
        self.assertEqual(result.value, expected.value)
        self.assertEqual(result.props, expected.props)

class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_paragraphs(self):
        md_list = [
            "This is **bolded** paragraph",
            "text in a p",
            "tag here",
            "",
            "This is another paragraph with _italic_ text and `code` here",
        ]

        md = "\n".join(md_list)

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )
    
    def test_comprehensive(self):
        md_list = [
            "# H1 Tag",
            "",
            "## H2 Tag",
            "",
            "### H3 Tag",
            "",
            "#### H4 Tag",
            "",
            "##### H5 Tag",
            "",
            "###### H6 Tag",
            "",
            "This is a paragraph with **bold** and _italic_ text",
            "",
            "This is a paragraph with an inline `code` tag",
            "",
            "```",
            "This is a code block",
            "```",
            "",
            "> This is a quote",
            "> block with more than one line",
            "",
            "An unordered list appears below:",
            "",
            "- first",
            "- second",
            "- third",
            "",
            "An ordered list appears below:",
            "",
            "1. first",
            "2. second",
            "3. third",
            "",
            "The end",
        ]

        md = "\n".join(md_list)
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = [
            "<div><h1>H1 Tag</h1><h2>H2 Tag</h2><h3>H3 Tag</h3><h4>H4 Tag</h4><h5>H5 Tag</h5><h6>H6 Tag</h6><p>This is a paragraph with <b>bold</b> and <i>italic</i> text</p><p>This is a paragraph with an inline <code>code</code> tag</p><pre><code>This is a code block</code></pre><blockquote>This is a quote<br>block with more than one line</blockquote><p>An unordered list appears below:</p><ul><li>first</li><li>second</li><li>third</li></ul><p>An ordered list appears below:</p><ol><li>first</li><li>second</li><li>third</li></ol><p>The end</p></div>",
        ]
        expected = "\n".join(expected)
        print(expected)
        self.assertEqual(html, expected)