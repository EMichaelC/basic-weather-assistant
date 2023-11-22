from openai import OpenAI
import os
import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
import json
import time
import argparse
from dotenv import load_dotenv

def get_weather_by_location(latitude, longitude, weather_variable="temperature_2m"):
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    # Prepare the API call
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": weather_variable
    }

    # Call the API
    responses = openmeteo.weather_api(url, params=params)

    # Process the first location response
    response = responses[0]

    # Process hourly data
    hourly = response.Hourly()
    hourly_data_values = hourly.Variables(0).ValuesAsNumpy()

    hourly_data = {
        "date": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s"),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s"),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left"
        )
    }
    hourly_data[weather_variable] = hourly_data_values

    return pd.DataFrame(data=hourly_data)

def get_daily_weather_by_location(latitude, longitude, weather_variable=["weather_code", "temperature_2m_max", "temperature_2m_min"]):
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": weather_variable
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]

    # Process daily data. The order of variables needs to be the same as requested.
    daily = response.Daily()
    daily_weather_code = daily.Variables(0).ValuesAsNumpy()
    daily_temperature_2m_max = daily.Variables(1).ValuesAsNumpy()
    daily_temperature_2m_min = daily.Variables(2).ValuesAsNumpy()

    daily_data = {"date": pd.date_range(
        start = pd.to_datetime(daily.Time(), unit = "s"),
        end = pd.to_datetime(daily.TimeEnd(), unit = "s"),
        freq = pd.Timedelta(seconds = daily.Interval()),
        inclusive = "left"
    )}
    daily_data["weather_code"] = daily_weather_code
    daily_data["temperature_2m_max"] = daily_temperature_2m_max
    daily_data["temperature_2m_min"] = daily_temperature_2m_min

    return pd.DataFrame(data = daily_data)


if __name__ == "__main__":
    load_dotenv()
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    assistant = client.beta.assistants.create(
        name="Weather Assistant",
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
        tools=[
            # {
            #     "type": "function",
            #     "function": {
            #         "name": "get_weather_by_location",
            #         "description": "Get the weather in location based on latitude and longitude",
            #         "parameters": {
            #             "type": "object",
            #             "properties": {
            #                 "latitude": {"type": "string", "description": "The latitude of the location (e.g., 37.7749)"},
            #                 "longitude": {"type": "string", "description": "The longitude of the location (e.g., -122.4194)"},
            #             },
            #         },
            #         "required": ["latitude", "longitude"]
                    
            #     }
            # },
            {
                "type": "function",
                "function": {
                    "name": "get_daily_weather_by_location",
                    "description": "Get the daily weather in location based on latitude and longitude",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "latitude": {"type": "string", "description": "The latitude of the location (e.g., 37.7749)"},
                            "longitude": {"type": "string", "description": "The longitude of the location (e.g., -122.4194)"},
                            # "weather_variable": {
                            #     "type": "array",
                            #     "items": {
                            #         "type": "string",
                            #         "enum": ["weather_code", "temperature_2m_max", "temperature_2m_min"],
                            #     },
                            #     "description": "The weather variable to retrieve (e.g., temperature_2m_max)",
                            # },
                        },
                    },
                    "required": ["latitude", "longitude"]
                }
            }
        ],
        model="gpt-4-1106-preview"
    )

     # Create an argument parser
    parser = argparse.ArgumentParser(description="Weather Assistant CLI")
    parser.add_argument("message", type=str, help="Your message to the Weather Assistant")
    args = parser.parse_args()

    # Use the provided message
    user_message = args.message

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
        assistant_id=assistant.id
    )

    # Use a while loop to check if the run is completed
    while True:
        retrieved_run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )

        if retrieved_run and retrieved_run.required_action and retrieved_run.required_action.submit_tool_outputs:
            tool_call = retrieved_run.required_action.submit_tool_outputs.tool_calls[0]
            tool_call_id = tool_call.id
            tool_call_function = tool_call.function
            tool_call_arguments = tool_call_function.arguments
            tool_call_arguments_json = json.loads(tool_call_arguments)
            tool_call_function_name = tool_call_function.name

            # Call the API
            if tool_call_function_name == "get_daily_weather_by_location":
                weather_data = get_daily_weather_by_location(
                    latitude=tool_call_arguments_json["latitude"],
                    longitude=tool_call_arguments_json["longitude"],
                    # weather_variable=tool_call_arguments_json["weather_variable"]
                )
            elif tool_call_function_name == "get_weather_by_location":
                weather_data = get_weather_by_location(
                    latitude=tool_call_arguments_json["latitude"],
                    longitude=tool_call_arguments_json["longitude"],
                    weather_variable="temperature_2m"
                )
            else:
                raise Exception("Unknown function name")

            # convert the dataframe to a JSON string
            weather_data_json = weather_data.to_json(orient="records")
            # convert json to one string:
            weather_data_json = "".join(weather_data_json.splitlines())
            break

        time.sleep(1)

    # Create a new message to the assistant with the weather data and ask for a concise summary
    run = client.beta.threads.runs.submit_tool_outputs(
            thread_id=thread.id,
            run_id=run.id,
            tool_outputs=[
                {
                "tool_call_id": tool_call.id,
                "output": weather_data_json + "\n\nPlease summarize the weather in one or two sentences."
                }
            ]
        )
    
    while True:
        retrieved_run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )

        if retrieved_run.status == "completed":
            break

        time.sleep(1)

    
    messages = client.beta.threads.messages.list(
        thread_id=thread.id
    )

    print_messages = []
    for thread_message in messages.data:
        for content_item in thread_message.content:
            print_messages.append(content_item.text.value + "\n")

    for message in reversed(print_messages):
        print(message)





