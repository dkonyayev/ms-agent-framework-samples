# Return initalized FoundryChatClient for use in the agent framework.
import os

from azure.identity import AzureCliCredential
from agent_framework.foundry import FoundryChatClient
from dotenv import load_dotenv

load_dotenv()


def create_foundry_client() -> FoundryChatClient:
    project_endpoint = os.environ["FOUNDRY_PROJECT_ENDPOINT"]

    return FoundryChatClient(
        project_endpoint=project_endpoint,
        model=os.getenv("FOUNDRY_MODEL", "gpt-4o"),
        credential=AzureCliCredential(),
    )