import unittest
from md_to_textnode import split_nodes_images, split_nodes_links, split_nodes_delimiter, text_to_textnodes, markdown_to_blocks, block_to_blocktype
from textnode_to_html import text_node_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextType, BlockType, TextNode
from markdown_to_html import markdown_to_html_node


class TestMDToHTML(unittest.TestCase):
    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )


class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_single_paragraph_simple(self):
        md = "Hello world"
        node = markdown_to_html_node(md)
        self.assertEqual(node.to_html(), "<div><p>Hello world</p></div>")

    def test_multiple_paragraphs_trim_blank_lines(self):
        md = """
First paragraph.

Second paragraph here.

Third one.
"""
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div>"
            "<p>First paragraph.</p>"
            "<p>Second paragraph here.</p>"
            "<p>Third one.</p>"
            "</div>",
        )

    def test_heading_levels(self):
        md = """
# Title
## Subtitle
###### Tiny
"""
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div>"
            "<h1>Title</h1>"
            "<h2>Subtitle</h2>"
            "<h6>Tiny</h6>"
            "</div>",
        )

    def test_unordered_list(self):
        md = """
- item one
- item two
- item three
"""
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><ul>"
            "<li>item one</li>"
            "<li>item two</li>"
            "<li>item three</li>"
            "</ul></div>",
        )

    def test_ordered_list(self):
        md = """
1. first
2. second
3. third
"""
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><ol>"
            "<li>first</li>"
            "<li>second</li>"
            "<li>third</li>"
            "</ol></div>",
        )

    def test_blockquote(self):
        md = """
> This is a quote
> that spans lines
"""
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><blockquote>This is a quote that spans lines</blockquote></div>",
        )

    def test_mixed_blocks(self):
        md = """
# Title

Paragraph with **bold** and `code`.

- list item one
- list item two
"""
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div>"
            "<h1>Title</h1>"
            "<p>Paragraph with <b>bold</b> and <code>code</code>.</p>"
            "<ul>"
            "<li>list item one</li>"
            "<li>list item two</li>"
            "</ul>"
            "</div>",
        )

    def test_code_block_ignores_inline(self):
        md = ""


if __name__ == "__main__":
    unittest.main(unittest.main())
