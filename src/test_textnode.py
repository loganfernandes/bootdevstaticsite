import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        
    def test_url_not_eq(self):
        node = TextNode("Testing no URL", TextType.LINK)
        node2 = TextNode("Testing no URL", TextType.LINK, "google")
        self.assertNotEqual(node, node2)
        
    def test_textType_eq(self):
        node = TextNode("Testing text type", TextType.LINK)
        node2 = TextNode("Testing text type", TextType.LINK)
        self.assertEqual(node, node2)
    
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

if __name__ == "__main__":
    unittest.main()
