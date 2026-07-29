from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

from src.config import PROJECT_ENDPOINT

credential = DefaultAzureCredential()

project_client = AIProjectClient(
    endpoint=PROJECT_ENDPOINT,
    credential=credential,
)