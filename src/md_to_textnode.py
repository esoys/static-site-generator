from textnode import TextType, TextNode, BlockType
from md_to_link import extract_markdown_links, extract_markdown_images


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    seperated_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            seperated_nodes.append(node)

        else:
            parts = node.text.split(delimiter)
            
            if len(parts) % 2 == 0:
                raise Exception("invalid markdown syntax")

            sep_parts = []

            for i in range(0, len(parts)):
                if i % 2 == 0:
                    sep_parts.append(TextNode(parts[i], TextType.TEXT))
                else:
                    sep_parts.append(TextNode(parts[i], text_type))
                
            seperated_nodes.extend(sep_parts)
            
    return seperated_nodes


def split_nodes_images(old_nodes):
    seperated_nodes = []
    
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            seperated_nodes.append(node)

        else:
            images = extract_markdown_images(node.text)

            if not images:
                seperated_nodes.append(node)
                continue
            else:
                parts = []
                node_text = node.text
                sep_parts = []

                for image in images:
                    first_segment = node_text.split(
                        f"![{image[0]}]({image[1]})", 1
                    )
                    parts.append(first_segment[0])
                    if len(first_segment) == 2:
                        node_text = first_segment[1]
                    else:
                        parts.append(node_text)
                        break

                parts.append(node_text)

                for i in range(0, len(parts)):
                    if parts[i].strip():
                        sep_parts.append(TextNode(parts[i], TextType.TEXT))

                    if i < len(images):
                        sep_parts.append(TextNode(images[i][0], TextType.IMAGE, images[i][1]))

                seperated_nodes.extend(sep_parts)
    
    return seperated_nodes


def split_nodes_links(old_nodes):
    seperated_nodes = []
    
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            seperated_nodes.append(node)

        else:
            links = extract_markdown_links(node.text)

            if not links:
                seperated_nodes.append(node)
                continue
            else:
                parts = []
                sep_parts = []
                node_text = node.text

                for link in links:
                    first_segment = node_text.split(
                        f"[{link[0]}]({link[1]})", 1
                    )
                    parts.append(first_segment[0])
                    if len(first_segment) == 2:
                        node_text = first_segment[1]
                    else:
                        parts.append(node_text)
                        break

                parts.append(node_text)

                for i in range(0, len(parts)):
                    if parts[i].strip():
                        sep_parts.append(TextNode(parts[i], TextType.TEXT))

                    if i < len(links):
                        sep_parts.append(TextNode(links[i][0], TextType.LINK, links[i][1]))

                seperated_nodes.extend(sep_parts)
    
    return seperated_nodes


def text_to_textnodes(text):
    return split_nodes_delimiter(
        split_nodes_delimiter(
            split_nodes_delimiter(
                split_nodes_images(
                    split_nodes_links(text)
                ), "`", TextType.CODE
            ),"_", TextType.ITALIC
        ), "**", TextType.BOLD
    )


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    res_blocks = []
    for block in blocks:
        if block:
            res_blocks.append(block.strip())

    return res_blocks 
    

def block_to_blocktype(block):
    lines = block.split("\n")

    if not lines or (len(lines) == 1 and lines[0] == ""):
        return BlockType.PARAGRAPH
    
    for i in range(1, 7):
        if block.startswith("#" * i + " "):
            return BlockType.HEADING

    if len(lines) >= 2 and lines[0] == "```" and lines[-1] == "```":
        return BlockType.CODE


    if all(line.startswith(">") for line in lines): 
        return BlockType.QUOTE

    if all(line.startswith("- ") for line in lines): 
        return BlockType.UNORDERED_LIST

    ok = True
    for idx, line in enumerate(lines, start=1):
        if not line.startswith(f"{idx}. "):
            ok = False
            break
    if ok:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
