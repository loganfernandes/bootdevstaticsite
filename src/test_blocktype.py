import unittest
from blocktype import BlockType, block_to_block_type


class TestFunctions(unittest.TestCase):
    def test_block_to_block_type_one_heading(self):
        md = "# heading"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type,
            BlockType.HEADING
        )
    def test_block_to_block_type_two_heading(self):
        md = "## heading"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type,
            BlockType.HEADING
        )
    def test_block_to_block_type_three_heading(self):
        md = "### heading"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type,
            BlockType.HEADING
        )
    def test_block_to_block_type_four_heading(self):
        md = "#### heading"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type,
            BlockType.HEADING
        )
    def test_block_to_block_type_five_heading(self):
        md = "##### heading"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type,
            BlockType.HEADING
        )
    def test_block_to_block_type_six_heading(self):
        md = "###### heading"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type,
            BlockType.HEADING
        )
    def test_block_to_block_type_seven_heading(self):
        md = "####### heading"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type,
            BlockType.PARAGRAPH
        )
    def test_block_to_block_type_heading_no_space(self):
        md = "#heading"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type,
            BlockType.PARAGRAPH
        )
    def test_block_to_block_type_heading_no_text(self):
        md = "#"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type,
            BlockType.PARAGRAPH
        )
        
    def test_block_to_block_type_heading_extra_text(self):
        md = "# heading\nextra text"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type,
            BlockType.PARAGRAPH
        )
        
    def test_block_to_block_type_code(self):
        md = "```\nSome sample code goes here\n```"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type,
            BlockType.CODE
        )
    
    def test_block_to_block_type_quote(self):
        md = ">This is a test quote.\n>With multiple lines\n>Hopefully it all comes through correctly"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type,
            BlockType.QUOTE
        )
        
    def test_block_to_block_type_unordered_list(self):
        md = "- This is a test UNORDERED_LIST.\n- With multiple lines\n- Hopefully it all comes through correctly"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type,
            BlockType.UNORDERED_LIST
        )
        
    def test_block_to_block_type_ordered_list(self):
        md = "1. This is a test ORDERED_LIST.\n2. With multiple lines\n3. Hopefully it all comes through correctly"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type,
            BlockType.ORDERED_LIST
        )
        
    def test_block_to_block_type_paragraph(self):
        md = "Just a regular paragraph with nothing crazy in it"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type,
            BlockType.PARAGRAPH
        )
    
if __name__ == "__main__":
    unittest.main()
