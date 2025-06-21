import os
import json
import hashlib
from datetime import datetime

METADATE_FILE = "data/metadate.json"

if not os.path.exists(METADATE_FILE) :
    with open(METADATE_FILE, "w") as f:
        json.dump([], f)

def load_metadata():
    with open(METADATE_FILE, "r") as f:
        return json.load(f)

def save_metadata(metadata_list):
    with open(METADATE_FILE, "w") as f:
        json.dump(metadata_list, f, indent=4)


def calculate_file_hash(content):
    return hashlib.sha256(content).hexdigest()

def add_metadata(filename, encrypted_filename, content):
    metadata_list = load_metadata()
    file_hash = calculate_file_hash(content)
    base_name = os.path.basename(filename)

    matching_files = [entry for entry in metadata_list if entry["original_filename"] == base_name ]

    for entry in matching_files : 
        if entry["file_hash"] == file_hash:
            print("⚠️ This exact file version already exists. Skipping metadata entry.")
            return
        
    version = 1
    if matching_files:
        latest_version = max(entry["version"] for entry in matching_files)
        version = latest_version + 1

    file_info = {
        "original_filename" : os.path.basename(filename),
        "encrypted_filename": os.path.basename(encrypted_filename),
        "file_size": len(content),
        "date_added": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "file_hash" : calculate_file_hash(content),
        "version": version
    }
    
    metadata_list.append(file_info)
    save_metadata(metadata_list)

