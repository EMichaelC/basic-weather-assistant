# Weather Assistant Application

## Overview

This Weather Assistant Application is a web-based interface that interacts with an OpenAI model to provide weather information based on user queries. It's built using FastAPI and utilizes the OpenAI API for processing natural language queries related to weather.

## Prerequisites

Before you start using this application, you need to ensure you have the following:

- Python 3.7 or higher
- `fastapi`: A modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.
- `uvicorn`: A lightning-fast ASGI server implementation, using uvloop and httptools.
- `openai-python`: The official Python client for the OpenAI API.
- `python-multipart` (for form handling in FastAPI)
- `pandas`: Used for data manipulation and analysis.
- `requests_cache`: Enables caching for API requests to improve performance and reduce the load on the API server.
- `retry_requests`: Adds retry functionality to requests, useful for handling transient network issues.
- `openmeteo_requests`: A custom client for accessing the Open-Meteo API.
- `python-dotenv`: Reads key-value pairs from a .env file and can set them as environment variables.

## Installation and configuration

1. Clone or download the repository to your local machine.
2. Pip install the required Python libraries:
3. Create an OpenAI account and get your API key from [here](https://beta.openai.com/).
4. See assistant_funcs and run the create_assistant function to create your assistant.
5. Visit openai and find your assistant ID or get it from the response of the create_assistant function.
6. Set the environment variables `OPENAI_API_KEY` and `ASSISTANT_ID` to your API key and assistant ID respectively.

## Usage

To run the application, use the following command:

1. `uvicorn server:app --reload`
2. Got to http://localhost:8000
3. Enter your query and click on the submit button
4. The response will be displayed on the screen

## License

This project is licensed under the MIT License.

### For more on how assistants work, see:

https://platform.openai.com/docs/assistants/how-it-works
