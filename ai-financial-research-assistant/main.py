from pydantic import BaseModel
from fastapi import FastAPI
from dotenv import load_dotenv
from google import genai
import os 

class QuestionRequest(BaseModel):
    question: str

load_dotenv()

app = FastAPI()

api_key = os.getenv("API_KEY")

client = genai.Client(api_key=api_key)

@app.get("/")
def root():
    return {
            "message" : "AI Financial Research Assistant API is running"
    }

@app.post("/analyze")
def analyze(request: QuestionRequest):

    prompt = f"""
    You are an expert financial research analyst.
    
    Answer the following financial question clearly and professionally.
    
    Question:
    {request.question}
    
    Guidelines:
    - Use simple language.
    - Mention risks where appropriate.
    - If discussing investments, mention that this is educational information and not financial advice.
    """
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return {
        "answer": response.text
    }


