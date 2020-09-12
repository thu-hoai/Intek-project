#!/usr/bin/env python3
"""The utilities to application"""
import hashlib
import hmac
import json
import os


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def hash_message(consumer_secret, path, body_message):
    """Hash a given message

    Args:
        consumer_secret (str): The consumer secret of client application
        path (str): the endpoint of the method
        body_message (str): a string of the message body

    Returns:
        str: the hash string of the message
    """
    message = path + json.dumps(body_message)
    encrypted_content = hmac.new(
        consumer_secret.encode(),
        msg=message.encode(),
        digestmod=hashlib.sha1)
    hashed_value = encrypted_content.hexdigest()

    return hashed_value


def is_an_allowed_file_extension(file_name):
    """ Check if given file is belong to allowed extension or not

    Args:
        file_name (str): file name

    Returns:
        (bool): True if the file extension is allowed. False otherwise
    """
    if '.' in file_name:
        if file_name.split('.')[-1] in ALLOWED_EXTENSIONS:
            return True
    return False


def create_directory_tree(directory, cache_directory_depth, file_name):
    """Create a directory tree

    Args:
        directory (str): the path of the directory
        cache_directory_depth (int): The number of the directory depth
        file_name (str): file name

    Returns:
        str: the directory path
    """
    depth_lst = list(file_name[:cache_directory_depth])

    for char in depth_lst:
        directory = os.path.join(directory, char)
        os.makedirs(directory, exist_ok=True)
    return directory


def remove_photos_from_directory(directory, filename_list):
    """Remove a file from a directory

    Args:
        directory (str): The directory path where store file
        filename_list (list): A list of file names which should be removed

    Returns:
        int: The number of files that were removed
    """
    # Remove all photos file
    count = 0
    for root, dirs, files in os.walk(directory):
        for image_name in files:
            if image_name.split('.')[0] in filename_list:
                count += 1
                photo_path = os.path.join(root, image_name)
                print('photo_path', photo_path)
                os.remove(photo_path)

    return count
