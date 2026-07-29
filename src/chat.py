from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY") or os.getenv("AZURE_OPENAI_API_KEY")
base_url = os.getenv("OPENAI_API_BASE") or os.getenv("AZURE_OPENAI_API_BASE") or os.getenv("AZURE_OPENAI_BASE_URL")
model_name = os.getenv("MODEL_DEPLOYMENT_NAME", "gpt-5.2")

if api_key is None:
    raise RuntimeError(
        "Missing credentials. Set OPENAI_API_KEY or AZURE_OPENAI_API_KEY in your environment or .env file."
    )

client_kwargs = {"api_key": api_key}
if base_url:
    client_kwargs["base_url"] = base_url

openai_client = OpenAI(**client_kwargs)

# Generate a response using the OpenAI-compatible client
response = openai_client.responses.create(
    model=model_name,

     instructions="Keep it concise (in 5 bullets or less)",
     input="What is Microsoft Foundry?"

    #input="Explain machine learning in simple terms."

    # In addition to the user input, you can provide instructions (often referred to as a system prompt) to guide the model's behavior.
    # instructions="You are a helpful AI assistant that answers questions clearly and concisely for beginners.",
    # input="Explain neural networks."
)

# Display the response
# print(response.output_text)
print(f"Response: {response.output_text}")
print(f"Response ID: {response.id}")
print(f"Tokens used: {response.usage.total_tokens}")
print(f"Status: {response.status}")
print(f"Temperature: {response.temperature}")