import os

from settings import DATA_FOLDER, DATASETS


def check_if_data():
    """This function is used to check if data are placed """
    data_folder_files = os.listdir(DATA_FOLDER)

    if DATASETS['metadata'] in data_folder_files and DATASETS['keywords'] in data_folder_files and DATASETS[
        'credits'] in data_folder_files:
        return True
    else:
        return False


def create_output_folder():
    """This function us used to crete the output folder"""
    if not os.path.exists('output'):
        os.makedirs('output')