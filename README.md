---
title: News Summarization and TTS
emoji: 📰
colorFrom: blue
colorTo: pink
sdk: streamlit
sdk_version: 1.43.2
app_file: app.py
pinned: false
license: mit
---

# News Summarization and Text-to-Speech Application

A web-based application that extracts key details from multiple news articles related to a given company, performs sentiment analysis, conducts comparative analysis, and generates text-to-speech output in Hindi.

## Features

- News article extraction and summarization
- Sentiment analysis for each article
- Comparative analysis across multiple articles
- Hindi Text-to-Speech conversion
- Interactive web interface
- RESTful API endpoints

## Project Overview

This application allows users to:
1. Enter a company name
2. View news articles about that company
3. See sentiment analysis of each article (positive, negative, or neutral)
4. View comparative analysis with visualizations
5. Listen to a Hindi audio summary of the analysis

## Setup Instructions

1. Clone the repository:
```bash
git clone <repository-url>
cd news-summarization-tts
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Download required NLTK data:
```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
```

5. Start the backend API server:
```bash
python api.py
```

6. In a new terminal window, start the Streamlit frontend:
```bash
streamlit run app.py
```

## Project Structure

- `app.py`: Main Streamlit application interface
- `api.py`: FastAPI backend endpoints
- `utils.py`: Utility functions for news extraction, sentiment analysis, and TTS
- `requirements.txt`: Project dependencies
- `README.md`: Project documentation

## API Endpoints

- `POST /api/news`: Fetch news articles for a company and analyze them
- `GET /api/health`: Health check endpoint

## Implementation Details

### News Extraction

The application uses one of the following approaches to extract news:
- Web scraping using BeautifulSoup
- NewsAPI integration (if configured)
- Fallback test data for demonstration purposes

### Sentiment Analysis

Sentiment analysis is performed using the Hugging Face Transformers library, which categorizes articles as:
- POSITIVE
- NEGATIVE
- NEUTRAL

### Comparative Analysis

The application generates insights across all articles:
- Sentiment distribution
- Top keywords
- Average sentiment score

### Hindi Text-to-Speech

The summary is converted to Hindi speech using Google's gTTS (Google Text-to-Speech) library.

## Known Issues and Workarounds

- **Web Scraping Limitations**: Google News and other news sites may block scraping. The application includes fallback mechanisms to ensure functionality.
- **Sentiment Model Variations**: Different sentiment models might use different label formats. The application maps these to standard positive/negative/neutral categories.
- **Performance Considerations**: Fetching and processing multiple articles can take time. The application is limited to processing 10 articles maximum.

## Troubleshooting

If you encounter issues:

1. **API Connection Error**: Ensure the FastAPI backend is running before starting the Streamlit app.

2. **No Articles Found**: Try different company names or check your internet connection.

3. **Missing Visualizations**: This could indicate no articles were processed successfully. Check the console logs for details.

4. **Text-to-Speech Not Working**: Ensure you have an active internet connection as gTTS requires internet access.

## Dependencies

- streamlit: Web interface
- beautifulsoup4, requests, newspaper3k: Web scraping
- transformers, textblob, nltk: Text analysis
- pandas, numpy: Data processing
- fastapi, uvicorn: API backend
- gTTS: Text-to-speech
- plotly: Visualizations

## Future Improvements

- Add more news sources
- Implement better keyword extraction
- Add language selection for both text and speech
- Implement caching to improve performance
- Add user authentication and history

## License

This project is licensed under the MIT License - see the LICENSE file for details.
