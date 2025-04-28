import os
import json
import anthropic
from tools import get_tools, list_directory, read_file


class MyAgent:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
        self.tools = get_tools()
        self.messages = []

    def chat(self, user_input: str):
        self.messages.append({"role": "user", "content": user_input})
        response = self.client.messages.create(
            model="claude-3-haiku-20240307",
            messages=self.messages,
            tools=self.tools,
            max_tokens=1024,
        )
        self._handle_response(response)

    def _handle_response(self, response):
        tool_calls = [block for block in response.content if block.type == "tool_use"]

        if not tool_calls:
            text = "\n".join(block.text for block in response.content if block.type == "text")
            print(f"Claude: {text}\n")

            self.messages.append({"role": "assistant", "content": text})
            return

        for call in tool_calls:
            result = self._execute_tool(call)
            self.messages.append({"role": "assistant","content": [
                {"type": "tool_use","id": call.id,"name": call.name,"input": call.input}
            ]})
            self.messages.append({"role": "user", "content": [{"type": "tool_result", "tool_use_id": call.id, "content": json.dumps(result)}]})

        follow_up = self.client.messages.create(
            model="claude-3-haiku-20240307",
            messages=self.messages,
            max_tokens=1024,
        )
        self._handle_response(follow_up)

    def _execute_tool(self, call):
        if call.name == "list_directory":
            return list_directory()
        if call.name == "read_file":
            return read_file(call.input["filename"])

        error_msg = f"Error: the tool '{call.name} is not available."
        print(error_msg)
        return {"error": error_msg}





if __name__ == "__main__":
    agent = MyAgent()

    while True:
        try:
            user_input = input("You: ")
        except (EOFError, KeyboardInterrupt):
            print()
            break

        agent.chat(user_input)


