import unittest

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


if __name__ == "__main__":
    unittest.main(unittest.main())
