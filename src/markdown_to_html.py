from md_to_textnode import split_nodes_images, split_nodes_links, split_nodes_delimiter, text_to_textnodes, markdown_to_blocks, block_to_blocktype
from textnode_to_html import text_node_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextType, BlockType, TextNode


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        block_type = block_to_blocktype(block)
        children.append(block_to_htmlnode(block, block_type))
        
    return ParentNode("div", children)


def block_to_htmlnode(block, block_type):
    if block_type == BlockType.CODE:
        block_lines = block.split("\n")
        cut_lines = block_lines[1:len(block_lines) - 1]
        code_text = "\n".join(cut_lines)

        text_node = TextNode(code_text, TextType.TEXT)
        code_child = text_node_to_html_node(text_node)

        code_node = ParentNode("code", [code_child])
        pre_node = ParentNode("pre", [code_node])

        return pre_node

    if block_type == BlockType.PARAGRAPH:
        children = text_to_children(block)
        return ParentNode("p", children)

    if block_type == BlockType.HEADING:
        num_hash = 0
        for c in block[0:6]:
            if c == "#":
                num_hash += 1
            else:
                break

        children = text_to_children(block[num_hash:].lstrip())
        return ParentNode(f"h{num_hash}", children)

    if block_type == BlockType.QUOTE:
        block_lines = block.split("\n")
        cut_lines = []
        for line in block_lines:
            if line[0] == ">":
                cut_lines.append(line[1:].strip())
            else:
                cut_lines.append(line.strip())
        quote_text = "\n".join(cut_lines)
        children = text_to_children(quote_text)

        return ParentNode("blockquote", children)

    if block_type in (BlockType.UNORDERED_LIST, BlockType.ORDERED_LIST):
        li_nodes = []
        for line in block.split("\n"):
            line = line.strip()
            if block_type == BlockType.UNORDERED_LIST:
                item_text = line[2:]
            else:
                dot_index = line.find(".")
                item_text = line[dot_index + 2:]

            li_children = text_to_children(item_text)
            li_nodes.append(ParentNode("li", li_children))

        outer_tag = "ul" if block_type == BlockType.UNORDERED_LIST else "ol"
        return ParentNode(outer_tag, li_nodes)


def text_to_children(block):
    text_nodes = text_to_textnodes(block)
    html_nodes = []
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))

    return html_nodes

