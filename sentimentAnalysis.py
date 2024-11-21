import pandas as pd
from textblob import TextBlob

def analyze_sentiment(Review):
    """Returns the sentiment polarity of the text."""
    blob = TextBlob(Review)
    return blob.sentiment.polarity

# Step 1: Load the Excel file
file_path = '/amazon_all_reviews_CsV_.xlsx'  # Replace with your actual file path
#sheet_name = 'amazon_all_reviews_CsV_'  # Modify based on your sheet name

# Use openpyxl engine for .xlsx files
df = pd.read_excel(file_path,engine='openpyxl')

# Step 2: Assuming the text data is in a column named 'Text' (change the column name if different)
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

# Step 4: Output the results
print(df[['Review', 'Sentiment', 'Sentiment_Label']])

# Optional: Save the results to a new Excel file
df.to_excel('sentiment_analysis_output.xlsx', index=False)  