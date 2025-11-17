import unittest
from textnode_to_html import text_node_to_html_node
from md_to_textnode import split_nodes_delimiter, split_nodes_images, split_nodes_links, text_to_textnodes, markdown_to_blocks, block_to_blocktype
from md_to_link import extract_markdown_images, extract_markdown_links
from textnode import TextNode, TextType, BlockType


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


    def test_md_split_code(self):
        old_nodes = [
            TextNode("text node", TextType.TEXT),
            TextNode("node `code` text", TextType.TEXT),
            TextNode("ila _ic_", TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(old_nodes, "`", TextType.CODE)
        new_nodes_check = [
            TextNode("text node", TextType.TEXT),
            TextNode("node ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT),
            TextNode("ila _ic_", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, new_nodes_check)


    def test_md_split_code2(self):
        old_nodes = [
            TextNode("text node", TextType.TEXT),
            TextNode("node code` text", TextType.TEXT),
            TextNode("ila _ic_", TextType.TEXT)
        ]
        with self.assertRaises(Exception):
            split_nodes_delimiter(old_nodes, "`", TextType.CODE)


    def test_md_split_code3(self):
        old_nodes = [
            TextNode("text node", TextType.TEXT),
            TextNode("node ` code` text", TextType.TEXT),
            TextNode("ila _ic_", TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(old_nodes, "`", TextType.CODE)
        new_nodes_check = [
            TextNode("text node", TextType.TEXT),
            TextNode("node ", TextType.TEXT),
            TextNode(" code", TextType.CODE),
            TextNode(" text", TextType.TEXT),
            TextNode("ila _ic_", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, new_nodes_check)


    def test_md_to_link(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)


    def test_md_to_link2(self):
        matches = extract_markdown_images(
            "davor auch text ![image](https://www.freeiconspng.com/images/pepe-png) und halt noch text und so"
        )
        self.assertListEqual([("image", "https://www.freeiconspng.com/images/pepe-png")], matches)


    def test_md_to_link3(self):
        matches = extract_markdown_links(
            "davor auch text [titel vom link](https://www.freeiconspng.com/images/pepe-png) und halt noch text und so"
        )
        self.assertListEqual([("titel vom link", "https://www.freeiconspng.com/images/pepe-png")], matches)


    def test_md_to_link4(self):
        matches = extract_markdown_links("[titel vom link](http://www.ratemypoo.com/)")
        self.assertListEqual([("titel vom link", "http://www.ratemypoo.com/")], matches)
    

    def test_md_to_link4(self):
        matches = extract_markdown_links("text ohn link")
        self.assertListEqual([], matches)



    def test_split_nodes_images(self):
        node = TextNode("Text start ![image title](http://www.imagelink.com/image.png) text after ![2. image title](http://www.anderesbild.de/bild.png) und nochmal text", TextType.TEXT)
        new_nodes = split_nodes_images([node])
        self.assertListEqual(
            [
                TextNode("Text start ", TextType.TEXT),
                TextNode("image title", TextType.IMAGE, "http://www.imagelink.com/image.png"),
                TextNode(" text after ", TextType.TEXT),
                TextNode("2. image title", TextType.IMAGE, "http://www.anderesbild.de/bild.png"),
                TextNode(" und nochmal text", TextType.TEXT),
            ],
            new_nodes,
        )


    def test_split_nodes_images2(self):
        node = TextNode("![image title](http://www.imagelink.com/image.png) text after ![2. image title](http://www.anderesbild.de/bild.png) ", TextType.TEXT)
        new_nodes = split_nodes_images([node])
        self.assertListEqual(
            [
                TextNode("image title", TextType.IMAGE, "http://www.imagelink.com/image.png"),
                TextNode(" text after ", TextType.TEXT),
                TextNode("2. image title", TextType.IMAGE, "http://www.anderesbild.de/bild.png"),
            ],
            new_nodes,
        )


    def test_split_nodes_images3(self):
        node = TextNode("![image title](http://www.imagelink.com/image.png)![2. image title](http://www.anderesbild.de/bild.png)", TextType.TEXT)
        new_nodes = split_nodes_images([node])
        self.assertListEqual(
            [
                TextNode("image title", TextType.IMAGE, "http://www.imagelink.com/image.png"),
                TextNode("2. image title", TextType.IMAGE, "http://www.anderesbild.de/bild.png"),
            ],
            new_nodes,
        )


    def test_split_nodes_links(self):
        node = TextNode("Text start [link title](http://www.imagelink.com/image.png) text after [2. link title](http://www.anderesbild.de/bild.png) und nochmal text", TextType.TEXT)
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("Text start ", TextType.TEXT),
                TextNode("link title", TextType.LINK, "http://www.imagelink.com/image.png"),
                TextNode(" text after ", TextType.TEXT),
                TextNode("2. link title", TextType.LINK, "http://www.anderesbild.de/bild.png"),
                TextNode(" und nochmal text", TextType.TEXT),
            ],
            new_nodes,
        )


    def test_text_to_textnodes(self):
        node = TextNode("Dies **bold** ist ein test _italic_ du verstehst `code block` und dazu ein [link](https://www.jajaja.com) und so ![image](http://bild.de/kek.png)", TextType.TEXT)
        new_nodes = text_to_textnodes([node])
        self.assertListEqual(
            [
                TextNode("Dies ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" ist ein test ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" du verstehst ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" und dazu ein ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.jajaja.com"),
                TextNode(" und so ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "http://bild.de/kek.png")
            ],
            new_nodes,
        )

    def test_text_to_textnodes2(self):
        node = TextNode("![bild1](www.bild1.de)Dies **bold** ist ein test _italic_ du verstehst `code block` und dazu ein [link](https://www.jajaja.com) und so ![image](http://bild.de/kek.png)", TextType.TEXT)
        new_nodes = text_to_textnodes([node])
        self.assertListEqual(
            [
                TextNode("bild1", TextType.IMAGE, "www.bild1.de"),
                TextNode("Dies ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" ist ein test ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" du verstehst ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" und dazu ein ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.jajaja.com"),
                TextNode(" und so ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "http://bild.de/kek.png")
            ],
            new_nodes,
        )

    def test_text_to_textnodes3(self):
        node = TextNode("Dies **und nochmal** **bold** ist ein test _italic_ du verstehst `code block` und dazu ein [link](https://www.jajaja.com) und so ![image](http://bild.de/kek.png)", TextType.TEXT)
        new_nodes = text_to_textnodes([node])
        self.assertListEqual(
            [
                TextNode("Dies ", TextType.TEXT),
                TextNode("und nochmal", TextType.BOLD),
                TextNode(" ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" ist ein test ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" du verstehst ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" und dazu ein ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.jajaja.com"),
                TextNode(" und so ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "http://bild.de/kek.png")
            ],
            new_nodes,
        )

    def test_text_to_textnodes4(self):
        node = TextNode("[link](www.hallo.de)", TextType.TEXT)
        new_nodes = text_to_textnodes([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "www.hallo.de")
            ],
            new_nodes,
        )

    
    def test_markdown_to_blocks(self):
        md = """This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
Same paragraph but in a new line

- list
- still list"""

        blocks = markdown_to_blocks(md)
        self.assertEqual(
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nSame paragraph but in a new line",
                "- list\n- still list"
            ],
            blocks
        )
 
    def test_markdown_to_blocks2(self):
        md = """This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
Same paragraph but in a new line



- list
- still list"""

        blocks = markdown_to_blocks(md)
        self.assertEqual(
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nSame paragraph but in a new line",
                "- list\n- still list"
            ],
            blocks
        )


    def test_block_to_blocktype(self):
        block = "- item\n- item2\n- item3"
        
        block_type = block_to_blocktype(block)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_block_to_blocktype2(self):
        block = "1. item1\n2. item2\n3. item3"
        
        block_type = block_to_blocktype(block)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)

    def test_block_to_blocktype3(self):
        block = ">blblbllb\n>blabla\n>jaja"
        
        block_type = block_to_blocktype(block)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_block_to_blocktype4(self):
        block = """### head"""
        
        block_type = block_to_blocktype(block)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_heading_levels(self):
        for i in range(1, 7):
            block = "#" * i + " Title"
            assert block_to_blocktype(block) == BlockType.HEADING

    def test_paragraph_fallback(self):
        block = "Just a normal line\nwith another line"
        assert block_to_blocktype(block) == BlockType.PARAGRAPH

    def test_code_block_fence_only(self):
        block = "```\nprint('hi')\n```"
        assert block_to_blocktype(block) == BlockType.CODE

    def test_code_block_requires_two_lines(self):
        block = "```"
        assert block_to_blocktype(block) == BlockType.PARAGRAPH

    def test_quote_all_lines_prefixed(self):
        block = "> a\n> b\n> c"
        assert block_to_blocktype(block) == BlockType.QUOTE

    def test_quote_rejects_mixed_lines(self):
        block = "> a\nnot quote"
        assert block_to_blocktype(block) == BlockType.PARAGRAPH

    def test_unordered_list_all_lines_prefixed(self):
        block = "- one\n- two\n- three"
        assert block_to_blocktype(block) == BlockType.UNORDERED_LIST

    def test_unordered_list_rejects_mixed_lines(self):
        block = "- one\nx two"
        assert block_to_blocktype(block) == BlockType.PARAGRAPH

    def test_ordered_list_strict_sequence(self):
        block = "1. one\n2. two\n3. three"
        assert block_to_blocktype(block) == BlockType.ORDERED_LIST

    def test_ordered_list_wrong_numbering(self):
        block = "1. one\n3. three"
        assert block_to_blocktype(block) == BlockType.PARAGRAPH

    def test_empty_block_is_paragraph(self):
        assert block_to_blocktype("") == BlockType.PARAGRAPH

    def test_blank_line_inside_block_causes_paragraph(self):
        block = "- one\n\n- two"
        assert block_to_blocktype(block) == BlockType.PARAGRAPH


if __name__ == "__main__":
    unittest.main(unittest.main())      
