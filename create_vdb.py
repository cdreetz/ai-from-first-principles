import os
import chromadb
import requests
os.environ["TOKENIZERS_PARALLELISM"] = "false"

chroma_client = chromadb.Client()

def create_my_collection(name):
    return chroma_client.get_or_create_collection(name="my_collection")


def fetch_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except Exception as e:
        raise Exception(f"Error fetching HTML: {str(e)}")


def create_new_collection():
    my_urls = [
        "https://www.creetz.com/",
        "https://www.creetz.com/resume.html"
    ]
    my_documents = []
    my_ids = []
    for i, url in enumerate(my_urls):
        my_documents.append(fetch_html(url))
        my_ids.append(f"id{i}")

    collection = chroma_client.get_or_create_collection(name="my_collection")
    collection.upsert(
        documents=my_documents,
        ids=my_ids
    )
    return collection

