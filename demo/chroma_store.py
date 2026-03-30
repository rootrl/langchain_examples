from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_chroma import Chroma

file_path = "../data/naval.pdf"
loader = PyPDFLoader(file_path)

docs = loader.load()

print(len(docs))


# splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200, add_start_index=True
)
all_splits = text_splitter.split_documents(docs)

print(len(all_splits))

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

vector_1 = embeddings.embed_query(all_splits[0].page_content)
vector_2 = embeddings.embed_query(all_splits[1].page_content)

assert len(vector_1) == len(vector_2)
print(f"Generated vectors of length {len(vector_1)}\n")
print(vector_1[:10])


# DB
vector_store = Chroma(
    collection_name="example_collection",
    embedding_function=embeddings,
    host="localhost",
    port=8000,
    ssl=False
)

ids = vector_store.add_documents(documents=all_splits)


results = vector_store.similarity_search_with_score("how to reading?")
doc, score = results[0]
print(f"Score: {score}\n")
print(doc)
