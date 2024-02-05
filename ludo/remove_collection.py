
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

def remove_database_collection( yaml_file_path):
   
    # Open the YAML file
    with open(yaml_file_path, 'r') as file:
        app_config = yaml.safe_load(file)
    
    chatbot = App.from_config(config=app_config)
 
    #RESET THE DATABASE collection
    chatbot.db.reset()
    print(f"Database collection has been reset: {app_config['vectordb']['config']['collection_name']} ")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py  <config_yaml_file>")
        sys.exit(1)
    
    yaml_file_path = sys.argv[1]
    
    remove_database_collection(yaml_file_path)
    

