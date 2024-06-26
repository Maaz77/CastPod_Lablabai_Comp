
#!pip install datasets

from datasets import load_dataset
docs = load_dataset(f"Cohere/wikipedia-22-12-it-embeddings", split="train")

from datasets import load_dataset
docs = load_dataset(f"Cohere/wikipedia-22-12-it-embeddings", split="train", streaming=True)

# for doc in docs:
#     docid = doc['id']
#     title = doc['title']
#     text = doc['text']
#     emb = doc['emb']

# cFOpZHszHLRa0KBUKO1nWN04Qg2YpqNbuNfcPp1r

#Run: pip install cohere datasets
from datasets import load_dataset
import torch
import cohere

co = cohere.Client(f"cFOpZHszHLRa0KBUKO1nWN04Qg2YpqNbuNfcPp1r")  # Add your cohere API key from www.cohere.com

#Load at max 1000 documents + embeddings
max_docs = 1000
docs_stream = load_dataset(f"Cohere/wikipedia-22-12-it-embeddings", split="train", streaming=True)

docs = []
doc_embeddings = []

for doc in docs_stream:
    docs.append(doc)
    doc_embeddings.append(doc['emb'])
    if len(docs) >= max_docs:
        break

doc_embeddings = torch.tensor(doc_embeddings)

query = 'Who founded Youtube'
response = co.embed(texts=[query], model='multilingual-22-12')
query_embedding = response.embeddings
query_embedding = torch.tensor(query_embedding)

# Compute dot score between query embedding and document embeddings
dot_scores = torch.mm(query_embedding, doc_embeddings.transpose(0, 1))
top_k = torch.topk(dot_scores, k=3)

# Print results
print("Query:", query)
for doc_id in top_k.indices[0].tolist():
    print(docs[doc_id]['title'])
    print(docs[doc_id]['text'], "\n")