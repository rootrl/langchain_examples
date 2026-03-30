from langchain_community.document_loaders import PyPDFLoader

file_path = "../data/naval.pdf"
loader = PyPDFLoader(file_path)

docs = loader.load()

print(len(docs))

print(docs[0])
