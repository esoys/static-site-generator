import os
import shutil
from markdown_to_html import markdown_to_html_node, extract_title 
     
public_dir = os.path.abspath(os.path.join(os.getcwd(), "public"))
static_dir = os.path.abspath(os.path.join(os.getcwd(), "static"))


def del_public(): 
    if os.path.exists(public_dir):
        for dir in os.listdir(public_dir):
            print(f"deleting: {public_dir}/{dir}")
        shutil.rmtree(public_dir)
    
    os.mkdir("public")
    

def copy_static(source, target):
    if os.path.exists(source):
        for path in os.listdir(source):
            current_path = os.path.abspath(os.path.join(source, path))
            target_path = os.path.abspath(os.path.join(target, path))

            if os.path.isfile(current_path):
                print(f"copying: {current_path} to {target_path}")
                shutil.copy(current_path, target_path)
            else:
                if not os.path.exists(target_path):
                    os.mkdir(target_path)
                copy_static(current_path, target_path)

               

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    content_path = os.path.join(from_path, "index.md")
    template_path = os.path.join(template_path, "template.html")
    dest_file_path = os.path.join(dest_path, "index.html")

    print("template_path: ", template_path)
    
    with open(content_path, "r") as md_f:
        md = md_f.read()

    with open(template_path, "r") as template_f:
        template = template_f.read()

    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(dest_path)


    html_body = markdown_to_html_node(md).to_html()
    html_title = extract_title(md)

    template = template.replace("{{ Title }}", html_title)
    template = template.replace("{{ Content }}", html_body)

    with open(dest_file_path, "w") as dest_f:
        dest_f.write(template)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    content_path = os.path.join... 

    

def main():
    del_public()
    copy_static(static_dir, public_dir)
    from_path = os.path.abspath(os.path.join(os.getcwd(), "content"))
    template_path = os.path.abspath(os.getcwd())
    dest_path = public_dir
    generate_page(from_path, template_path, dest_path)
main()




