from pydantic import BaseModel,ValidationError
from fastapi import FastAPI
from dotenv import load_dotenv
from google import genai
import os
import json
from market_service import get_stock_info
from typing import List


class AnalysisResponse(BaseModel):
    summary: str
    bullish_factors: List[str]
    bearish_factors: List[str]
    risks: List[str]
    investment_horizon: str
    disclaimer: str

class QuestionRequest(BaseModel):
    symbol: str
    question: str


load_dotenv()

app = FastAPI()

api_key = os.getenv("API_KEY")

client = genai.Client(api_key=api_key)


@app.get("/")
def root():
    return {
        "message": "AI Financial Research Assistant API is running"
    }


@app.post("/analyze")
def analyze(request: QuestionRequest):

    market_data = get_stock_info(request.symbol)

    print(market_data)

    prompt = f"""
You are an expert financial research analyst.

Stock Information:
{market_data}

Question:
{request.question}

Return your response ONLY in valid JSON format.

Required JSON structure:

{{
    "summary": "Short summary of the stock situation.",
    "bullish_factors": [
        "factor1",
        "factor2"
    ],
    "bearish_factors": [
        "factor1",
        "factor2"
    ],
    "risks": [
        "risk1",
        "risk2"
    ],
    "investment_horizon": "Short Term / Medium Term / Long Term",
    "disclaimer": "Educational information only and not financial advice."
}}

Do not include markdown.
Do not use triple backticks.
Return only JSON.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    print(response.text)

    try:
        analysis = AnalysisResponse(
            **json.loads(response.text)
        )
     
        return {
            "symbol": request.symbol,
            "market_data": market_data,
            "analysis": analysis
        }

    except json.JSONDecodeError:
        return {
            "error": "Model returned invalid JSON",
            "raw_response": response.text
        }

    except ValidationError as e:
        return {
            "error": "Model returned invalid schema",
            "details": e.errors(),
            "raw_response": response.text
        }
    
