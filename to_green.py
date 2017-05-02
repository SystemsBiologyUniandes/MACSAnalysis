import os
from shutil import copyfile
import sys

if len(sys.argv)!=2:
    print("The program must be run as python 'dir'. 'dir' is the experiment directory (with final /)")
    exit()
    
parent_dir = sys.argv[1]

if not parent_dir.endswith("/"):
    print("The experiment directory must contain the final /")
    

def list_directories(directory):
    '''Returns a list unhidden of directory filenames inside the directory.
    Args:
        directory (str): The directory containing the subdirectories to list.
    Returns:
        list: The list containing the directories.
    '''
    dir_names = [dir for root, dirs, files in os.walk(directory) for dir in dirs if not dir.startswith('.')]
    dir_names.sort()
    return dir_names

def list_files(directory = '.', extension = '.tif', pattern = ''):
    files = [file for root, dirs, files in os.walk(directory) for file in files if file.endswith(extension) and pattern in file]
    return files

time_dirs = list_directories(parent_dir)

for dire in time_dirs:
    part_dir = parent_dir+dire
    
    part_files = list_files(part_dir)
    for file in part_files:
        if file.endswith('c1.tif'):
            name = part_dir+'/'+file
            os.remove(name)
            
    part_files = list_files(part_dir)
    for file in part_files:
        if file.endswith('c3.tif'):
            in_name = part_dir+'/'+file
            out_name = part_dir+'/'+file[:-5]+'1.tif'     
            copyfile(in_name, out_name)
