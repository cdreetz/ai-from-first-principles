import os
import openai
from pydantic import BaseModel

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class EmailModel(BaseModel):
    sender: str
    recipient: str
    #time_sensitive: bool
    #spam: bool


def get_completion(email):
    response = client.responses.parse(
        model="gpt-4o",
        input=[
            {"role": "system", "content": "extract the name of the sender and recipient from this email. your output should be valid json"},
            {"role": "user", "content": email},
        ],
        text_format=EmailModel,
    )

    return response.output[0].content[0].text












if __name__ == "__main__":
    email = "hey richard, yeah i can do a talk. can i do it on building ai stuff without any frameworks or libraries?  i feel like people focus too much on them and not just understanding whats going on.  thanks, christian "
    out = get_completion(email)
    print(out)

