import unittest

from htmlnode import LeafNode



class TestLeafNode(unittest.TestCase):
    def test_eq(self):
        node = LeafNode("p", "hier steht text", {"href": "www.google.de"})
        node2 = LeafNode("p", "hier steht text", {"href": "www.google.de"})
        self.assertEqual(node.to_html(), node2.to_html())


    def test_eq2(self):
        node = LeafNode("div", "hier steht text", {"href": "www.google.de", "irgendwas": "was anderes"})
        node2 = LeafNode("div", "hier steht text", {"href": "www.google.de", "irgendwas": "was anderes"})
        self.assertEqual(node.to_html(), node2.to_html())


    def test_diff(self):
        node = LeafNode("div", "hier steht text", {"href": "www.google.de", "irgendwas": "was anderes"})
        node2 = LeafNode("div", "hier steht text", {"href": "www.google.de"})
        self.assertNotEqual(node.to_html(), node2.to_html())


    def test_diff2(self):
        node = LeafNode("div", "text", {"href": "www.google.de"})
        node2 = LeafNode("p", "hier steht text", {"href": "www.google.de"})
        self.assertNotEqual(node.to_html(), node2.to_html())


    def test_diff3(self):
        node = LeafNode("p", "text", {"href": "www.google.de"})
        node2 = LeafNode("div", "text", {"href": "www.google.de"})
        self.assertNotEqual(node.to_html(), node2.to_html())


if __name__ == "__main__":
    unittest.main(unittest.main())
