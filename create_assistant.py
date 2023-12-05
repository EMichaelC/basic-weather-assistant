from openai import OpenAI
import os
from dotenv import load_dotenv
from handlers import assistant_tools


def create_assistant():
    return client.beta.assistants.create(
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

if __name__ == '__main__':
    load_dotenv()
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    assistant = create_assistant()
    print(assistant.id)
