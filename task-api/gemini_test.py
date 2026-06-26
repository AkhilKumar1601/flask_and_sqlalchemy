from dotenv import load_dotenv
from google import genai
import os

load_dotenv()

api_key = os.getenv("API_KEY")


client = genai.Client(api_key=api_key)

response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Explain SQL joins in simple terms"
)

print(response.text)


