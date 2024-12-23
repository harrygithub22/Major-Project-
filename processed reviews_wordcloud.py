import pandas as pd
import re
from gensim import corpora
from gensim.models import LdaModel
import pyLDAvis.gensim_models
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Define a basic list of stopwords manually (can be extended as needed)
stopwords = set([
    "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours",
    "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself",
    "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", 
    "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if",
    "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between",
    "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out",
    "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why",
    "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", 
    "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", 
    "now", "d", "ll", "m", "o", "re", "ve", "y", "ain", "aren", "couldn", "didn", "doesn", "hadn", 
    "hasn", "haven", "isn", "ma", "mightn", "mustn", "needn", "shan", "shouldn", "wasn", "weren", "won", "wouldn"
])

# Load the Excel file containing the customer reviews or text data
file_path = '/content/amazon_all_reviews_CsV_.xlsx'  # Replace with the path to your file
df = pd.read_excel(file_path)

# Ensure 'Text' column exists in the dataframe
if 'Text' not in df.columns:
    print("The column 'Text' is not found in the Excel sheet. Please check the column name.")
else:
    # Preprocess and clean text data
    def preprocess_text(text):
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'http\S+', '', text)
        
        # Remove non-alphabetic characters (punctuation, numbers, etc.)
        text = re.sub(r'[^a-z\s]', '', text)
        
        # Tokenize by splitting on spaces
        tokens = text.split()
        
        # Remove stopwords (using the predefined list)
        tokens = [word for word in tokens if word not in stopwords]
        
        # Manual lemmatization (basic form using common word reductions)
        lemmatization_map = {
            'running': 'run', 'ran': 'run', 'better': 'good', 'worse': 'bad', 
            'eating': 'eat', 'eats': 'eat', 'jumped': 'jump', 'jumps': 'jump',
            'flies': 'fly', 'drove': 'drive', 'drives': 'drive', 'walking': 'walk',
            'walked': 'walk', 'going': 'go', 'went': 'go', 'does': 'do', 'did': 'do'
        }
        
        tokens = [lemmatization_map.get(word, word) for word in tokens]
        
        return tokens

    # Apply text preprocessing to the 'Text' column
    df['Processed_Text'] = df['Text'].apply(lambda x: preprocess_text(str(x)))
    
    # Create a dictionary (mapping of words to ids)
    dictionary = corpora.Dictionary(df['Processed_Text'])
    
    # Create a corpus (collection of bag-of-words representations)
    corpus = [dictionary.doc2bow(text) for text in df['Processed_Text']]
    
    # Apply LDA (Latent Dirichlet Allocation)
    num_topics = 5  # Number of topics to extract
    lda_model = LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=15)
    
    # Display the topics found by LDA
    print("Top topics found by LDA:")
    topics = lda_model.print_topics(num_words=5)  # Display top 5 words for each topic
    for topic in topics:
        print(topic)

# Visualize the topics using pyLDAvis
vis = pyLDAvis.gensim_models.prepare(lda_model, corpus, dictionary)

# Instead of pyLDAvis.show(vis), use:
pyLDAvis.display(vis)  # or pyLDAvis.enable_notebook() followed by display(vis) 
    
    # Word Frequency Analysis (after stopwords removal)
all_tokens = [word for text in df['Processed_Text'] for word in text]
word_counts = Counter(all_tokens)
common_words = word_counts.most_common(20)
    
    # Plot the top 20 most common words
words, counts = zip(*common_words)
plt.figure(figsize=(10, 6))
plt.barh(words, counts)
plt.xlabel('Word Count')
plt.title('Top 20 Most Common Words')
plt.gca().invert_yaxis()  # To display the top words on top
plt.show()
    
    # Word Cloud for most frequent words
wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_counts)
plt.figure(figsize=(10, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Word Cloud of Most Frequent Words')
plt.show()
    
    # Add a column to store the dominant topic for each review
def get_dominant_topic(corpus, lda_model):
    topic_percents = lda_model.get_document_topics(corpus)
    dominant_topics = [max(topic_percent, key=lambda x: x[1])[0] for topic_percent in topic_percents]
    return dominant_topics
    
df['Dominant_Topic'] = get_dominant_topic(corpus, lda_model)
    
    # Optionally, save the processed reviews with topics to a new Excel file
df.to_excel('processed_reviews_with_topics.xlsx', index=False)
