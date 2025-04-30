import unittest

from src.textnode import TextNode, TextType
from src.inlinenode import (
    split_nodes_delimiter, split_multi_delimiters,
    extract_markdown_images, extract_markdown_links,
    split_nodes_image, split_nodes_links, text_to_textnodes
)

class TestSplitNodes(unittest.TestCase):
    def test_code_split(self):
        node1 = TextNode(
            "`This is code` at the beginning of the line",
            TextType.NORMAL_TEXT
        )
        node2 = TextNode(
            "This line has `a code block` in the middle of the line",
            TextType.NORMAL_TEXT
        )
        node3 = TextNode(
            "This line has `a code block at the end of the line`",
            TextType.NORMAL_TEXT
        )

        result1 = split_nodes_delimiter(
            [node1], "`", TextType.CODE_TEXT
        )
        result2 = split_nodes_delimiter(
            [node2], "`", TextType.CODE_TEXT
        )
        result3 = split_nodes_delimiter(
            [node3], "`", TextType.CODE_TEXT
        )
        result4 = split_nodes_delimiter(
            [node1, node2, node3], "`", TextType.CODE_TEXT
        )

        expected1 = [
            TextNode("This is code", TextType.CODE_TEXT),
            TextNode(
                " at the beginning of the line", 
                TextType.NORMAL_TEXT
            )
        ]
        expected2 = [
            TextNode("This line has ", TextType.NORMAL_TEXT),
            TextNode("a code block", TextType.CODE_TEXT),
            TextNode(
                " in the middle of the line", 
                TextType.NORMAL_TEXT
            )
        ]
        expected3 = [
            TextNode("This line has ", TextType.NORMAL_TEXT),
            TextNode(
                "a code block at the end of the line", 
                TextType.CODE_TEXT
            )
        ]

        expected4 = expected1.copy()
        expected4.extend(expected2)
        expected4.extend(expected3)

        self.assertListEqual(result1, expected1)
        self.assertListEqual(result2, expected2)
        self.assertListEqual(result3, expected3)
        self.assertListEqual(result4, expected4)
    
    def test_code_split_error(self):
        node1 = TextNode(
            "`This line has an unpaired code delimiter at the start",
            TextType.NORMAL_TEXT
        )
        node2 = TextNode(
            "This line has an unpaired code delimiter ` in the middle",
            TextType.NORMAL_TEXT
        )
        node3 = TextNode(
            "This line has an unpaired code delimiter at the end`",
            TextType.NORMAL_TEXT
        )

        with self.assertRaises(SyntaxError):
            split_nodes_delimiter([node1], "`", TextType.CODE_TEXT)
        with self.assertRaises(SyntaxError):
            split_nodes_delimiter([node2], "`", TextType.CODE_TEXT)
        with self.assertRaises(SyntaxError):
            split_nodes_delimiter([node3], "`", TextType.CODE_TEXT)

    def test_bold_split(self):
        node1 = TextNode(
            "**This is bold** at the beginning of the line",
            TextType.NORMAL_TEXT
        )
        node2 = TextNode(
            "This line has **a bold block** in the middle of the line",
            TextType.NORMAL_TEXT
        )
        node3 = TextNode(
            "This line has **a bold block at the end of the line**",
            TextType.NORMAL_TEXT
        )

        result1 = split_nodes_delimiter(
            [node1], "**", TextType.BOLD_TEXT
        )
        result2 = split_nodes_delimiter(
            [node2], "**", TextType.BOLD_TEXT
        )
        result3 = split_nodes_delimiter(
            [node3], "**", TextType.BOLD_TEXT
        )
        result4 = split_nodes_delimiter(
            [node1, node2, node3], "**", TextType.BOLD_TEXT
        )

        expected1 = [
            TextNode("This is bold", TextType.BOLD_TEXT),
            TextNode(
                " at the beginning of the line", 
                TextType.NORMAL_TEXT
            )
        ]
        expected2 = [
            TextNode("This line has ", TextType.NORMAL_TEXT),
            TextNode("a bold block", TextType.BOLD_TEXT),
            TextNode(
                " in the middle of the line", 
                TextType.NORMAL_TEXT
            )
        ]
        expected3 = [
            TextNode("This line has ", TextType.NORMAL_TEXT),
            TextNode(
                "a bold block at the end of the line", 
                TextType.BOLD_TEXT
            )
        ]

        expected4 = expected1.copy()
        expected4.extend(expected2)
        expected4.extend(expected3)

        self.assertListEqual(result1, expected1)
        self.assertListEqual(result2, expected2)
        self.assertListEqual(result3, expected3)
        self.assertListEqual(result4, expected4)

    def test_italic_split(self):
        node1 = TextNode(
            "_This is italic_ at the beginning of the line",
            TextType.NORMAL_TEXT
        )
        node2 = TextNode(
            "This line has _an italic block_ in the middle of the line",
            TextType.NORMAL_TEXT
        )
        node3 = TextNode(
            "This line has _an italic block at the end of the line_",
            TextType.NORMAL_TEXT
        )

        result1 = split_nodes_delimiter(
            [node1], "_", TextType.ITALIC_TEXT
        )
        result2 = split_nodes_delimiter(
            [node2], "_", TextType.ITALIC_TEXT
        )
        result3 = split_nodes_delimiter(
            [node3], "_", TextType.ITALIC_TEXT
        )
        result4 = split_nodes_delimiter(
            [node1, node2, node3], "_", TextType.ITALIC_TEXT
        )

        expected1 = [
            TextNode("This is italic", TextType.ITALIC_TEXT),
            TextNode(
                " at the beginning of the line", 
                TextType.NORMAL_TEXT
            )
        ]
        expected2 = [
            TextNode("This line has ", TextType.NORMAL_TEXT),
            TextNode("an italic block", TextType.ITALIC_TEXT),
            TextNode(
                " in the middle of the line", 
                TextType.NORMAL_TEXT
            )
        ]
        expected3 = [
            TextNode("This line has ", TextType.NORMAL_TEXT),
            TextNode(
                "an italic block at the end of the line", 
                TextType.ITALIC_TEXT
            )
        ]

        expected4 = expected1.copy()
        expected4.extend(expected2)
        expected4.extend(expected3)

        self.assertListEqual(result1, expected1)
        self.assertListEqual(result2, expected2)
        self.assertListEqual(result3, expected3)
        self.assertListEqual(result4, expected4)

