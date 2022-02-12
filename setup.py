# Loading libraries.
import os
import setuptools

# Describe constant variables.
REQUIREMENTS_FILE_NAME = 'requirements.txt'
LONGDESC_FILE_NAME = 'README.MD'


def get_longdescription(file_name):
    """
    Purpose: Read 'Readme.MD' files for long_description.
    Author: Fatih Baday
    Input:  1.file_name (required - str) (readme.md file name)
    Output: 1.content (required - str) (content of readme.md file)
    """
    file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), file_name)
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def get_requirements(file_name):
    """
    Purpose: Get requirements for 'requirements.txt'.
    Author: Fatih Baday
    Input:  1.file_name (required - str) (requirements file name)
    Output: 1.dependencies_list (required - str) (list of dependencies)
    """
    file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), file_name)
    with open(file_path) as f:
        return f.read().splitlines()


# Define setup parameters.
setuptools.setup(
    name="all_label_converter",
    version="0.1.3",
    author="Fatih Baday",
    author_email="bfatih27@gmail.com",
    description="To convert image labels between each other.",
    long_description=get_longdescription(LONGDESC_FILE_NAME),
    long_description_content_type="text/markdown",
    url="https://github.com/fatihb7/all_label_converter",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3"],
    python_requires='>=3.6.0',
    install_requires=get_requirements(REQUIREMENTS_FILE_NAME)
)
