import os
import json
import chromadb.utils.embedding_functions as embedding_functions
from chromadb import HttpClient
from dotenv import load_dotenv

# Load the environment variables
load_dotenv("../.env")


model = 'text-embedding-3-small' 

openai_ef = embedding_functions.OpenAIEmbeddingFunction(
                model_name=model, api_key=os.getenv("OPENAI_API_KEY")
            )


# Create a Chroma client
client = HttpClient(host="localhost", port=8000)

# Testing to ensure that the chroma server is running
print('HEARTBEAT:', client.heartbeat())

# Directory containing Jose's files
directory = '/opt/ec-demo/ludo/with_attributes_v2'


def delete_collection(collection_name):
    existing_collections = client.list_collections()
    collection_names = [collection.name for collection in existing_collections]
    
    if collection_name in collection_names:
        client.delete_collection(name=collection_name)
        print(f"Deleted existing collection: {collection_name}")
    

def ingest_files(directory, collection_name):

    existing_collections = client.list_collections()
    collection_names = [collection.name for collection in existing_collections]  # Adjusted to use a property or method
    if collection_name in collection_names:
        collection = client.get_collection(name=collection_name)
    else:
        collection = client.create_collection(name=collection_name, embedding_function=openai_ef)
   

    documents = []
    metadatas = []
    ids = []

    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            with open(os.path.join(directory, filename), 'r') as file:
                data_list = json.load(file)  # This is now a list of dictionaries
                for data in data_list:  # Iterate through each dictionary in the list
                    documents.append(data['text'])
                    metadatas.append({
                        'number' : data["number"],
                        'timestamp_start' : data["timestamp_start"],
                        'timestamp_end' : data["timestamp_end"],
                        'kind' : data["kind"],
                        'file_number' : data["file_number"],
                        'url' : data["url"]
                    })
                    ids.append(data['url'])

    
    # Add all documents, metadatas, and ids in a single call
    if documents:
        collection.add(documents=documents, metadatas=metadatas, ids=ids)
        print("All files have been ingested.")

def query_collection(collection_name, query):
    collection = client.get_collection(name=collection_name, embedding_function=openai_ef)
    result = collection.query(query_texts=[query], n_results=2)
    return result



if __name__ == "__main__":
    
    # comentar estas dos líneas para no borrar la colección
    delete_collection('jose_content')
    ingest_files(directory, 'jose_content')
    

    query = "Qué es la inflación?"
    print(query_collection('jose_content', query))
    
