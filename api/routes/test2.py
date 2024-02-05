from embedchain import App
from embedchain.loaders.jsrt import JsrtLoader
from dotenv import load_dotenv
import os

load_dotenv("../.env")
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
            }
    },
    "vectordb": {
            "provider": "chroma",
            "config": {
                "collection_name": "jose_store",
                "host": os.getenv("HOST"),
                "port": os.getenv("PORT"),
                "allow_reset": True
            }
    },
}


chatbot = App.from_config(config=app_config)
chatbot.config.logger.parent.setLevel("DEBUG")

loader = JsrtLoader()

chatbot.add("http://192.168.1.140:9000/1%202%20Inflaci%C3%B3n-wav.json", data_type="jsrt", loader=loader)

# chatbot.query("What is Embedchain?")
