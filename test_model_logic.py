import joblib
import os
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Ensure NLTK data is available
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)

def preprocess_text(text):
    text = str(text).lower()
    # Keep numbers as they carry urgency/reward context (e.g. $1000, 10 mins)
    text = re.sub(r'[^a-z0-9\s]', '', text)
    tokens = text.split()
    stop_words = set(stopwords.words('english'))
    tokens = [t for t in tokens if t not in stop_words]
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(t) for t in tokens]
    return " ".join(tokens)

# Load model and vectorizer
base_dir = r'c:\Users\hmewa\OneDrive\Desktop\emotion_shield\emotion_shield'
model = joblib.load(os.path.join(base_dir, 'model', 'emotion_model.pkl'))
vectorizer = joblib.load(os.path.join(base_dir, 'model', 'vectorizer.pkl'))

test_cases = [
    "URGENT: Your student account will be suspended in 10 minutes. Click here now!",
    "Hi, do you want to grab coffee later?",
    "Official Notice from the Dean: Immediate action required regarding your scholarship.",
    "Congratulations! You won a $1000 gift card. Click to claim.",
    "Hey, don't forget the library books are due tomorrow."
]

print("--- Model Testing ---")
for text in test_cases:
    clean = preprocess_text(text)
    vec = vectorizer.transform([clean])
    prob = model.predict_proba(vec)[0][1]
    pred = model.predict(vec)[0]
    print(f"Text: {text}")
    print(f"  Clean: {clean}")
    print(f"  Prob(Manipulative): {prob:.4f}")
    print(f"  Prediction: {'Manipulative' if pred == 1 else 'Safe'}")
    print("-" * 20)
