import os

def files_load(directory_path):
    print(f"Loading files from: {directory_path}")
    
    try:
        # Get list of filenames
        filenames = os.listdir(directory_path)
        
        full_paths = []
        for name in filenames:
            # 1. Join directory + filename -> "tiles/clip_1.tif"
            relative_path = os.path.join(directory_path, name)
            
            # 2. Convert to absolute system path -> "/Users/dipesh/.../tiles/clip_1.tif"
            absolute_path = os.path.abspath(relative_path)
            
            # Optional: Filter out hidden Mac files like .DS_Store or check valid extension
            if not name.startswith('.') and name.endswith('.tif'):
                full_paths.append(absolute_path)
        
        return (full_paths, filenames)

    except FileNotFoundError:
        print(f"The directory {directory_path} does not exist.")
        return []