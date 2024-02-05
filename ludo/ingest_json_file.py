from embedchain import App
from dotenv import load_dotenv
import os
import re
import json
import requests
from datetime import datetime
import sys

import yaml

load_dotenv("../.env")

def ingest_json_file(json_file_path, yaml_file_path):
    # Open the JSON file
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    
    # Open the YAML file
    with open(yaml_file_path, 'r') as file:
        app_config = yaml.safe_load(file)
    
    chatbot = App.from_config(config=app_config)
    
    date = datetime.today().strftime('%Y-%m-%d')
    for item in data:
        metadata=item
        try:
            chatbot.add( item["text"],  data_type="text", metadata = metadata)
        except Exception as e:
            print(f"Failed to add item to database: {e}")

    print(f"File {json_file_path} has been loaded successfully. Number of items: {len(data)}" )

# RESET THE DATABASE collection
# chatbot.db.reset()




def validate_files(json_file_path, yaml_file_path):
    # Check if JSON file exists
    if not os.path.exists(json_file_path):
        print(f"JSON file not found: {json_file_path}")
        return False

    # Check if YAML file exists
    if not os.path.exists(yaml_file_path):
        print(f"YAML file not found: {yaml_file_path}")
        return False
    
    # Basic validation of YAML content
    try:
        with open(yaml_file_path, 'r') as yaml_file:
            yaml_content = yaml.safe_load(yaml_file)
            print("YAML file is valid.")
    except yaml.YAMLError as e:
        print(f"Error reading YAML file: {e}")
        return False
    
    return True

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_json_file> <config_yaml_file>")
        sys.exit(1)
    
    json_file_path, yaml_file_path = sys.argv[1], sys.argv[2]
    
    if validate_files(json_file_path, yaml_file_path):
        ingest_json_file(json_file_path, yaml_file_path)
    else:
        sys.exit(1)
