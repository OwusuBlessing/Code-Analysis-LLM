import os
from config import CODE_EXTENSIONS, DOWNLOAD_REPO_DIRECTORY


def read_code_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except Exception as e:
        # Handle file reading errors
        return f"Error reading file: {e}"


def create_individual_document(file_path, content):
    folder_path, file_name_with_extension = os.path.split(file_path)
    file_name, file_extension = os.path.splitext(file_name_with_extension)

    # Concatenate file_name and file_extension to include extension in filename
    full_file_name = f"{file_name}{file_extension}"

    document = {
        "file_name": full_file_name,
        "folder_path": folder_path,
        "content": content
    }
    return document


def process_folder_for_individual_docs(folder_path, code_extensions=CODE_EXTENSIONS):
    documents = []
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isdir(item_path):
            documents.extend(process_folder_for_individual_docs(item_path, code_extensions))
        else:
            _, file_extension = os.path.splitext(item)
            if file_extension in code_extensions:
                content = read_code_file(item_path)
                if content:
                    document = create_individual_document(item_path, content)
                    documents.append(document)
    return documents



