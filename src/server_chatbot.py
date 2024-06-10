import os
import openai
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

openai.api_key = os.getenv("OPENAI_API_KEY")


def get_pizza_info(pizza_type):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Provide ingredients and details for making {pizza_type} pizza.",
        max_tokens=150,
    )
    return response.choices[0].text.strip()
