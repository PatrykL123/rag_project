import hashlib 
import json
import os 
import glob 

def hash_file(file_path):
    hasher = hashlib.sha256()

    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(8192)
            if not chunk:
                break
            hasher.update(chunk)

    return hasher.hexdigest()


def get_new_files(directory_path: str, tracker_file: str ="data/processed_files.json") -> list:


    """
    Scans a folder and returns a list of paths to PDF files
    that are new or have been modified since the last run.
    """

    try:
        with open(tracker_file, 'r') as f:
            processed_files = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        processed_files = {}
    
    files_to_process = []

    files_found = glob.glob(f"{directory_path}/*.pdf")

    if not files_found:
        print("No files found")
        return []


    for filename in files_found: 

        file_hash = hash_file(filename)

        if filename not in processed_files or processed_files[filename] != file_hash:

            files_to_process.append(filename)

    return files_to_process



def update_tracker(processed_files_list: list, tracker_file: str ="data/processed_files.json") -> None:

    """
    Updates the JSON file with new hashes ONLY for those files
    that were successfully processed and added to the vector database.
    """


    if not processed_files_list:
        print("No new files to update")
        return
    

    try:
        with open(tracker_file, "rb") as f:
            processed_files = json.load(f)

    except (FileNotFoundError, json.JSONDecodeError):
        processed_files = {}



    for filename in processed_files_list:

        processed_files[filename] = hash_file(filename)



    with open(tracker_file, "w") as f:

        json.dump(processed_files, f, indent = 4)

    print(f"Tracker Updated sucessfully! Added/changed {len(processed_files_list)} files.")

        

    