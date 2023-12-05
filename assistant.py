from openai import OpenAI
import os
import json
import time
import argparse
from dotenv import load_dotenv
from handlers import tool_handlers, assistant_tools


def create_assistant():
    assistant = client.beta.assistants.create(
        name="General Weather Assistant",
        instructions='''You are a friendly assistant that tells me the weather in a location:
                        You have these weather codes: WMO Weather interpretation codes (WW)
                        Code	Description
                        0	Clear sky
                        1, 2, 3	Mainly clear, partly cloudy, and overcast
                        45, 48	Fog and depositing rime fog
                        51, 53, 55	Drizzle: Light, moderate, and dense intensity
                        56, 57	Freezing Drizzle: Light and dense intensity
                        61, 63, 65	Rain: Slight, moderate and heavy intensity
                        66, 67	Freezing Rain: Light and heavy intensity
                        71, 73, 75	Snow fall: Slight, moderate, and heavy intensity
                        77	Snow grains
                        80, 81, 82	Rain showers: Slight, moderate, and violent
                        85, 86	Snow showers slight and heavy
                        95 *	Thunderstorm: Slight or moderate
                        96, 99 *	Thunderstorm with slight and heavy hail
                        (*) Thunderstorm forecast with hail is only available in Central Europe''',
        tools=assistant_tools,
        model="gpt-4-1106-preview"
    )
    print("Assistant created")
    print(assistant.id)
    return assistant


def call_tool_function(tool_call_function_name, tool_call_arguments_json):
    if tool_call_function_name in tool_handlers:
        return tool_handlers[tool_call_function_name](tool_call_arguments_json)
    else:
        raise Exception(f"Unknown function name: {tool_call_function_name}")


async def ask_assistant(client, assistant_id, user_message):
    
    thread = client.beta.threads.create()

    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_message,
    )


    message = client.beta.threads.messages.retrieve(
        thread_id=thread.id,
        message_id=message.id,
    )


    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
    )

    # Use a while loop to check if the run is completed
    while True:
        retrieved_run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )

        if retrieved_run.status == "completed":
            break

        if retrieved_run and retrieved_run.required_action and retrieved_run.required_action.submit_tool_outputs:
            tool_call = retrieved_run.required_action.submit_tool_outputs.tool_calls[0]
            tool_call_id = tool_call.id
            tool_call_function = tool_call.function
            tool_call_arguments = tool_call_function.arguments
            tool_call_arguments_json = json.loads(tool_call_arguments)
            tool_call_function_name = tool_call_function.name

            # Call the API
            tool_call_arguments_json = json.loads(tool_call.function.arguments)
            print(tool_call_function_name)
            print(tool_call_arguments_json)
            # Call the appropriate handler function
            weather_data = call_tool_function(tool_call_function_name, tool_call_arguments_json)
            print(weather_data)
            # Create a new message to the assistant with the weather data and ask for a concise summary
            run = client.beta.threads.runs.submit_tool_outputs(
                    thread_id=thread.id,
                    run_id=run.id,
                    tool_outputs=[
                        {
                        "tool_call_id": tool_call.id,
                        "output": weather_data + "\n\nPlease summarize the weather in one or two sentences."
                        }
                    ]
                )

        time.sleep(1)

    
    messages = client.beta.threads.messages.list(
        thread_id=thread.id
    )

    print_messages = []
    for thread_message in messages.data:
        for content_item in thread_message.content:
            print_messages.append(content_item.text.value + "\n")

    return print_messages[0]




if __name__ == "__main__":
    load_dotenv()
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # Create an assistant
    assistant_id = os.getenv("ASSISTANT_ID")
    if not assistant_id:
        assistant = create_assistant()
        assistant_id = assistant.id

    # Create an argument parser
    parser = argparse.ArgumentParser(description="Weather Assistant CLI")
    parser.add_argument("message", type=str, help="Your message to the Weather Assistant")
    args = parser.parse_args()

    # Use the provided message
    user_message = args.message

    # Ask the assistant
    ask_assistant(user_message)
    
