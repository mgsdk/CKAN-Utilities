# -*- coding: utf-8 -*-

import os
import subprocess

def main():
    # Get the path of the root CKAN directory.
    root_path = os.path.abspath(os.path.join(os.path.curdir, ".."))
    
    # Update the repositories.
    update_repository("core", root_path)
    update_repository("cmdline", root_path)
    update_repository("GUI", root_path)
    update_repository("utilities", root_path)
    update_repository("GUI-Xwt", root_path)
    
    return

def update_repository(name, root_path):
    print("Updating repository \"" + name + "\"")
    
    # Change to the correct folder.
    ckan_folder_name = "CKAN-" + name
    ckan_folder_path = os.path.join(root_path, ckan_folder_name)
    
    if not os.path.exists(ckan_folder_path):
        return
    
    os.chdir(ckan_folder_path)
    
    # Reset the state of the repository.
    subprocess.call("git reset --hard HEAD", shell = True)
    
    # Go to the master branch.
    subprocess.call("git checkout master", shell = True)
    
    # Pull changes.
    subprocess.call("git pull upstream master", shell = True)
    subprocess.call("git pull", shell = True)
    
    # Push changes to github.
    subprocess.call("git push", shell = True)

if __name__ == "__main__":
    main()