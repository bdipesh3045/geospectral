import os

def files_load(file_path):
    print(f"Loading files from: {file_path}")
    """Load and return a list of file names in the given directory."""
    try:
        files = os.listdir(file_path)
        return files
    except FileNotFoundError:
        print(f"The directory {file_path} does not exist.")
        return []