import logging
import os

import uvicorn
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from starlette.middleware.cors import CORSMiddleware

from dash_extensions.streaming import sse_message
from openai import AzureOpenAI
from dotenv import load_dotenv

from models import Query


# Load environment variables from .env file.
load_dotenv()
# Setup logging.
logger = logging.getLogger(__name__)
# Setup FastAPI app.
app = FastAPI()
# Add CORS middleware to allow cross-origin requests (necessary for streaming).
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
# Setup AzureOpenAI client. NB: You must provide your own ENDPOINT/API_KEY/MODEL (and, optionally, API_VERSION).
client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),  # type: ignore
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),  # type: ignore
    api_version=os.getenv("OPENAI_API_VERSION", "2024-02-01"),
)
model_deployment_name = os.getenv("AZURE_OPENAI_MODEL", "gpt-4o")


@app.post("/stream")
async def stream(query: Query) -> StreamingResponse:
    return StreamingResponse(_stream(query), media_type="text/event-stream")


def _stream(query: Query):
    # Connect to Azure OpenAI.
    response_stream = client.chat.completions.create(
        messages=query.messages,  # type: ignore
        model=model_deployment_name,
        stream=True,
    )
    # Stream the content.
    for event in response_stream:
        if len(event.choices) == 0:
            continue
        delta_content = event.choices[0].delta.content
        if delta_content is not None:
            yield sse_message(delta_content)
    # Signal end of the stream.
    yield sse_message()


logger.info("Starting server.")

if __name__ == "__main__":
    uvicorn.run(app, port=8000)
