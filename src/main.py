from dotenv import load_dotenv
import os

# Load variables from the .env file in the project root
load_dotenv()

project_endpoint = os.getenv("PROJECT_ENDPOINT")
model_name = os.getenv("MODEL_DEPLOYMENT_NAME")

print(project_endpoint)
print(model_name)

