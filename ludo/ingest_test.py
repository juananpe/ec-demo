from embedchain import App
from dotenv import load_dotenv
import os
import re
import json
import requests
from datetime import datetime

load_dotenv("../.env")

#not needed but, hey here it is!
def convert_time_to_seconds(time_str):
    """Converts a time string in the format HH:MM:SS,SSS to total seconds."""
    hours, minutes, seconds = time_str.split(':')
    seconds, milliseconds = seconds.split(',')
    total_seconds = int(hours) * 3600 + int(minutes) * 60 + int(seconds)
    return total_seconds


PROMPT_WITH_HISTORY = """
  Use the following pieces of context to answer the query at the end.
  If you don't know the answer, just say that you don't know, don't try to make up an answer.
  I will provide you with our conversation history. Answer in spanish. 
  $context
  History: $history
  Query: $query
  Helpful Answer:
"""  # noqa:E501


collection_name = "jose_store"

# App config using OpenAI gpt-3.5-turbo-1106 as LLM
app_config = {
    "app": {
        "config": {
            "id": "embedchain-demo-app",
            "log_level" : "DEBUG"
        },
    },
    "llm": {
            "provider": "openai",
            "config": {
                "model": "gpt-3.5-turbo-1106",
                "prompt": PROMPT_WITH_HISTORY
            }
    },
    "vectordb": {
            "provider": "chroma",
            "config": {
                "collection_name": collection_name,
                "host": os.getenv("HOST"),
                "port": os.getenv("PORT"),
                "allow_reset": True
            }
    },
}
print(app_config)

# Uncomment this configuration to use Mistral as LLM
# app_config = {
#     "app": {
#         "config": {
#             "name": "embedchain-opensource-app"
#         }
#     },
#     "llm": {
#         "provider": "huggingface",
#         "config": {
#             "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
#             "temperature": 0.1,
#             "max_tokens": 250,
#             "top_p": 0.1
#         }
#     },
#     "embedder": {
#         "provider": "huggingface",
#         "config": {
#             "model": "sentence-transformers/all-mpnet-base-v2"
#         }
#     },
#     "vectordb": {
#         "provider": "chroma",
#         "config": {
#             "collection_name": "embedchain_store",
#             "host": "158.227.113.219",
#             "port": 8000,
#             "allow_reset": True,
#         }
#     },
# }

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

    # Extract information and create metadata

    # start_time = item["timestamp_start"]
    #start_seconds = convert_time_to_seconds(start_time)
    # item["url"] = f'{item["url"]}&t={start_seconds}s'


#    metadata = {
#        "number": item["number"],
#        "timestamp_start": item["timestamp_start"],
#        "timestamp_end": item["timestamp_end"],
#        "author": "Jose",
#        "date": date,
#        "kind": item["kind"],
#        "file_number": item["file_number"],
#        "filename": item["filename"],
#        "url": item["url"],
#    }
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

answer, sources = chatbot.chat("¿Qué es la inflación?", citations=True, session_id="ludo")
print("answer:")
print(answer)
print("sources:")
for i in sources:
  print(i)
  print(i[1]['url'])
  print(i[1]['text'])
  print(i[1]['score'])