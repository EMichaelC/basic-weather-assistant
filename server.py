from fastapi import FastAPI, Form
from starlette.responses import HTMLResponse
from starlette.requests import Request
import os
import json
import time
from dotenv import load_dotenv
from openai import OpenAI
from weather_assistant import ask_assistant

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Initialize OpenAI client
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Assistant ID
assistant_id = os.getenv("ASSISTANT_ID")

# HTML form for the user interface
html_content = """
                <html>
                    <head>
                        <title>Weather Assistant</title>
                    </head>
                    <body>
                        <h1>Weather Assistant</h1>
                        <form method="post">
                            <input type="text" name="message" placeholder="Ask about the weather...">
                            <input type="submit" value="Send">
                        </form>
                        <p><strong>Response:</strong> {response}</p>
                    </body>
                </html>
                """

@app.get("/", response_class=HTMLResponse)
async def read_form():
    return html_content.format(response="")

@app.post("/", response_class=HTMLResponse)
async def handle_form(request: Request):
    form_data = await request.form()
    user_message = form_data.get("message")
    response = await ask_assistant(openai_client, assistant_id, user_message)
    return html_content.format(response=response)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