class TestMultiSplitNodes(unittest.TestCase):
    def test_combo_split(self):
        node1 = TextNode(
            "**BOLD** - `CODE` - _ITALIC_", TextType.NORMAL_TEXT
        )
        node2 = TextNode(
            "`CODE` - _ITALIC_ - **BOLD**", TextType.NORMAL_TEXT
        )
        node3 = TextNode(
            "_ITALIC_ - **BOLD** - `CODE`", TextType.NORMAL_TEXT
        )

        result1 = split_multi_delimiters([node1])
        result2 = split_multi_delimiters([node2])
        result3 = split_multi_delimiters([node3])
        result4 = split_multi_delimiters([node1, node2, node3])

        expected1 = [
            TextNode("BOLD", TextType.BOLD_TEXT),
            TextNode(" - ", TextType.NORMAL_TEXT),
            TextNode("CODE", TextType.CODE_TEXT),
            TextNode(" - ", TextType.NORMAL_TEXT),
            TextNode("ITALIC", TextType.ITALIC_TEXT),
        ]
        expected2 = [
            TextNode("CODE", TextType.CODE_TEXT),
            TextNode(" - ", TextType.NORMAL_TEXT),
            TextNode("ITALIC", TextType.ITALIC_TEXT),
            TextNode(" - ", TextType.NORMAL_TEXT),
            TextNode("BOLD", TextType.BOLD_TEXT),
        ]
        expected3 = [
            TextNode("ITALIC", TextType.ITALIC_TEXT),
            TextNode(" - ", TextType.NORMAL_TEXT),
            TextNode("BOLD", TextType.BOLD_TEXT),
            TextNode(" - ", TextType.NORMAL_TEXT),
            TextNode("CODE", TextType.CODE_TEXT),
        ]

        expected4 = expected1.copy()
        expected4.extend(expected2)
        expected4.extend(expected3)

        self.assertListEqual(result1, expected1)
        self.assertListEqual(result2, expected2)
        self.assertListEqual(result3, expected3)
        self.assertListEqual(result4, expected4)

class TestImageExtraction(unittest.TestCase):
    def test_extract_markdown_images(self):
        result1 = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        result2 = extract_markdown_images(
            "![image_a](url_a) ![image_b](url_b)"
        )

        expected1 = [("image", "https://i.imgur.com/zjjcJKZ.png")]
        expected2 = [("image_a", "url_a"), ("image_b", "url_b")]

        self.assertListEqual(result1, expected1)
        self.assertListEqual(result2, expected2)

class TestLinkExtraction(unittest.TestCase):
    def test_extract_markdown_links(self):
        result = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        expected = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev")
        ]

        self.assertListEqual(result, expected)


class TestImageNodeSplit(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL_TEXT,
        )
        result = split_nodes_image([node])
        expected = [
            TextNode("This is text with an ", TextType.NORMAL_TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.NORMAL_TEXT),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
        ]
        self.assertListEqual(result, expected)


class TestLinkNodeSplit(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL_TEXT,
        )
        result = split_nodes_links([node])
        expected = [
            TextNode("This is text with a ", TextType.NORMAL_TEXT),
            TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.NORMAL_TEXT),
            TextNode("second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
        ]

        self.assertListEqual(result, expected)

class TestToNode(unittest.TestCase):
    def test_text_to_textnodes(self):
        result = text_to_textnodes(
            "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        )        
        expected = [
            TextNode("This is ", TextType.NORMAL_TEXT),
            TextNode("text", TextType.BOLD_TEXT),
            TextNode(" with an ", TextType.NORMAL_TEXT),
            TextNode("italic", TextType.ITALIC_TEXT),
            TextNode(" word and a ", TextType.NORMAL_TEXT),
            TextNode("code block", TextType.CODE_TEXT),
            TextNode(" and an ", TextType.NORMAL_TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.NORMAL_TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(result, expected)

        
if __name__ == "__main__":
    unittest.main()
