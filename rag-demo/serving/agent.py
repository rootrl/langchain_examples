from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from langchain_mongodb import MongoDBAtlasVectorSearch
from pymongo import MongoClient
from langchain_openai import OpenAIEmbeddings
from langchain_core.tools import tool

from langchain_mongodb.retrievers.hybrid_search import MongoDBAtlasHybridSearchRetriever

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

client = MongoClient("mongodb://user:pass@localhost:27017/?directConnection=true")

DB_NAME = "langchain_test_db"
COLLECTION_NAME = "langchain_test_vectorstores"
ATLAS_VECTOR_SEARCH_INDEX_NAME = "langchain-test-index-vectorstores"

MONGODB_COLLECTION = client[DB_NAME][COLLECTION_NAME]

vector_store = MongoDBAtlasVectorSearch(
    collection=MONGODB_COLLECTION,
    embedding=embeddings,
    index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME,
    relevance_score_fn="cosine",
)

app = FastAPI()

# Set up your client/origin
origins = [
    "http://localhost.example.com",
    "https://localhost.example.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@tool(description="get law information from verctor DB server")
def search_document(s: str) -> str:
    """ get law infomation from vector DB server """
    results = vector_store.similarity_search_with_score(s)
    return str(results)


model = ChatOpenAI(
    model="gpt-5.4-nano",
    temperature=0.1,
    max_tokens=3000,
    timeout=30,
)

agent = create_agent(
    model,
    tools=[search_document],
    system_prompt="你是一个《中华人民共和国刑法》刑法助手，search_document工具就是搜索《中华人民共和国刑法》的，请回答用户关于法律的提问（都试作询问《中华人民共和国刑法》）,请优先保证提供法律原文",
)
