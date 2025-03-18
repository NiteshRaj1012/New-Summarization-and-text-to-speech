import streamlit as st
from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import threading
import nest_asyncio
import utils  # Your utility functions

# Apply nest_asyncio to allow running asyncio code in Streamlit
nest_asyncio.apply()

# Create FastAPI app
api = FastAPI()
api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define API endpoints
@api.post("/api/news")
async def analyze_company_news(company_name: str):
    result = utils.process_company_news(company_name)
    return result

# Run FastAPI in a separate thread
def run_api():
    config = uvicorn.Config(app=api, host="127.0.0.1", port=8000, log_level="info")
    server = uvicorn.Server(config)
    server.run()

# Start API in a thread
threading.Thread(target=run_api, daemon=True).start()

import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Any, List
import json
import os

# Configure the page
st.set_page_config(
    page_title="News Analysis Dashboard",
    page_icon="📰",
    layout="wide"
)

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

def main():
    st.title("📰 News Analysis Dashboard")
    st.write("Analyze news articles and generate insights for any company")
    
    # Company input
    company_name = st.text_input("Enter Company Name", "Apple")
    
    if st.button("Analyze"):
        with st.spinner("Analyzing news articles..."):
            result = fetch_analysis(company_name)
            
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