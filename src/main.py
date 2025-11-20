import os
import shutil
     
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

                


def main():
    del_public()
    copy_static(static_dir, public_dir)
main()




