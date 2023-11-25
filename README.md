# Weather Assistant Application

## Overview

This Weather Assistant Application is a web-based interface that interacts with an OpenAI model to provide weather information based on user queries. It's built using FastAPI and utilizes the OpenAI API for processing natural language queries related to weather.

## Prerequisites

Before you start using this application, you need to ensure you have the following:

- Python 3.7 or higher
- FastAPI
- Uvicorn (for running the FastAPI app)
- OpenAI Python client
- `python-multipart` (for form handling in FastAPI)

## Installation

1. Clone or download the repository to your local machine.
2. Install the required Python libraries:
   ```bash
   pip install fastapi uvicorn openai python-multipart
   ```
3. Create an OpenAI account and get your API key from [here](https://beta.openai.com/).

## Configuration

To use the application, you need to set up a few environment variables:

- `OPENAI_API_KEY`: Your OpenAI API key. This is required to authenticate requests to the OpenAI API.
- `ASSISTANT_ID`: The ID of your OpenAI Assistant. This is specific to the assistant you have created in the OpenAI platform.

You can set these variables in a `.env` file in the root of the project or export them directly into your environment.

## Usage

To run the application, use the following command:

1. `uvicorn server:app --reload`
2. Got to http://localhost:8000
3. Enter your query and click on the submit button
4. The response will be displayed on the screen

## License

This project is licensed under the MIT License.
