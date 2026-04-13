from openai import OpenAI
import json
from dotenv import load_dotenv
from pprint import pprint

local_model = "gemma4:latest"
client=OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="not-needed"
)


def recommend(topic, sub_topic="Unknown"):
    """Give a recommendation for any topic"""
    if topic is not None:
        if "movie" in topic.lower():
            return json.dumps({"topic": "movie",
                            "sub_topic": sub_topic})
        elif "recipe" in topic.lower():
            return json.dumps({"topic": "recipe",
                            "sub_topic": sub_topic})
        elif "gift" in topic.lower():
            return json.dumps({"topic": "gift",
                            "sub_topic": sub_topic})
        else:
            return json.dumps({"topic": topic})
    

def run_conversation():
    # Step 1: send the conversation and available functions to the model
    user = """Can you please make recommendations for the following and also consider the sub topic mentioned about them:
    1. Movies about history.
    2. Recipes about sweet dish.
    3. Gifts for Parents."""
    messages = [
        {"role": "user", "content": user}
    ]
    tools = [
        {
            "type": "function",
            "function": {
                "name": "recommend",
                "description": "Provide a recommendation for any topic considering the sub topic about them",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "topic": {
                            "type": "string",
                            "description": "The topic, a user wants a recommnedation for.",
                            },
                        "sub_topic": {
                            "type": "string",
                            "description": "The sub topic of the topic that this recommendation will be given."
                            },
                        },
                    "required": ["topic", "sub_topic"],
                    },
                },
            }
        ]
    response = client.chat.completions.create(
        model=local_model,
        messages=messages,
        tools=tools,
        tool_choice="auto",  # auto is default, but we'll be explicit
        temperature=0
    )
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls

    print("\n*****------------------------------------------------------------------------------*****")
    if tool_calls:
        for tool_call in tool_calls:
            print("\n")
            print(tool_call)
    print("\n*****------------------------------------------------------------------------------*****")

    # Step 2: check if the model wanted to call a function
    if tool_calls:
        # Step 3: call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
        available_functions = {
            "recommend": recommend,
        }  # only one function in this example, but you can have multiple
        messages.append(response_message)  # extend conversation with assistant's reply
        # Step 4: send the info for each function call and function response to the model
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(
                topic=function_args.get("topic"),
                sub_topic=function_args.get("sub_topic"),
            )
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )  # extend conversation with function response
        second_response = client.chat.completions.create(
            model=local_model,
            messages=messages,
            temperature=0
        )  # get a new response from the model where it can see the function response
        return second_response.choices[0].message.content

print(run_conversation())