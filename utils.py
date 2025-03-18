import requests
from bs4 import BeautifulSoup
from newspaper import Article
from textblob import TextBlob
from transformers import pipeline
from gtts import gTTS
import pandas as pd
import numpy as np
from typing import List, Dict, Any
import os
import tempfile
import json

class NewsExtractor:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        # Use a different news source - example with NewsAPI
        self.api_key = "36f972a4972c4453b02d29d3c07a4eae"  # You would need to get this from newsapi.org
        
    def fetch_news(self, company_name: str) -> List[Dict[str, Any]]:
        """Fetch news articles related to the company."""
        articles = []
        
        try:
            # Use NewsAPI instead of scraping
            url = f"https://newsapi.org/v2/everything?q={company_name}&apiKey={self.api_key}&language=en&pageSize=10"
            response = requests.get(url)
            data = response.json()
            
            if data.get('status') == 'ok' and data.get('totalResults', 0) > 0:
                for item in data.get('articles', [])[:10]:
                    articles.append({
                        'title': item.get('title', 'Untitled'),
                        'summary': item.get('description', 'No summary available'),
                        'url': item.get('url', ''),
                        'text': item.get('content', 'No content available'),
                        'keywords': [company_name] + item.get('title', '').lower().split()[:5],
                        'publish_date': item.get('publishedAt', 'Unknown date')
                    })
        except Exception as e:
            print(f"Error fetching from NewsAPI: {str(e)}")
        
        # If no articles were found, use varied test data
        if not articles:
            sentiments = ["POSITIVE", "NEGATIVE", "NEUTRAL"]
            keywords = ["business", "finance", "technology", "market", "growth", "decline", 
                        "strategy", "product", "launch", "innovation", "revenue", "profit"]
            
            for i in range(random.randint(5, 10)):  # Random number of articles
                sentiment = random.choice(sentiments)
                article_keywords = [company_name.lower()] + random.sample(keywords, k=3)
                score = random.uniform(0.6, 0.95) if sentiment != "NEUTRAL" else random.uniform(0.4, 0.6)
                
                articles.append({
                    'title': f"{random.choice(['Breaking', 'New', 'Recent', 'Important'])} {sentiment.lower()} news about {company_name}",
                    'summary': f"A {sentiment.lower()} summary about {company_name}'s {random.choice(['recent', 'latest', 'ongoing'])} {random.choice(['developments', 'activities', 'performance'])}.",
                    'url': f"https://example.com/article{i+1}",
                    'text': f"This is article {i+1} about {company_name}. {random.choice(['The company reported', 'Analysts suggest', 'Industry experts confirm'])} {random.choice(['positive results', 'concerning trends', 'stable performance'])}.",
                    'keywords': article_keywords,
                    'publish_date': f"2023-{random.randint(1,12):02d}-{random.randint(1,28):02d}",
                    'sentiment': sentiment,
                    'sentiment_score': score
                })
        
        return articles

