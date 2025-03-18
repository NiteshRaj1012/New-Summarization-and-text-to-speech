# News Summarization and Text-to-Speech Application

A web-based application that extracts key details from multiple news articles related to a given company, performs sentiment analysis, conducts comparative analysis, and generates text-to-speech output in Hindi.

## Features

- News article extraction and summarization
- Sentiment analysis for each article
- Comparative analysis across multiple articles
- Hindi Text-to-Speech conversion
- Interactive web interface
- RESTful API endpoints

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
nltk.download('averaged_perceptron_tagger')
```

5. Run the application:
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

- `POST /api/news`: Fetch news articles for a company
- `POST /api/sentiment`: Analyze sentiment of articles
- `POST /api/tts`: Generate Hindi TTS audio

## Usage

1. Launch the application using Streamlit
2. Enter a company name in the input field
3. Click "Analyze" to fetch and process news articles
4. View the sentiment analysis results and comparative analysis
5. Play the Hindi TTS audio summary

## Technologies Used

- Python 3.8+
- Streamlit for web interface
- BeautifulSoup4 for web scraping
- Transformers for sentiment analysis
- gTTS for Hindi text-to-speech
- FastAPI for backend API
- Newspaper3k for article extraction

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details. 