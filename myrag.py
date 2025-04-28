import os
import anthropic
import chromadb
from create_vdb import create_my_collection, create_new_collection
os.environ["TOKENIZERS_PARALLELISM"] = "false"

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
collection = create_new_collection()

def get_content(prompt):
    results = collection.query(query_texts=[prompt],n_results=2)
    return results["documents"]

def get_completion(prompt, content):
    response = client.messages.create(
        model="claude-3-haiku-20240307",
        system="you are a helpful assistant who has some additional documents to help answer user questions",
        messages=[
            {"role":"user", "content":f"User prompt:{prompt}\n\nDocuments:{content}"},
        ],
        max_tokens=100
    )
    return response.content[0].text




if __name__ == "__main__":
    prompt=input("You: ")
    documents = get_content(prompt)
    out = get_completion(prompt, documents)
    print("\nAI: ",out)
 
