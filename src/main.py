from functions import write_static_to_public, generate_pages_recursive

def main():
    print("Running...")
    write_static_to_public()
    print("Generation complete.")
    
    generate_pages_recursive("content/", "template.html", "public/")
    
main()