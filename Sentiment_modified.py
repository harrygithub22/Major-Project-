import pandas as pd
from textblob import TextBlob
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Step 1: Load the Excel file
file_path = '/amazon_all_reviews_CsV_.xlsx'  # Replace with your actual file path

# Use openpyxl engine for .xlsx files
df = pd.read_excel(file_path, engine='openpyxl')

# Step 2: Sentiment Analysis - Function to analyze sentiment
def analyze_sentiment(Review):
    """Returns the sentiment polarity of the text."""
    blob = TextBlob(Review)
    return blob.sentiment.polarity

df['Sentiment'] = df['Review'].apply(analyze_sentiment)

# Step 3: Classify sentiment as Positive, Negative, or Neutral
def classify_sentiment(polarity):
    if polarity > 0:
        return 'Positive'
    elif polarity < 0:
        return 'Negative'
    else:
        return 'Neutral'

df['Sentiment_Label'] = df['Sentiment'].apply(classify_sentiment)

# Step 4: Keyword extraction for sentiment analysis
from sklearn.feature_extraction.text import CountVectorizer

def extract_keywords(text, n=10):
    """Extracts the most frequent n words from the text."""
    vectorizer = CountVectorizer(stop_words='english', max_features=n)
    x = vectorizer.fit_transform([text])
    return vectorizer.get_feature_names_out()

df['Keywords'] = df['Review'].apply(lambda x: extract_keywords(x, n=5))  # Extract top 5 keywords for each review

# Step 5: Extract important features (frequent words in positive and negative reviews)
def get_most_common_words(df, sentiment_label, n=20):
    """Get the most common words from reviews with a specific sentiment."""
    reviews = df[df['Sentiment_Label'] == sentiment_label]['Review']
    all_words = ' '.join(reviews).lower().split()
    most_common_words = Counter(all_words).most_common(n)
    return most_common_words

positive_keywords = get_most_common_words(df, 'Positive', 20)
negative_keywords = get_most_common_words(df, 'Negative', 20)

# Step 6: Negative feature identification
negative_words = ['bad', 'poor', 'terrible', 'worse', 'disappointing', 'not', 'uncomfortable', 'horrible', 'useless']
def extract_negative_features(review, negative_keywords):
    """Identifies the presence of negative features in a review."""
    return [word for word in negative_keywords if word in review.lower()]

df['Negative_Features'] = df['Review'].apply(lambda x: extract_negative_features(x, negative_words))

# Step 7: Word cloud generation (optional)
def generate_word_cloud(df, sentiment_label):
    """Generate a word cloud for a given sentiment label."""
    reviews = ' '.join(df[df['Sentiment_Label'] == sentiment_label]['Review'])
    wordcloud = WordCloud(stopwords='english', background_color='white', width=800, height=400).generate(reviews)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(f'Word Cloud for {sentiment_label} Reviews')
    plt.show()

# Generate word cloud for positive reviews
generate_word_cloud(df, 'Positive')

# Generate word cloud for negative reviews
generate_word_cloud(df, 'Negative')

# Step 8: Output the results
print(df[['Review', 'Sentiment', 'Sentiment_Label', 'Keywords', 'Negative_Features']])

# Optional: Save the results to a new Excel file
df.to_excel('sentiment_analysis_with_keywords_output.xlsx', index=False)
