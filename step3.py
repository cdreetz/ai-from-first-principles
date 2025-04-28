import os
import json
import anthropic
from tools import get_tools, list_directory, read_file


class MyAgent:
    def __init__(self):
        self.messages = None
        self.client = anthropic.Anthropic(
            api_key=os.getenv("ANTHROPIC_API_KEY")
        )
        self.user_input = ""
        self.tools = get_tools()

    def get_completion(self, user_input=None):
        if self.messages is None:
            self.messages = [
                {"role":"user", "content": user_input}
            ]
        elif user_input:
            self.messages.append({"role":"user","content": user_input})

        response = self.client.messages.create(
            model="claude-3-haiku-20240307",
            messages=self.messages,
            max_tokens=100,
            tools=self.tools
        )
        return response

    def use_tools(self, response):
        tool_calls = [content for content in response.content if content.type == "tool_use"]

        if tool_calls:
            tool_call = tool_calls[0]
            print("tool call: ", tool_call)
            tool_response = self.execute_tool(tool_call)

            assistant_content = []
            for content_item in response.content:
                if content_item.type == "text":
                    assistant_content.append({"type": "text", "text": content_item.text})
                elif content_item.type == "tool_use":
                    assistant_content.append({
                        "type": "tool_use",
                        "id": content_item.id,
                        "name": content_item.name,
                        "input": content_item.input
                    })
            self.messages.append({"role":"assistant","content": assistant_content})
            self.messages.append({"role": "user", "content": [
                {"type": "tool_result", "tool_use_id": tool_call.id, "content": json.dumps(tool_response)}
            ]})

            next_response = self.get_completion()
            has_tool_calls = any(content.type == "tool_use" for content in next_response.content)
            if has_tool_calls:
                return self.use_tools(next_response)
            else:
                final_text = next((content.text for content in next_response.content if content.type == "text"), None)
                if final_text:
                    print("Claude: " + final_text)

                return next_response
        else:
            self.messages.append({"role":"assistant", "content": response.content[0].text})
            return self.messages

    def execute_tool(self, tool_call):
        if tool_call.name == "list_directory":
            return list_directory()
        elif tool_call.name == "read_file":
            print(tool_call)
            return read_file(tool_call.input["filename"])

    def run_chat(self):
        while True:
            #prompt="i have a group of 4 python files in my dir, how many lines of code is the first one?"
            prompt = input("You: ")
            response = self.get_completion(prompt)
            tool_use_output = self.use_tools(response)
            #print(self.messages[1]["content"][0]["text"])
            print(self.messages[-1])


if __name__ == "__main__":
    myagent = MyAgent()
    myagent.run_chat()


 
