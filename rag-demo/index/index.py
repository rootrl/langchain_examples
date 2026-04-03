from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from uuid import uuid4

from langchain_mongodb import MongoDBAtlasVectorSearch
from pymongo import MongoClient

client = MongoClient("mongodb://user:pass@localhost:27017/?directConnection=true")

file_path = "../data/law.pdf"
loader = PyPDFLoader(file_path)

docs = loader.load()


# splitter

legal_separators = [
    r"\n第[一二三四五六七八九十百千]+章",    # 章
    r"\n第[一二三四五六七八九十百千]+节",    # 节
    r"\n第[一二三四五六七八九十百千]+条",    # 条
    r"\n（[一二三四五六七八九十]+）",         # 款（以中文括号数字开头）
    r"\n[一二三四五六七八九十]+、",           # 有序列表
    r"\n",                                    # 普通换行
]
text_splitter = RecursiveCharacterTextSplitter(
    separators=legal_separators,
    is_separator_regex=True,
    chunk_size=1500, 
    chunk_overlap=200, 
    keep_separator=True, 
)

all_splits = text_splitter.split_documents(docs)

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

vector_store.create_vector_search_index(dimensions=1536)

uuids = [str(uuid4()) for _ in range(len(all_splits))]
vector_store.add_documents(documents=all_splits, ids=uuids)
