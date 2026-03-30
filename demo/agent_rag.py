from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.tools import tool

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

vector_store = Chroma(
    collection_name="example_collection",
    embedding_function=embeddings,
    host="localhost",
    port=8000,
    ssl=False
)

@tool(description="get information from verctor DB server")
def search_document(s: str) -> str:
    """ get infomation from vector DB server """
    results = vector_store.similarity_search_with_score(s)
    return str(results)

model = ChatOpenAI(
    model="gpt-5.4-nano",
    temperature=0.1,
    max_tokens=1000,
    timeout=30,
)

agent = create_agent(
    model,
    tools=[search_document],
    system_prompt="You are a Local RAG assistant, search document from vector DB server, if there's no result, Just say you dont't know",
)

# Run the agent
response = agent.invoke(
    {"messages": [{"role": "user", "content": "how to read?"}]}
)

print(response)
