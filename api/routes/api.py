from embedchain import App
from fastapi import APIRouter, Query, responses
from pydantic import BaseModel
import uuid
from typing import Optional
from dotenv import load_dotenv

load_dotenv(".env")

router = APIRouter()

# App config using OpenAI gpt-3.5-turbo-1106 as LLM
# app_config = {
#     "app": {
#         "config": {
#             "id": "embedchain-demo-app",
#         }
#     },
#     "llm": {
#         "provider": "openai",
#         "config": {
#             "model": "gpt-3.5-turbo-1106",
#         }
#     },
# }

# Uncomment this configuration to use Mistral as LLM
app_config = {
    "app": {
        "config": {
            "name": "embedchain-opensource-app"
        }
    },
    "llm": {
        "provider": "huggingface",
        "config": {
            "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
            "temperature": 0.1,
            "max_tokens": 250,
            "top_p": 0.1
        }
    },
    "embedder": {
        "provider": "huggingface",
        "config": {
            "model": "sentence-transformers/all-mpnet-base-v2"
        }
    }
}

ec_app = App.from_config(config=app_config)

class SourceModel(BaseModel):
    source: str


class QuestionModel(BaseModel):
    question: str
    session_id: str


@router.post("/api/v1/add")
async def add_source(source_model: SourceModel):
    """
    Adds a new source to the Embedchain app.
    Expects a JSON with a "source" key.
    """
    source = source_model.source
    try:
        ec_app.add(source)
        return {"message": f"Source '{source}' added successfully."}
    except Exception as e:
        response = f"An error occurred: Error message: {str(e)}. Contact Embedchain founders on Slack: https://embedchain.com/slack or Discord: https://embedchain.com/discord"  # noqa:E501
        return {"message": response}


@router.get("/api/v1/chat")
async def handle_chat(query: str, session_id: str = Query(None), citations: bool = False):
    """
    Handles a chat request to the Embedchain app.
    Accepts 'query' and 'session_id' as query parameters.
    """
    try:
        response = ec_app.chat(query, session_id=session_id, citations=citations)
    except Exception as e:
        response = f"An error occurred: Error message: {str(e)}. Contact Embedchain founders on Slack: https://embedchain.com/slack or Discord: https://embedchain.com/discord"  # noqa:E501
    return {"response": response}

@router.get("/api/v1/start")
async def start_session():
    """ Starts a new user session and generates a unique user token.
    """ 
    user_token = str(uuid.uuid4())
    return {'user_token': user_token}


@router.get("/api/v1/chat_history")
async def handle_chat_history():
    """
    Handles a chat history request to the Embedchain app.
    """
    try:
        app_id = ec_app.config.id
        response = ec_app.llm.memory.get(app_id=app_id, fetch_all=True, display_format=True)
    except Exception as e:
        response = f"An error occurred: Error message: {str(e)}. Contact Embedchain founders on Slack: https://embedchain.com/slack or Discord: https://embedchain.com/discord"
    return {"response": response}

@router.get("/")
async def root():
    return responses.RedirectResponse(url="/docs")
