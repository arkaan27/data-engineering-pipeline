import os
from src.components.Utils.Data_processing_Utils import process_files, create_directory


def test_create_directory():
    """
    Creates a sample test directory and checks whether it exists or not
    :return:
    """
    output_directory = "test"
    create_directory(output_directory)

    assert os.path.exists(output_directory)


def test_process_files():
    """

    :return:
    """

