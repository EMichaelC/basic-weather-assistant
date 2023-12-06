from assistant_funcs import get_weather_by_location, get_daily_weather_by_location, get_text_from_first_google_search_result


assistant_tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_text_from_first_google_search_result",
                    "description": "Get the text from the first Google search result",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string", "description": "The query to search for (e.g., What is the weather in San Francisco?)"},
                        },
                    },
                    "required": ["query"]
                }
            },
        ]


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
            # {
            #     "type": "function",
            #     "function": {
            #         "name": "get_daily_weather_by_location",
            #         "description": "Get the daily weather in location based on latitude and longitude",
            #         "parameters": {
            #             "type": "object",
            #             "properties": {
            #                 "latitude": {"type": "string", "description": "The latitude of the location (e.g., 37.7749)"},
            #                 "longitude": {"type": "string", "description": "The longitude of the location (e.g., -122.4194)"},
            #                 # "weather_variable": {
            #                 #     "type": "array",
            #                 #     "items": {
            #                 #         "type": "string",
            #                 #         "enum": ["weather_code", "temperature_2m_max", "temperature_2m_min"],
            #                 #     },
            #                 #     "description": "The weather variable to retrieve (e.g., temperature_2m_max)",
            #                 # },
            #             },
            #         },
            #         "required": ["latitude", "longitude"]
            #     }
            # },




def handle_get_daily_weather_by_location(arguments):
    return get_daily_weather_by_location(
        latitude=arguments["latitude"],
        longitude=arguments["longitude"]
    )

def handle_get_weather_by_location(arguments):
    return get_weather_by_location(
        latitude=arguments["latitude"],
        longitude=arguments["longitude"],
        weather_variable="temperature_2m"
    )

def handle_get_text_from_first_google_search_result(arguments):
    return get_text_from_first_google_search_result(
        query=arguments["query"]
    )

tool_handlers = {
    "get_daily_weather_by_location": handle_get_daily_weather_by_location,
    "get_weather_by_location": handle_get_weather_by_location,
    "get_text_from_first_google_search_result": handle_get_text_from_first_google_search_result,
}