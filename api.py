from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List
import uvicorn
from utils import process_company_news

app = FastAPI(title="News Analysis API")

class CompanyRequest(BaseModel):
    company_name: str

class Article(BaseModel):
    title: str
    summary: str
    url: str
    text: str
    keywords: List[str]
    publish_date: str
    sentiment: str
    sentiment_score: float

class AnalysisResponse(BaseModel):
    articles: List[Article]
    comparative_analysis: Dict[str, Any]
    audio_path: str

@app.post("/api/news", response_model=AnalysisResponse)
async def analyze_company_news(request: CompanyRequest):
    """
    Analyze news articles for a given company.
    """
    try:
        result = process_company_news(request.company_name)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 