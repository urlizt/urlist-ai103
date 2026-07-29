from dotenv import load_dotenv
import os

# Load variables from .env
load_dotenv()

PROJECT_ENDPOINT = os.environ["PROJECT_ENDPOINT"]
MODEL_DEPLOYMENT_NAME = os.environ["MODEL_DEPLOYMENT_NAME"]