import unittest
from main import text_node_to_html_node

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)


    def test_eq2(self):
        node = TextNode("This is an image", TextType.IMAGE)
        node2 = TextNode("This is an image", TextType.IMAGE)
        self.assertEqual(node, node2)


    def test_diff(self):
        node = TextNode("This is a link", TextType.LINK, "http://www.google.de/")
        node2 = TextNode("This is a link", TextType.ITALIC)
        self.assertNotEqual(node, node2)


    def test_diff2(self):
        node = TextNode("This is a link", TextType.LINK, "http://www.google.de/")
        node2 = TextNode("This is a text", TextType.LINK, "http://www.google.de/")
        self.assertNotEqual(node, node2)


    def test_diff3(self):
        node = TextNode("This is a link", TextType.LINK, "http://www.google.de/")
        node2 = TextNode("This is a link", TextType.TEXT, "http://www.google.de/")
        self.assertNotEqual(node, node2)

    

    def test_text(self):
        node = TextNode("text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "text node")


    def test_text2(self):
        node = TextNode("link node", TextType.LINK, url="www.test.de")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.props, {"href": "www.test.de"})


    def test_text3(self):
        node = TextNode("italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "italic node")


if __name__ == "__main__":
    unittest.main(unittest.main())      
