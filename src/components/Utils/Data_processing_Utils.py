"""
Module for processing the data

Author: Arkaan Quanunga
Date: 14/03/2022
"""

import os
import json
from collections import defaultdict


def create_directory(directory_name):
    """
    Creates a directory if the directory does not exist already

    :param directory_name: The directory name to be created
    :return:
    """
    try:
        assert isinstance(directory_name, str)
    except AssertionError:
        print("{}, is not of type string".format(directory_name))

    if not os.path.exists(directory_name):
        os.mkdir(directory_name)


def process_files(output_directory, data_dir):
    """
    Processes the Json files by separating the data based on resource types

    :param output_directory: The output directory to put the processed data
    :param data_dir: The directory of unprocessed FHIR data
    :return:
    """
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            with open(os.path.join(root, file), 'r') as f:

                # Reading the file
                extracted_data = json.load(f)

                # Extracting entries of the file
                entries = extracted_data['entry']

                # Creating set & dictionary
                resource_types = set()
                entry_resources = defaultdict(list)

                # Extracting data to dictionary based on resource type
                for resource in entries:
                    resource_type = resource["resource"]["resourceType"]
                    resource_types.add(resource_type)
                    resource_file_path = output_directory + \
                        "/" + f"{resource_type}.json"
                    entry_resources[resource_file_path].append(resource)

                for resource_file_path, resources in entry_resources.items():
                    if os.path.exists(resource_file_path):
                        # Getting existing contents of each resource
                        with open(resource_file_path, 'r') as i:
                            contents = json.load(i)

                        contents.extend(resources)
                    else:
                        contents = resources

                    # Saving it to output dir
                    with open(resource_file_path, 'w') as j:
                        json.dump(contents, j)
