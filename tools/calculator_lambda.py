import json
import math
import re

def sanitize_expression(expression):
    return re.sub(r'[^0-9+\-*/().\s]', '', expression)

def evaluate_expression(expression):
    try:
        safe_dict = {
            'abs': abs,
            'round': round,
            'max': max,
            'min': min,
            'pow': pow,
            'sqrt': math.sqrt
        }
        cleaned_expression = sanitize_expression(expression)
        result = eval(cleaned_expression, {"__builtins__": {}}, safe_dict)
        return result
    except Exception as e:
        return f"Error: Invalid expression - {str(e)}"

def lambda_handler(event, context):
    print(f"Event: {event}")
    agent = event['agent']
    actionGroup = event['actionGroup']
    function = event['function']
    parameters = event.get('parameters', {})
    print(f"Parameters: {parameters}")
    
    try:
        param_name = parameters[0].get('name')
        expression = parameters[0].get('value')
        if param_name != "expression" or not expression:
            raise ValueError("Missing expression parameter")
            
        result = evaluate_expression(expression)
        
        responseBody = {
            "TEXT": {
                "body": f"{result}"
            },
            # "PAYLOAD": {
            #     "expression": expression,
            #     "result": result
            # }
        }
        
    except Exception as e:
        responseBody = {
            "TEXT": {
                "body": f"Error calculating expression: {str(e)}"
            }
        }

    action_response = {
        'actionGroup': actionGroup,
        'function': function,
        'functionResponse': {
            'responseBody': responseBody
        }
    }

    function_response = {
        'response': action_response, 
        'messageVersion': event['messageVersion']
    }
    
    print(f"Response: {function_response}")
    return function_response
