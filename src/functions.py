from textnode import TextType, TextNode
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i, section in enumerate(sections):
            if section == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(section, TextType.TEXT))
            else:
                split_nodes.append(TextNode(section, text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text):
    # text = raw markdown text
    extracted_list = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    
    return extracted_list # should contain the alt text and URL of any markdown images

def extract_markdown_links(text):
    # that extracts markdown links instead of images
    extracted_list = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    
    return extracted_list # return tuples of anchor text and URLs

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        extracted = extract_markdown_images(node.text)
        if len(extracted) == 0:
            new_nodes.append(node)
            continue
        remaining_text = node.text
        for (alt, url) in extracted:
            split_text = remaining_text.split(f"![{alt}]({url})", 1)
            if split_text[0]:
                new_nodes.append(TextNode(split_text[0], TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            remaining_text = split_text[1]
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes
    
def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        extracted = extract_markdown_links(node.text)
        if len(extracted) == 0:
            new_nodes.append(node)
            continue
        remaining_text = node.text
        for (text, url) in extracted:
            split_text = remaining_text.split(f"[{text}]({url})", 1)
            if split_text[0]:
                new_nodes.append(TextNode(split_text[0], TextType.TEXT))
            new_nodes.append(TextNode(text, TextType.LINK, url))
            remaining_text = split_text[1]
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
            
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    
    return nodes

def markdown_to_blocks(markdown):
    cleaned_list = []
    split_markdown = markdown.split("\n\n")
    for block in split_markdown:
        if block == "":
            continue
        clean_block = block.strip()
        cleaned_list.append(clean_block)
    return cleaned_list