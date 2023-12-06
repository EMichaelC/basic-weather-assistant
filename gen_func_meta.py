import inspect
from typing import get_type_hints

def generate_function_metadata(func):
    # Get the signature of the function
    signature = inspect.signature(func)
    parameters = signature.parameters
    type_hints = get_type_hints(func)

    # Extract parameter information
    params_dict = {}
    for name, param in parameters.items():
        # Assuming descriptions are provided in annotations
        param_type = type_hints.get(name, 'string')
        description = param.annotation if param.annotation != param.empty else "No description"
        
        params_dict[name] = {
            "type": param_type.__name__ if hasattr(param_type, '__name__') else str(param_type),
            "description": description
        }

    # Creating the dictionary
    function_dict = {
        "type": "function",
        "function": {
            "name": func.__name__,
            "description": func.__doc__,
            "parameters": {
                "type": "object",
                "properties": params_dict
            },
            "required": list(parameters.keys())
        }
    }

    return function_dict


if __name__ == "__main__":
    from assistant_funcs import get_daily_weather_by_location, get_weather_by_location, get_text_from_first_google_search_result
    from handlers import handle_get_daily_weather_by_location, handle_get_weather_by_location, handle_get_text_from_first_google_search_result
    from assistant import call_tool_function

    # Generate the metadata for the functions
    get_daily_weather_by_location_metadata = generate_function_metadata(get_daily_weather_by_location)
    get_weather_by_location_metadata = generate_function_metadata(get_weather_by_location)
    get_text_from_first_google_search_result_metadata = generate_function_metadata(get_text_from_first_google_search_result)

    # Generate the metadata for the handlers
    handle_get_daily_weather_by_location_metadata = generate_function_metadata(handle_get_daily_weather_by_location)
    handle_get_weather_by_location_metadata = generate_function_metadata(handle_get_weather_by_location)
    handle_get_text_from_first_google_search_result_metadata = generate_function_metadata(handle_get_text_from_first_google_search_result)

    print(get_daily_weather_by_location_metadata)
    print(get_weather_by_location_metadata)
    print(get_text_from_first_google_search_result_metadata)