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
            return [old_nodes]
        
        
    
    
def split_nodes_link(old_nodes):