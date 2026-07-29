from src.foundry import project_client
from src.config import MODEL_DEPLOYMENT_NAME

print("Connected successfully!")
print(f"Endpoint: {project_client}")
print(f"Model: {MODEL_DEPLOYMENT_NAME}")
