import json

class ChatMemory:
    def __init__(self):
        self.memory = [{'role': 'system', 'content': '"You are a helpful assistant. If needed use appropriate tool wisely."'}]

    def add_message(self, role, content):
        """Adds a message with a specific role (user, assistant, system) to the memory."""
        self.memory.append({'role': role, 'content': content})

    def add_tool_message(self, role, content, tool_call_id):
        self.memory.append({'role': role, 'content': content, 'tool_call_id':tool_call_id})

    def update_system_message(self, content):
        """Updates the existing system message with new content."""
        if self.memory and self.memory[0]['role'] == 'system':
            self.memory[0]['content'] = content
        else:
            self.memory.insert(0, {'role': 'system', 'content': content})

    def get_memory(self):
        """Returns the entire chat memory."""
        return self.memory

    def clear_memory(self, keep_system_message=True):
        """Clears the memory. Keeps the system message by default unless keep_system_message is False."""
        if keep_system_message:
            self.memory = [{'role': 'system', 'content': 'You are a helpful assistant.'}]
        else:
            self.memory = []

    def last_message(self):
        """Returns the last message."""
        if self.memory:
            return self.memory[-1]
        return None

    def search_memory(self, keyword):
        """Returns all messages that contain the keyword."""
        return [msg for msg in self.memory if keyword.lower() in msg['content'].lower()]
    
    def add_response(self, response, tool_output=None):
        role, content, tool_call_ids = self.handle_response(response, tool_output)
        if tool_call_ids:
            self.memory.append(response.choices[0].message)
            for i, id in enumerate(tool_call_ids):
                self.add_tool_message(role, json.dumps(content[i]), id)
        else:
            self.add_message(role, content)
        return content
    
    def handle_response(self, response, tool_output=None):
        parsed_response = self.parse_response(response)[0]
        if parsed_response['finish_reason'] == 'stop':
            return parsed_response['role'], parsed_response['content'], None
        if parsed_response['finish_reason'] == 'function_call':
            role = 'tool'
            content = parsed_response['function_call'][0]
            return role, content
        if parsed_response['finish_reason'] == 'tool_calls':
            role = 'tool'
            # content = json.dumps({'function_name': parsed_response['tool_calls'][0].function.name, 'arguments': parsed_response['tool_calls'][0].function.arguments, 'output': tool_output})
            content = [{'function_name': tool_call.function.name, 'arguments':tool_call.function.arguments, 'output': tool_output[i]} for i, tool_call in enumerate(parsed_response['tool_calls'])]
            # print('ids', [tool_call.id for tool_call in parsed_response['tool_calls']])
            tool_call_ids = [tool_call.id for tool_call in parsed_response['tool_calls']]
            return role, content, tool_call_ids

    def parse_response(self, response):
        """Converts a ChatCompletion object to a dictionary with specific fields."""
        return [
            {
                'finish_reason': choice.finish_reason,
                'role': choice.message.role,
                'content': choice.message.content,
                'function_call': choice.message.function_call,
                'tool_calls': choice.message.tool_calls,
                'refusal': choice.message.refusal
            }
            for choice in response.choices
        ]

