import os
import anthropic

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def get_completion(prompt):
    response = client.messages.create(
        model="claude-3-haiku-20240307",
        system="you are a helpful assistant",
        messages=[
            {"role":"user", "content":prompt},
        ],
        max_tokens=100
    )
    return response.content[0].text


if __name__ == "__main__":
    prompt="what is 2+2?"
    out = get_completion(prompt)
    print(out)
 
