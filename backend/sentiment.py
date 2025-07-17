# from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# def analyze_sentiment(text):
#     analyzer = SentimentIntensityAnalyzer()
#     scores = analyzer.polarity_scores(text)
#     compound = scores['compound']
#     if compound >= 0.05:
#         return 'positive', scores
#     elif compound <= -0.05:
#         return 'negative', scores
#     else:
#         return 'neutral', scores

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    scores = analyzer.polarity_scores(text)
    compound = scores['compound']
    if compound >= 0.05:
        sentiment = 'positive'
    elif compound <= -0.05:
        sentiment = 'negative'
    else:
        sentiment = 'neutral'
    return sentiment, scores
