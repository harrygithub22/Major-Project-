import pandas as pd
import re
import string

# Function to clean and tokenize text without using NLTK's download feature
def clean_and_tokenize(text):
    # Convert text to lowercase
    text = text.lower()
    
    # Remove non-alphabetic characters (punctuation, numbers, etc.)
    text = re.sub(r'[^a-z\s]', '', text)
    
    # Tokenize the text into words (split by whitespace)
    tokens = text.split()
    
    return tokens

# Load Excel file (ensure the path is correct)
file_path = '/content/amazon_all_reviews_CsV_.xlsx'  # Replace with the path to your file
df = pd.read_excel(file_path)

# Let's assume the data you're interested in is in a column named 'Text'
# You can change the column name accordingly if needed
if 'Text' not in df.columns:
    print("The column 'Text' is not found in the Excel sheet. Please check the column name.")
else:
    # Apply cleaning and tokenization to each row in the 'Text' column
    df['Cleaned_Tokenized'] = df['Text'].apply(lambda x: clean_and_tokenize(str(x)))
    
    # Display the results
    print(df[['Text', 'Cleaned_Tokenized']].head())  # Show the first few rows for verification

    # Optionally, save the cleaned and tokenized data back to a new Excel file
    df.to_excel('cleaned_tokenized_output.xlsx', index=False)
