import pandas as pd
import numpy as np
import re
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import os

# Download necessary NLTK data
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

def preprocess_text(text):
    # Lowercasing
    text = str(text).lower()
    # Remove special characters but KEEP numbers (scams often use amounts/deadlines)
    text = re.sub(r'[^a-z0-9\s]', '', text)
    # Tokenization
    tokens = text.split()
    # Remove common stopwords but keep some context-heavy ones
    stop_words = set(stopwords.words('english'))
    # Optional: remove specific words that are definitely not useful
    tokens = [t for t in tokens if t not in stop_words]
    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(t) for t in tokens]
    return " ".join(tokens)

def train():
    # Load dataset
    dataset_path = os.path.join(os.path.dirname(__file__), '..', 'dataset', 'final_training_dataset.csv')
    df = pd.read_csv(dataset_path)
    
    # Preprocess
    df['clean_text'] = df['text'].astype(str).apply(preprocess_text)

    # Feature extraction: 
    # Use min_df to skip extremely rare words, max_df to skip too common words
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2), 
        max_features=8000,
        min_df=2,
        max_df=0.8
    )
    X = vectorizer.fit_transform(df['clean_text'])
    y = df['label']

    # Train model with balanced weights and high regularization
    model = LogisticRegression(class_weight='balanced', C=5.0, max_iter=2000)
    model.fit(X, y)

    # Save model and vectorizer
    model_dir = os.path.dirname(__file__)
    joblib.dump(model, os.path.join(model_dir, 'emotion_model.pkl'))
    joblib.dump(vectorizer, os.path.join(model_dir, 'vectorizer.pkl'))

    print("Model and vectorizer saved successfully!")

if __name__ == "__main__":
    train()
