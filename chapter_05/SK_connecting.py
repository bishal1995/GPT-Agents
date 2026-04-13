import asyncio

import semantic_kernel as sk
from openai import AsyncOpenAI
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion

selected_service = "Ollama"
local_model = "gemma4:latest"

kernel = sk.Kernel()

service_id = None

if selected_service == "Ollama":
    service_id = "ollama_chat"

    # Ollama exposes an OpenAI-compatible API at /v1
    # A non-empty API key is required by the OpenAI client, even for local Ollama.
    ollama_client = AsyncOpenAI(
        api_key="fake-key",
        base_url="http://localhost:11434/v1",
    )

    kernel.add_service(
        OpenAIChatCompletion(
            service_id=service_id,
            ai_model_id=local_model,
            async_client=ollama_client
        ),
    )


# This function is currently broken
async def run_prompt():
    result = await kernel.invoke_prompt(prompt="recommend a movie about time travel")
    print(result)


# Use asyncio.run to execute the async function
asyncio.run(run_prompt())
