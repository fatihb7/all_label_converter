"""
Author: Fatih Baday <bfatih27@gmail.com>
Purpose: Helper functions to be used in changing tag types.
"""
# Importing libraries.
import os
import cv2
import logging


def check_path_exist(path: str):
    """
    :param path: path of the file/folder to check.
    :return: true or false (success or fail)
    """
    if not os.path.isdir(path):
        logging.error("The file path of the Data could not be found! Please check!")
        return False
    else:
        return True


def check_file_exist(path: str, file_name: str):
    """
    :param path: path of the folder to check
    :param file_name: file name.
    :return: true or false (success or fail)
    """
    if file_name not in os.listdir(path):
        logging.error(f"The '{file_name}' file could not be found! Please check!")
        logging.error("The process has been terminated. Unsuccessful!")
        return False
    else:
        return True


def get_image_size(path: str, file_name: str):
    """
    :purpose: Get image height and weight.
    :param path: folder_path.
    :param file_name: image file name.
    :return: image shape
    """
    image_path = os.path.join(path, file_name)
    if not os.path.exists(image_path):
        logging.error("The image file not founded. Width, height, depth value was defined 0.")
        return 0, 0, 0

    return cv2.imread(image_path).shape
