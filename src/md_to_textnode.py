from textnode import TextType, TextNode


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
