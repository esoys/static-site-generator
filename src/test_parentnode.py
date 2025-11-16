
import unittest

from htmlnode import LeafNode, ParentNode



class TestParentNode(unittest.TestCase):
    def test_eq(self):
        child_node = LeafNode("p", "hier steht text", {"href": "www.google.de"})
        parent_node = ParentNode("p", [child_node], {"href": "www.google.de"})
        self.assertEqual(parent_node.to_html(), '<p href="www.google.de"><p href="www.google.de">hier steht text</p></p>')


    def test_eq2(self):
        grandchild_node = LeafNode("span", "grandchild")
        child_node = ParentNode("div", [grandchild_node],{"href": "www.google.de", "irgendwas": "was anderes"})
        parent_node = ParentNode("div", [child_node]) 
        self.assertEqual(parent_node.to_html(), '<div><div href="www.google.de" irgendwas="was anderes"><span>grandchild</span></div></div>')


    def test_err1(self):
        parent_node = ParentNode("p", [])
        self.assertRaises(ValueError, parent_node.to_html) 


    def test_err2(self):
        child_node = LeafNode("span", "foo", {"type": "button"})
        parent_node = ParentNode(None, [child_node])
        self.assertRaises(ValueError, parent_node.to_html)


    def test_err3(self):
        child_node = LeafNode("span", "foo", {"type": "button"})
        parent_node = ParentNode(None, None)
        self.assertRaises(ValueError, parent_node.to_html)


if __name__ == "__main__":
    unittest.main(unittest.main())
