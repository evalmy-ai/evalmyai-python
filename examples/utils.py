import os

from evalmyai._evalmyai import Evaluator

from dotenv import load_dotenv

load_dotenv(dotenv_path="../.env")

auth = {
    "api_key": os.getenv("AZURE_OPENAI_API_KEY"),
    "azure_endpoint": os.getenv("AZURE_OPENAI_ENDPOINT"),
    "api_version": os.getenv("AZURE_OPENAI_API_VERSION"),
    "azure_deployment": os.getenv("AZURE_DEPLOYMENT_NAME"),
}

auth_open_ai = {"api_key": os.getenv("OPENAI_API_KEY"), "model": "gpt-4o"}

token = os.getenv("EVALMYAI_TOKEN")


def init_evaluator():
    return Evaluator(auth, token)
