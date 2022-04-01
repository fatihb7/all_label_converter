"""
Author: Fatih Baday <bfatih27@gmail.com>
Purpose: As class is called, it reads the config file and transfers it to the class.
"""
# Importing libraries.
import os
import yaml

from pathlib import Path

# Get path of current file for set config path.
CONFIG_FILE_PATH = os.path.join(Path(__file__).parent.parent, "config.yaml")


class Config:
    with open(CONFIG_FILE_PATH, 'r') as f:
        settings = yaml.safe_load(f)
