from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List
import uvicorn
from utils import process_company_news
import os
import threading

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

def run_api():
    config = uvicorn.Config(app=app, host="127.0.0.1", port=8080, log_level="info")
    server = uvicorn.Server(config)
    server.run()

# Start API in a thread
threading.Thread(target=run_api, daemon=True).start()

import streamlit as st
from utils import NewsExtractor, SentimentAnalyzer, TextToSpeech, ComparativeAnalyzer

# This must be the first Streamlit command
st.set_page_config(
    page_title="News Analysis Dashboard",
    page_icon="📰",
    layout="wide"
)

# Import other modules AFTER setting page config

import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json

# Constants
API_URL = "http://localhost:8000"

def fetch_analysis(company_name: str) -> Dict[str, Any]:
    """Fetch analysis from the API."""
    try:
        import time
        timestamp = int(time.time())  # Current timestamp to prevent caching
        response = requests.post(
            f"{API_URL}/api/news",
            json={"company_name": company_name, "timestamp": timestamp}
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error fetching analysis: {str(e)}")
        return None

def display_article_details(article: Dict[str, Any]):
    """Display details for a single article."""
    with st.expander(article['title']):
        st.write("**Summary:**", article['summary'])
        st.write("**Sentiment:**", article['sentiment'])
        st.write("**Sentiment Score:**", f"{article['sentiment_score']:.2f}")
        st.write("**Keywords:**", ", ".join(article['keywords']))
        st.write("**Source:**", article['url'])
        st.write("**Published:**", article['publish_date'])

def display_comparative_analysis(analysis: Dict[str, Any]):
    """Display comparative analysis visualizations."""
    st.header("Comparative Analysis")
    
    # Debug information
    st.write("Debug - Received analysis data:", analysis)
    
    # Check if sentiment_distribution exists and has data
    if analysis and 'sentiment_distribution' in analysis and analysis['sentiment_distribution']:
        # Sentiment Distribution
        st.subheader("Sentiment Distribution")
        sentiment_data = pd.DataFrame(
            list(analysis['sentiment_distribution'].items()),
            columns=['Sentiment', 'Count']
        )
        
        # Only create chart if there's data
        if not sentiment_data.empty and sentiment_data['Count'].sum() > 0:
            fig1 = px.pie(
                sentiment_data,
                values='Count',
                names='Sentiment',
                title='Sentiment Distribution'
            )
            st.plotly_chart(fig1)
        else:
            st.info("No sentiment distribution data available.")
    else:
        st.info("No sentiment distribution data available.")
    
    # Check if top_keywords exists and has data
    if analysis and 'top_keywords' in analysis and analysis['top_keywords']:
        # Top Keywords
        st.subheader("Top Keywords")
        keyword_data = pd.DataFrame(
            list(analysis['top_keywords'].items()),
            columns=['Keyword', 'Count']
        )
        
        # Only create chart if there's data
        if not keyword_data.empty and keyword_data['Count'].sum() > 0:
            fig2 = px.bar(
                keyword_data,
                x='Count',
                y='Keyword',
                title='Top Keywords',
                orientation='h'
            )
            st.plotly_chart(fig2)
        else:
            st.info("No keyword data available.")
    else:
        st.info("No keyword data available.")
    
    # Average Sentiment Score
    if analysis and 'average_sentiment' in analysis:
        st.metric(
            "Average Sentiment Score",
            f"{analysis.get('average_sentiment', 0):.2f}"
        )

# Process company news directly in Streamlit
@st.cache_data
def process_company_news(company_name):
    news_extractor = NewsExtractor()
    sentiment_analyzer = SentimentAnalyzer()
    tts_generator = TextToSpeech()
    comparative_analyzer = ComparativeAnalyzer()
    
    # Fetch news articles
    articles = news_extractor.fetch_news(company_name)
    
    # Analyze sentiment for each article
    for article in articles:
        sentiment_result = sentiment_analyzer.analyze_sentiment(article['text'])
        article['sentiment'] = sentiment_result['label']
        article['sentiment_score'] = sentiment_result['score']
    
    # Generate comparative analysis
    comparative_analysis = comparative_analyzer.analyze_articles(articles)
    
    # Get sentiment counts from comparative analysis
    sentiment_counts = comparative_analysis.get('sentiment_distribution', {})
    
    # Create the Hindi summary with proper error handling
    summary_text = f"{company_name} के बारे में {len(articles)} समाचार लेखों का विश्लेषण। "
    summary_text += f"कुल लेखों में से {sentiment_counts.get('POSITIVE', 0)} सकारात्मक, "
    summary_text += f"{sentiment_counts.get('NEGATIVE', 0)} नकारात्मक, और "
    summary_text += f"{sentiment_counts.get('NEUTRAL', 0)} तटस्थ हैं।"
    
    # Generate TTS audio
    audio_path = tts_generator.generate_hindi_tts(summary_text)
    
    return {
        'articles': articles,
        'comparative_analysis': comparative_analysis,
        'audio_path': audio_path
    }

def main():
    st.title("📰 News Analysis Dashboard")
    st.write("Analyze news articles and generate insights for any company")
    
    # Company input
    company_name = st.text_input("Enter Company Name", "Apple")
    
    if st.button("Analyze"):
        with st.spinner("Analyzing news articles..."):
            # Process directly instead of using API
            result = process_company_news(company_name)
            
            if result:
                # Display articles
                st.header("Articles")
                for article in result['articles']:
                    display_article_details(article)
                
                # Display comparative analysis
                display_comparative_analysis(result['comparative_analysis'])
                
                # Display audio player
                if result['audio_path'] and os.path.exists(result['audio_path']):
                    st.header("Hindi Summary")
                    st.audio(result['audio_path'])

if __name__ == "__main__":
    main() 