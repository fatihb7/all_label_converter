"""
Author: Fatih Baday <bfatih27@gmail.com>
Purpose: As class is called, it reads the config file and transfers it to the class.
"""
# Importing libraries.
import os
import yaml

# Constant variables.
CONFIG_FILE_PATH = os.path.join(os.getcwd(), "config.yaml")


class Config:
    with open(CONFIG_FILE_PATH, 'r') as f:
        settings = yaml.safe_load(f)
