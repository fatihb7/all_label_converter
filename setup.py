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


def get_packages():
    """
    Purpose: Get packages list.
    Author: Fatih Baday
    :return: packages_list
    """
    packages_list = setuptools.find_packages()
    return packages_list


def get_data_files():
    """
    Purpose: Get data files.
    Author: Fatih Baday
    :return: data_files
    """

    data_files = {
        "all_label_converter": ["config.yaml"]
    }

    return data_files


def get_exclude_files():
    """
    Purpose: Get exclude files list.
    Author: Fatih Baday
    :return: exclude_files
    """
    exclude_files = {
        "all_label_converter": ["for_test.py"]
    }
    return exclude_files


# Define setup parameters.
setuptools.setup(
    name="all_label_converter",
    version="0.1.7",
    author="Fatih Baday",
    author_email="bfatih27@gmail.com",
    description="To convert image labels between each other.",
    long_description=get_longdescription(LONGDESC_FILE_NAME),
    long_description_content_type="text/markdown",
    url="https://github.com/fatihb7/all_label_converter",
    packages=get_packages(),
    package_dir={
        "": ".",
        "cores": "./all_label_converter/cores"
    },
    package_data=get_data_files(),
    exclude_package_data=get_exclude_files(),
    classifiers=[
        "Programming Language :: Python :: 3"],
    python_requires='>=3.6.0',
    install_requires=get_requirements(REQUIREMENTS_FILE_NAME)
)
