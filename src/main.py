from textnode import TextNode, TextType


def main():
    myText = TextNode("here's a dummy value", TextType.LINK, "www.thebigGoog.com")
    print(myText)
    
    
main()