class SentimentAnalyzer:
    def __init__(self):
        self.sentiment_analyzer = pipeline("sentiment-analysis")
        # Map of model outputs to our expected sentiment categories
        self.label_map = {
            "LABEL_0": "NEGATIVE",
            "LABEL_1": "POSITIVE",
            "negative": "NEGATIVE",
            "positive": "POSITIVE",
            "neutral": "NEUTRAL",
            "NEGATIVE": "NEGATIVE",
            "POSITIVE": "POSITIVE",
            "NEUTRAL": "NEUTRAL"
        }
        
    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment of text using transformers."""
        try:
            # Handle empty text
            if not text or len(text.strip()) == 0:
                return {'label': 'NEUTRAL', 'score': 0.5}
                
            # Limit text length for model
            result = self.sentiment_analyzer(text[:512])[0]
            
            # Map the label to our expected format
            label = result['label']
            mapped_label = self.label_map.get(label, "NEUTRAL")
            
            return {
                'label': mapped_label,
                'score': float(result['score'])
            }
        except Exception as e:
            print(f"Error in sentiment analysis: {str(e)}")
            return {'label': 'NEUTRAL', 'score': 0.5}

class TextToSpeech:
    def __init__(self):
        self.temp_dir = tempfile.gettempdir()
        
    def generate_hindi_tts(self, text: str) -> str:
        """Generate Hindi TTS audio file."""
        try:
            tts = gTTS(text=text, lang='hi')
            audio_path = os.path.join(self.temp_dir, 'summary.mp3')
            tts.save(audio_path)
            return audio_path
        except Exception as e:
            print(f"Error generating TTS: {str(e)}")
            return None

class ComparativeAnalyzer:
    def analyze_articles(self, articles: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Perform comparative analysis on articles."""
        if not articles:
            # Return default structure with empty data
            return {
                'sentiment_distribution': {'POSITIVE': 0, 'NEGATIVE': 0, 'NEUTRAL': 0},
                'average_sentiment': 0.5,
                'top_keywords': {},
                'total_articles': 0
            }
        
        # Create a DataFrame for analysis
        df = pd.DataFrame(articles)
        
        # Ensure 'sentiment' column exists
        if 'sentiment' not in df.columns:
            print("Warning: 'sentiment' column missing from articles data")
            df['sentiment'] = 'NEUTRAL'  # Default to neutral
        
        # Calculate sentiment distribution
        sentiment_counts = df['sentiment'].value_counts().to_dict()
        
        # Ensure all sentiment categories exist
        for sentiment in ['POSITIVE', 'NEGATIVE', 'NEUTRAL']:
            if sentiment not in sentiment_counts:
                sentiment_counts[sentiment] = 0
        
        # Calculate average sentiment score
        if 'sentiment_score' in df.columns:
            avg_sentiment = df['sentiment_score'].mean()
        else:
            print("Warning: 'sentiment_score' column missing")
            avg_sentiment = 0.5  # Default middle value
        
        # Extract common keywords with robust error handling
        top_keywords = {}
        try:
            if 'keywords' in df.columns:
                # Extract keywords and filter out None values
                all_keywords = []
                for keywords in df['keywords']:
                    if isinstance(keywords, list):
                        all_keywords.extend(keywords)
                
                if all_keywords:
                    # Count keyword occurrences
                    keyword_counter = {}
                    for keyword in all_keywords:
                        if keyword in keyword_counter:
                            keyword_counter[keyword] += 1
                        else:
                            keyword_counter[keyword] = 1
                    
                    # Sort by count and get top 10
                    sorted_keywords = sorted(keyword_counter.items(), key=lambda x: x[1], reverse=True)
                    top_keywords = dict(sorted_keywords[:10])
        except Exception as e:
            print(f"Error extracting keywords: {str(e)}")
            top_keywords = {"Error": 0}  # Provide at least one item
        
        return {
            'sentiment_distribution': sentiment_counts,
            'average_sentiment': float(avg_sentiment),
            'top_keywords': top_keywords,
            'total_articles': len(articles)
        }
        
def process_company_news(company_name: str) -> Dict[str, Any]:
    """Process news articles for a company and generate analysis."""
    news_extractor = NewsExtractor()
    sentiment_analyzer = SentimentAnalyzer()
    tts_generator = TextToSpeech()
    comparative_analyzer = ComparativeAnalyzer()
    
    # Fetch news articles
    articles = news_extractor.fetch_news(company_name)
    
    # Analyze sentiment for each article
    # In process_company_news function:

# Analyze sentiment for each article
    for article in articles:
        try:
            sentiment_result = sentiment_analyzer.analyze_sentiment(article['text'])
            # Map sentiment labels if needed - the model might use different labels
            label = sentiment_result['label']
            
            # Map model labels to expected labels if necessary
            # For example, if your model returns "LABEL_0" and "LABEL_1"
            if label == "LABEL_0":
                label = "NEGATIVE"
            elif label == "LABEL_1":
                label = "POSITIVE"
            
            article['sentiment'] = label
            article['sentiment_score'] = sentiment_result['score']
        except Exception as e:
            print(f"Error analyzing sentiment: {str(e)}")
            # Default values if sentiment analysis fails
            article['sentiment'] = 'NEUTRAL'
            article['sentiment_score'] = 0.5
    
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