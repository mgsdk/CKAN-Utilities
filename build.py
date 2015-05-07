# -*- coding: utf-8 -*-

import os
import shutil
import subprocess

def main():
    # Get the path of the root CKAN directory.
    root_path = os.path.abspath(os.path.join(os.path.curdir, ".."))
    
    # Build each repository.
    build_repository("core", root_path)
    build_repository("GUI", root_path)
    build_repository("cmdline", root_path)
    
    link_main_ckan(root_path)
    
    return

def link_main_ckan(root_path):
    # Copy all the required resources.
    build_output_dir = os.path.join(root_path, "Build")
    
    if not os.path.exists(build_output_dir):
        os.makedirs(build_output_dir)
    
    copy_resources("core", root_path, build_output_dir)
    copy_resources("GUI", root_path, build_output_dir)
    copy_resources("cmdline", root_path, build_output_dir)
    
    # Copy the packer.
    shutil.copy(os.path.join(root_path, "CKAN-core", "packages", "ILRepack.1.25.0", "tools", "ILRepack.exe"), os.path.join(build_output_dir, "ILRepack.exe"))
    
    # Create the final executable.
    os.chdir(build_output_dir)
    subprocess.call("mono ILRepack.exe /target:exe /out:ckan.exe CmdLine.exe CKAN-GUI.exe ChinhDo.Transactions.dll CKAN.dll CommandLine.dll ICSharpCode.SharpZipLib.dll log4net.dll Newtonsoft.Json.dll INIFileParser.dll CurlSharp.dll", shell = True)
    
    return

def build_repository(name, root_path):
    print("Building repository \"" + name + "\"")
    
    # Change to the correct folder.
    ckan_folder_name = "CKAN-" + name
    ckan_folder_path = os.path.join(root_path, ckan_folder_name)
    
    if not os.path.exists(ckan_folder_path):
        return
    
    os.chdir(ckan_folder_path)
    
    # Call the build script.
    subprocess.call("sh build.sh", shell = True)
    
    return

def copy_resources(name, root_path, build_path):
    # Change to the correct folder.
    ckan_folder_name = "CKAN-" + name
    ckan_folder_path = os.path.join(root_path, ckan_folder_name, "bin", "Debug")
    
    # Get all the dll files.
    files = os.listdir(ckan_folder_path)
    
    for f in files:
        if os.path.splitext(f)[1] == ".dll":
            shutil.copy(os.path.join(ckan_folder_path, f), build_path)
        if os.path.splitext(f)[1] == ".exe":
            shutil.copy(os.path.join(ckan_folder_path, f), build_path)
    
    return
    
if __name__ == "__main__":
    main()