from langchain_openai import OpenAIEmbeddings

from langchain_mongodb import MongoDBAtlasVectorSearch
from pymongo import MongoClient

from langchain_mongodb.retrievers.hybrid_search import MongoDBAtlasHybridSearchRetriever

client = MongoClient("mongodb://user:pass@localhost:27017/?directConnection=true")

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

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

documents = vector_store.similarity_search_with_score("第一百二十条之二", k=10)

for doc, score in documents:
   print(score, doc.page_content)
