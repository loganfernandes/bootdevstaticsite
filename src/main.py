from functions import write_static_to_public, generate_pages_recursive
import sys

def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"
        
    
    print("Running...")
    write_static_to_public("../static", "../docs")
    
    generate_pages_recursive("content", "template.html", "docs", basepath)
    
    print("Generation complete.")
main()