#!/usr/bin/env python3

#A Command-Line Interface Python script that will output
#a list of duplicate files identified by their absolute path and name.

import argparse
import os
import sys
import pprint
import hashlib
import json
import time

# WAYPOINT01: Write a Python Script Skeleton
def parse_arguments():
    """
    Convert argument strings to objects and assign them as attributes of
    the namespace.

    @return: an instance ``argparse.Namespace`` corresponding to the
        populated namespace.
    """
    # Initialize parser
    parser = argparse.ArgumentParser(description='Duplicate Files Finder')

    # Add positional and optional arguments
    parser.add_argument('-p', '--path', metavar='PATH', required=True,
        help='The root directory to start scanning for duplicate files')

    return parser.parse_args()

def check_exist_pathname(path_name):
    """
    Check if given path is exist or not.

    @param: path name in need of checking

    @return: 
        - True if given path name is valid
        - False otherwise
    """
    try:
        if not isinstance(str, path_name) or not path_name:
            return False      
    except TypeError:
        return os.path.exists(path_name)

# WAYPOINT02: Search for all the Files
def scan_files(path):
    """
    Search all the files from an absolute path

    @param: path: an absolute path

    @return: A flat list of files (scanned recursively) from the specified path
    """

    # Create a list of Absolute Path
    full_paths_list = []

    for dir_path, file_name, filenames in os.walk(path):
        for file_name in filenames:
            full_path = os.path.join(dir_path, file_name)
            # eleminate symlink list
            if not os.path.islink(full_path):
                full_paths_list.append(full_path)
            
    return full_paths_list

def group_by_condition(file_path_names, function):
    """
    Group by condition
    """
    # Create a dictionary with the key is filesize or checksum
    group_by_condition = {}

    # Add link paths as list into dictionary
    for file_path in file_path_names:
        # ignore empty file(fuction group_by_size) or broken link(funtion check_sum)
        if function(file_path): 
            group_by_condition.setdefault(function(file_path), []).append(file_path)
    
    # Eliminate lists which have only one file
    return [file_path for file_path in group_by_condition.values() if
            len(file_path) > 1]

# WAYPOINT03: Group Files by their Size
def group_files_by_size(file_path_names):
    """
    Group files by them their size

    @param: file_path_names: flat list of absolute file path names

    @return: a list of groups (with at least two files) which have the same size
    """
 
    return group_by_condition(file_path_names, os.path.getsize)

# WAYPOINT04: Generate a Hash Value for a File
def get_file_checksum(file_path_name, method=hashlib.md5):
    """
    Get the MD5 hash value of the content of the file

    @param: 
        -file_path_name: the absolute path of a file
        -method with default value hashlib.md5

    @return: MD5 hash value of the content of this file
    """
    # Calculate hash file contents by open, read, close file
    with open(file_path_name, 'rb') as file_check:
        data = file_check.read()
    return method(data).hexdigest()

# WAYPOINT05: Group Files by their Checksum
def group_files_by_checksum(file_path_names):
    """
    Group files by their checksum

    @param: file_path_names: A flat list of the absolute path and name of files

    @return: A list of groups that contain duplicate files
    """
    return group_by_condition(file_path_names, get_file_checksum)

# WAYPOINT06: Find all Duplicate Files
def find_duplicate_files(file_path_names):
    """
    Find all duplicate files (by checking their size and checksum)

    @Param: file_path_names: A flat list of the absolute path and name of files

    @Return: a list of groups that contain duplicate files
    """
    group_by_dup = []

    # Group file by size first then check checksum
    for file_path in group_files_by_size(file_path_names):
        group_by_dup.extend(group_files_by_checksum(file_path))

    return group_by_dup

# WAYPOINT07: Output a JSON Expression
def format_print(path_list):
    """
    Serialize the list to a JSON formatted string

    @param: path_list: a list of the absolute path and name of files

    @return: the list to a JSON formatted string
    """
    return json.dumps(path_list, indent=4)

# WAYPOINT08: Performance Optimization (Bonus)
BUFSIZE=64*1024

def do_cmp(f1, f2):
    """
    Compare the files named f1 and f2

    @param: 
        -f1: file 1
        -f2: file 2

    @return: 
        -True if they seem equal
        -False otherwise 
    """
    bufsize = BUFSIZE

    # Compare by open and read bytes chunk 8MB
    # If detect difference between them return False 
    with open(f1, 'rb') as fp1, open(f2, 'rb') as fp2:
        while True:
            b1 = fp1.read(bufsize) 
            b2 = fp2.read(bufsize)
            if b1 != b2:
                return False
            if not b1:
                return True

def group_files_by_compare(file_path_names):
    """
    Group files by compare their contents
    
    @param: file_path_names: A flat list of the absolute path and name of files

    @return: A list of groups that contain duplicate files
    
    """
    result = []

    while file_path_names:
        
        file_path_names_update = []
        dupl_file_group = [] # store duplicate files groups
        first_ele_tmp = file_path_names[0] 
        dupl_file_group.append(first_ele_tmp)

        # Always compare the rest to the first element of the list
        for file_path in file_path_names[1:]:
            if do_cmp(first_ele_tmp, file_path):
                dupl_file_group.append(file_path)
            else:
                # Store file_path_name updated (eleminated duplicate files) to compare next loops
                file_path_names_update.append(file_path) 
        
        if len(dupl_file_group) > 1: #eleminate lists which have only one element
            result.append(dupl_file_group)

        # Update file_path_name list to avoiding to duplicate check  
        file_path_names = file_path_names_update

    return result

def find_duplicate_files_by_compare(file_path_names):
    """
    Find all duplicate files (by checking their size and comparing contents)

    @Param: file_path_names: A flat list of the absolute path and name of files

    @Return: a list of groups that contain duplicate files
    """

    group_by_dup = []

    # Group file by size first then compare
    for file_path in group_files_by_size(file_path_names):
        group_by_dup.extend(group_files_by_compare(file_path))

    return group_by_dup

def main():
    """
    Call funtions and running
    """
    start = time.time()
    arguments = parse_arguments()

    # Check if exist path name
    if not check_exist_pathname(arguments.path):
        print("Not a exist path")
        return  

    # Convert specified path to a normalized absolutized version of the pathname path
    path = os.path.abspath(arguments.path)

    # A flat list of files from the specified path as 'file_path_name'
    file_path_names = scan_files(path)
    
    # TEST WAYPOINT07
    # print(format_print(find_duplicate_files(file_path_names)))
    # end_checksum = time.time()
    # print(f'checksum_function finished in {str(end_checksum-start)} secs')
    
    # TEST WAYPOINT08
    print(format_print(find_duplicate_files_by_compare(file_path_names)))
    end_compare = time.time()
    print(f'compare_function finished in {str(end_compare-start)} secs')


if __name__ == "__main__":
    main()
