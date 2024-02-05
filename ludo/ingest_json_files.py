from embedchain import App
from dotenv import load_dotenv
import os
import re
import json
import requests
from datetime import datetime

load_dotenv("../.env")


import yaml

# Open the YAML file
with open('ec_app.yaml', 'r') as file:
    app_config = yaml.safe_load(file)


print(app_config)


chatbot = App.from_config(config=app_config)
# chatbot.config.logger.parent.setLevel("DEBUG")


# URL of the JSON data
url = 'http://127.0.0.1:9000/1%201%20Planteando%20objetivos%20politica%20economica-wav.json'

# Send a GET request to the URL to get the json data
response = requests.get(url)

# Make sure the request was successful
if response.status_code == 200:
    # Parse the JSON content
    data = response.json()
    print(f"File {url} has been loaded successfully. Number of items: {len(data)}" )
    # Now data is loaded and can be used as shown in the previous examples
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")


# RESET THE DATABASE collection
# chatbot.db.reset()

date = datetime.today().strftime('%Y-%m-%d')
for item in data:
    print("adding item to database:")
    print(item["text"])
    metadata=item
    try:
        chatbot.add( item["text"],  data_type="text", metadata = metadata)
        print("item added to database") 
    except Exception as e:
        print(f"Failed to add item to database: {e}")

# context = chatbot.search("¿Qué es la inflación?", num_documents=5)
# print(json.dumps(context))

answer, sources = chatbot.chat("¿porqué existe conflicto entre inflación y pleno empleo?", citations=True, session_id="ludo")
print("answer:")
print(answer)
print("sources:")
for i in sources:
  print(i)
  print(i[1]['url'])
  print(i[1]['text'])
  print(i[1]['score'])