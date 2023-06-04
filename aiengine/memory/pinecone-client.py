# import os
# from dotenv import load_dotenv
# load_dotenv()
# import openai
# import pinecone as pinecone
# import requests
# import json
# import unittest

# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
# PINECONE_NAMESPACE = "tht_namespace"

# # Initialize OpenAI API
# openai.api_key = OPENAI_API_KEY
# print(OPENAI_API_KEY, PINECONE_API_KEY, PINECONE_NAMESPACE)
# # Initialize Pinecone
# pinecone.init(api_key=PINECONE_API_KEY,  environment="DEV")
# #pinecone.deinit()

# # Ensure Pinecone namespace exists
# pinecone.create_namespace(namespace_name=PINECONE_NAMESPACE)

# print("pinecone namespace created")

# def __init__

# def embed_text(text):
#     # Request GPT-3 embeddings
#     url = "https://api.openai.com/v1/engines/davinci-codex/completions"
#     headers = {"Content-Type": "application/json", "Authorization": f"Bearer {OPENAI_API_KEY}"}
#     data = {
#         "prompt": f"Embed the following text: {text}",
#         "max_tokens": 16,
#         "n": 1,
#         "stop": None,
#         "temperature": 0.5,
#     }

#     response = requests.post(url, headers=headers, json=data)
#     response_json = response.json()
#     embeddings = response_json["choices"][0]["text"].strip()

#     # Store embeddings in Pinecone
#     with pinecone.deinit():
#         pinecone.namespace(PINECONE_NAMESPACE)
#         pinecone.upsert(items={text: embeddings})

# def search_text(query_text):
#     # Get query_text embeddings
#     query_embeddings = embed_text(query_text)

#     # Search in Pinecone
#     with pinecone.deinit():
#         pinecone.namespace(PINECONE_NAMESPACE)
#         results = pinecone.fetch(ids=[query_text])

#     return results

# # Example usage:
# text_to_embed = "This is an example text."
# embed_text(text_to_embed)

# query = "Find similar text to this example."
# search_results = search_text(query)

# print("Search results:")
# for text, similarity_score in search_results.items():
#     print(f"Text: {text}, Similarity score: {similarity_score}")

# # Cleanup Pinecone namespace
# pinecone.deinit()
# pinecone.delete_namespace(namespace_name=PINECONE_NAMESPACE)


# class TestEmbedAndSearch(unittest.TestCase):

#     def test_embed_and_search(self):
#         # Embed a sample text
#         sample_text = "This is a sample text for testing."
#         embed_text(sample_text)

#         # Search for a similar text
#         query_text = "Find a similar text to this test."
#         search_results = search_text(query_text)

#         # Check if the sample_text is in the search results
#         self.assertIn(sample_text, search_results)

#         # Check if the similarity score is within an acceptable range
#         similarity_score = search_results[sample_text]
#         self.assertGreater(similarity_score, 0.75, "Similarity score is too low.")
#         self.assertLess(similarity_score, 1.0, "Similarity score is too high.")


# if __name__ == "__main__":
#     unittest.main()