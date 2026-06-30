from pydantic import BaseModel
from fastapi import FastAPI
from dotenv import load_dotenv
from google import genai
import os 
from market_service import get_stock_info

class QuestionRequest(BaseModel):
    symbol : str
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

    market_data = get_stock_info(request.symbol)

    print(market_data)

    prompt = f"""
    You are an expert financial research analyst.
    
    Stock Information:
    
    Company Name: {market_data["name"]}
    Current Price: {market_data["current_price"]}
    Sector: {market_data["sector"]}
    1 Month Return: {market_data["one_month_return_percent"]}%
    
    Recent News:
    {market_data["recent_news"]}
    
    Question:
    {request.question}
    
    Guidelines:
    - Use simple language.
    - Mention risks where appropriate.
    - Mention bullish and bearish factors.
    - Use recent news if relevant.
    - This is educational information and not financial advice.
    """ 


    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return {
        "answer": response.text
    }


