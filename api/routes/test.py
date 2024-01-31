from embedchain import App
from dotenv import load_dotenv
import os

load_dotenv(".env")


PROMPT_WITH_HISTORY = """
  Use the following pieces of context to answer the query at the end.
  If you don't know the answer, just say that you don't know, don't try to make up an answer.
  I will provide you with our conversation history.

  $context

  History: $history

  Query: $query

  Helpful Answer:
"""  # noqa:E501

# App config using OpenAI gpt-3.5-turbo-1106 as LLM
app_config = {
    "app": {
        "config": {
            "id": "embedchain-demo-app",
            "log_level" : "WARNING"
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
                "collection_name": "testing",
                "host": os.getenv("HOST"),
                "port": os.getenv("PORT"),
                "allow_reset": True
            }
    },
}

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
#             "allow_reset": True
#         }
#     },
# }

elon_bot = App.from_config(config=app_config)

# Embed online resources
# elon_bot.add("https://www.eldiario.es/politica/gobierno-da-garantizada-legislatura-aprobacion-amnistia-pese-no-junts-congreso_1_10881377.html")
elon_bot.add("https://en.wikipedia.org/wiki/Elon_Musk")
#elon_bot.add("https://www.forbes.com/profile/elon-musk")

# Query the bot
# print(elon_bot.query("How many companies does Elon Musk run and name those?"))
# Answer: Elon Musk currently runs several companies. As of my knowledge, he is the CEO and lead designer of SpaceX, the CEO and product architect of Tesla, Inc., the CEO and founder of Neuralink, and the CEO and founder of The Boring Company. However, please note that this information may change over time, so it's always good to verify the latest updates.

# response = ec_app.chat(query, session_id=session_id, citations=citations)

#from embedchain.config import BaseLlmConfig
#query_config = BaseLlmConfig(number_documents=5)

answer, sources = elon_bot.chat("Qué ha ocurrido con la ley de amnistía?", citations=True, session_id="new_session_id")
# answer, sources = elon_bot.chat("Who is Elon Musk?", citations=True)
print(answer)
# print(sources)

# print urls of lista
for i in sources:
    print(i[1]['url'])