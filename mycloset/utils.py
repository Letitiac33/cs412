import os
import requests
from dotenv import load_dotenv

load_dotenv()


def remove_background(image_file) -> bytes:
    api_key = os.getenv("REMOVE_BG_API_KEY")
    response = requests.post(
        "https://api.remove.bg/v1.0/removebg",
        files={"image_file": image_file},
        data={"size": "auto"},
        headers={"X-Api-Key": api_key},
    )
    return response.content
