from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

# nltk.download("vader_lexicon")
sid = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    score = sid.polarity_scores(text)['compound']
    if score >= 0.05:
        return 'Positive'
    elif score <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'