from pymongo.mongo_client import MongoClient
from pymongo.operations import SearchIndexModel
import time

# Connect to your deployment
uri = "mongodb://root:example@localhost:27017/"
client = MongoClient(uri)

# Access your database and collection
database = client["langchain_test_db"]
collection = database["langchain_test_vectorstores"]

# Create your index model, then create the search index
search_index_model = SearchIndexModel(
  definition={
    "fields": [
      {
        "type": "vector",
        "numDimensions": 1536,
        "path": "embedding",
        "similarity": "euclidean | cosine | dotProduct"
      }
    ]
  },
  name="langchain-test-index-vectorstores",
  type="vectorSearch"
)

result = collection.create_search_index(model=search_index_model)
print("New search index named " + result + " is building.")

# Wait for initial sync to complete
print("Polling to check if the index is ready. This may take up to a minute.")
predicate=None
if predicate is None:
  predicate = lambda index: index.get("queryable") is True

while True:
  indices = list(collection.list_search_indexes(result))
  if len(indices) and predicate(indices[0]):
    break
  time.sleep(5)
print(result + " is ready for querying.")

client.close()

