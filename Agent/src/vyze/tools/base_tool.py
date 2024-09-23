import json
from typing import Dict, Any, Callable, Type
from functools import wraps
from pydantic import BaseModel

from typing import Callable, Dict

class Tool:
    def __init__(self, functions):
        self.functions = functions

    def __call__(self):  #convert_schema_to_function_format
        opeanai_compatible_fns = []
        for function in self.functions:
            schema = function.schema()
            function_name = schema.get('tool_name')
            description = schema.get('description')
            properties = schema.get('properties')
            required = schema.get('required', [])

            parameters = {
                "type": "object",
                "properties": {},
                "required": required
            }

            # print(properties.items())
            for prop_name, prop_details in properties.items():
                # print(prop_details)
                param = {
                    "type": prop_details['type'] if 'type' in prop_details else 'null',
                    "description": prop_details.get('description', '')
                }


                # print(param)
                if 'type' in prop_details and prop_details['type'] == 'array':
                    param['type'] = 'array'
                    param['items'] = {"type": prop_details.get('items', {}).get('type', 'string')}

                if 'enum' in prop_details:
                    param['enum'] = prop_details['enum']
                    
                if 'anyOf' in prop_details:
                    types = [sub_prop['type'] for sub_prop in prop_details['anyOf'] if 'type' in sub_prop]
                    param['type'] = types[0] if len(types) == 1 else types  
                parameters["properties"][prop_name] = param

            function_format = {
                "type": "function",
                "function": {
                    "name": function_name,
                    "description": description,
                    "parameters": parameters
                }
            }
            opeanai_compatible_fns.append(function_format)

        return opeanai_compatible_fns



def handle_tool_calls(response) -> Any:
    """Handle the tool call and execute the user-defined function."""
    tool_calls = response.choices[0].message.tool_calls
    tool_outputs = []
    for call in tool_calls:
        function_name = call.function.name
        arguments = json.loads(call.function.arguments)
        
        func = get_function(function_name)
        output = func(**arguments)
        tool_outputs.append(output)
    return tool_outputs


def validate_model(model_class: Type[BaseModel]):
    if not model_class.__doc__:
        raise ValueError(f"Model class '{model_class.__name__}' must have a docstring.")

    for field_name, field_info in model_class.__annotations__.items():
        if field_name not in model_class.__fields__:
            raise ValueError(f"Field '{field_name}' is missing in model fields.")

        field = model_class.__fields__[field_name]
        if not field.description:
            raise ValueError(f"Field '{field_name}' must have a description.")

        if not isinstance(field_info, type):
            raise ValueError(f"Field '{field_name}' must have a valid type annotation.")

    print(f"Model '{model_class.__name__}' passed validation.")



function_registry: Dict[str, Callable] = {}

def register_function(name: str, func: Callable) -> None:
    """Register a function in the central registry."""
    function_registry[name] = func

def get_function(name: str) -> Callable:
    """Retrieve a function from the central registry."""
    if name not in function_registry:
        raise ValueError(f"Function '{name}' not found in registry.")
    return function_registry[name]

def add_function(func: Callable):
    def decorator(model_class: Type[BaseModel]):
        original_schema = model_class.schema

        @wraps(original_schema)
        def new_schema(*args, **kwargs):
            schema = original_schema(*args, **kwargs)
            schema['tool_name'] = func.__name__
            return schema

        model_class.schema = new_schema

        register_function(func.__name__, func)

        return model_class
    return decorator
