import shutil
import os

def delete_and_create_folder(folder_path):
    """
    Deletes a folder if it exists and creates a new one with the same name.

    Parameters:
    - folder_path (str): The path to the folder.

    Returns:
    - str: The path to the newly created folder.
    """
    # Check if the folder exists
    if os.path.exists(folder_path):
        # If it exists, delete the folder and its contents
        try:
            shutil.rmtree(folder_path)
            print(f"Deleted existing folder and its contents: {folder_path}")
        except OSError as e:
            print(f"Error deleting folder: {e}")

    # Create a new folder with the same name
    try:
        os.makedirs(folder_path)
        print(f"Created new folder: {folder_path}")
    except OSError as e:
        print(f"Error creating folder: {e}")

    return folder_path
