import openai
import os
from vyze.memory.basic_memory import ChatMemory
from vyze.tools.base_tool import handle_tool_calls

class ChatOpenAI:
    def __init__(self,
                 api_key=None,
                 model_name='gpt-4o-mini', 
                 memory: bool = False,
                 tools: list = None,
                 temperature=0.2, 
                 max_tokens=1500):
        """
        Initializes the ChatOpenAI class for interacting with the OpenAI API.

        Parameters:
        - api_key (str): Your OpenAI API key. If not provided, it will be fetched from the OPENAI_API_KEY environment variable.
        - model_name (str): The model to use. Default is 'gpt-4o-mini'.
        - temperature (float): Sampling temperature. Default is 0.2.
        - max_tokens (int): Maximum number of tokens to generate in the response. Default is 1500.
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        
        if not self.api_key:
            raise ValueError("API key must be provided either via argument or 'OPENAI_API_KEY' environment variable.")
        
        self.model_name = model_name
        self.memory = memory
        self.tools = tools
        self.temperature = temperature
        self.max_tokens = max_tokens

        if self.memory:
            self.chat_memory = ChatMemory()

    def run(self, prompt, system_message=None):
        if not self.memory:
            messages=[
                {"role": "system", "content": system_message or "You are a helpful assistant. If needed use appropriate tool wisely."},
                {"role": "user", "content": prompt}
            ]
        else:
            if system_message:
                self.chat_memory.update_system_message(system_message)
            if prompt:
                self.chat_memory.add_message('user', prompt)
                
            messages = self.chat_memory.get_memory()
        response=None
        # print(self.tools)
        # try:
        response = openai.chat.completions.create(
            model=self.model_name,
            messages=messages,
            tools= self.tools
        )
        # except Exception as e:
        #     print("Error: ", e)
            # print(response)
            # print(response.choices[0].finish_reason)
            
        tool_outputs = None
        if response.choices[0].finish_reason == 'function_call' or response.choices[0].finish_reason=='tool_calls':
            tool_outputs = handle_tool_calls(response)

        if self.memory:
            self.chat_memory.add_response(response, tool_outputs)

        return response.choices[0].message.content or tool_outputs

    def clear_memory(self, keep_system_message=True):
        """Clears the memory in ChatMemory if memory is enabled."""
        if self.memory and self.chat_memory:
            self.chat_memory.clear_memory(keep_system_message=keep_system_message)

    def search_memory(self, keyword, exact_match=False):
        """Searches the memory in ChatMemory if memory is enabled."""
        if self.memory and self.chat_memory:
            return self.chat_memory.search_memory(keyword, exact_match=exact_match)
        return []

    def last_message(self):
        """Returns the last message from ChatMemory if memory is enabled."""
        if self.memory and self.chat_memory:
            return self.chat_memory.last_message()
        return None
    
    def update_system_message(self, content):
        self.chat_memory.update_system_message(content)



    def get_config(self):
        """
        Returns a masked configuration of the API key and other parameters.
        """
        masked_api_key = '*' * (len(self.api_key) - 4) + self.api_key[-4:] if self.api_key else None
        return {
            'api_key': masked_api_key,
            'model_name': self.model_name,
            'temperature': self.temperature,
            'max_tokens': self.max_tokens
        }
