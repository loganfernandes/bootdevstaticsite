from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(markdown_block):
    lines = markdown_block.split("\n")
    
    if is_heading(lines):
        return BlockType.HEADING
    if is_code(markdown_block):
        return BlockType.CODE
    if is_quote(lines):
        return BlockType.QUOTE
    if is_unordered_list(lines):
        return BlockType.UNORDERED_LIST
    if is_ordered_list(lines):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def is_heading(lines):
    count = 0
    if len(lines) != 1:
        return False
    block = lines[0]
    for char in block:
        if char == "#":
            count += 1
        else:
            break
    if 1 <= count <= 6 and count < len(block):
        return block[count] == " "
    return False
    
            
def is_code(block):
    return block.startswith("```\n") and block.endswith("```")
 
def is_quote(lines):
    return all(line.startswith(">") for line in lines)

def is_unordered_list(lines):
    return all(line.startswith("- ") for line in lines)
 
def is_ordered_list(lines):
    tracker = []
    for i, line in enumerate(lines, 1):
        expected_prefix = f"{i}. "
        tracker.append(line.startswith(expected_prefix))
    return all(tracker) and len(tracker) > 0