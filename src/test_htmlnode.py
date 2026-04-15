import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(props={"href": "https://www.google.com"})
        result = node.props_to_html()
        self.assertEqual(result, ' href="https://www.google.com"')
        
    def test_props_to_html_none(self):
        node = HTMLNode()
        result = node.props_to_html()
        self.assertEqual(result, "")
        
    def test_props_to_html_empty(self):
        node = HTMLNode(props={})
        result = node.props_to_html()
        self.assertEqual(result, "")
        
    def test_props_to_html_two(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        result = node.props_to_html()
        self.assertEqual(result, ' href="https://www.google.com" target="_blank"')

if __name__ == "__main__":
    unittest.main()
