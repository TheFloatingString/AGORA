import os
import openai
import dotenv

dotenv.load_dotenv()


openai.api_key = os.getenv("OPENAI_API_KEY")

response = openai.Completion.create(
        model="text-davinci-003",
        prompt="What is the capital city of Canada?",
        temperature=0.5,
        max_tokens=250,
        top_p=1.0,
        frequency_penalty=0.8,
        presence_penalty=0.0
    )

print(response)
