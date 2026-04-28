from textnode import TextType, TextNode, text_node_to_html_node
from blocktype import block_to_block_type, BlockType
from htmlnode import LeafNode, ParentNode
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

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        children.append(block_to_html_node(block))
    return ParentNode("div", children)
        
def block_to_html_node(block):
    block_type = block_to_block_type(block)
    match block_type:
        case (BlockType.PARAGRAPH):
            text = block.split("\n")
            text = " ".join(text)
            children = text_to_children(text)
            return ParentNode("p", children)
        case (BlockType.HEADING):
            heading_level = get_heading_level(block)
            text = block[heading_level + 1:]
            children = text_to_children(text)
            return LeafNode(f"h{heading_level}", children)
        case (BlockType.CODE):
            code = ParentNode("code", [get_code_lines(block)])
            return ParentNode("pre", [code])
        case (BlockType.QUOTE):
            text = " ".join(get_quote_lines(block))
            children = text_to_children(text)
            return ParentNode("blockquote", children)
        case (BlockType.UNORDERED_LIST):
            li_nodes = get_unordered_list_lines(block)
            return ParentNode("ul", li_nodes)
        case (BlockType.ORDERED_LIST):
            li_nodes = get_ordered_list_lines(block)
            return ParentNode("ol", li_nodes)
        
def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes

def get_heading_level(block):
    count = 0
    for char in block:
        if char == "#":
            count += 1
        else:
            break
    return count

def get_quote_lines(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        new_line = line[1:].strip()
        new_lines.append(new_line)
    return new_lines

def get_unordered_list_lines(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        new_line = line[2:]
        new_lines.append(ParentNode("li", text_to_children(new_line)))
    return new_lines

def get_ordered_list_lines(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        new_line = line.split(". ", 1)
        new_lines.append(ParentNode("li", text_to_children(new_line[1])))
    return new_lines
    
def get_code_lines(block):
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    return child
    