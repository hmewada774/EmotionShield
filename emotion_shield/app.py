from flask import Flask, render_template, request, jsonify
import joblib
import os
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

app = Flask(__name__)

# Load model and vectorizer
MODEL_PATH = os.path.join('model', 'emotion_model.pkl')
VECTORIZER_PATH = os.path.join('model', 'vectorizer.pkl')

try:
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
except:
    # Fallback if model doesn't exist yet during initial setup
    model = None
    vectorizer = None

# Comprehensive Rule-based categories
RULES = {
    'urgency': {
        'words': ['urgent', 'immediately', 'now', 'deadline', 'last chance', 'hurry', 'act fast', 'soon', 'expiring', 'expires', 'limited time', 'within 10 minutes', 'within hour', 'today only'],
        'weight': 0.3,
        'label': 'Artificial Urgency',
        'explanation': 'Creates pressure to force a quick decision without verification.'
    },
    'authority': {
        'words': ['dean', 'admin', 'legal notice', 'compliance', 'official', 'director', 'department', 'university', 'registrar', 'security department', 'it support', 'management', 'office of', 'administration'],
        'weight': 0.2,
        'label': 'Authority Impersonation',
        'explanation': 'Claims to be from an official department to gain trust or compliance.'
    },
    'fear': {
        'words': ['suspended', 'violation', 'penalty', 'cancelled', 'blocked', 'breach', 'warning', 'locked', 'danger', 'unauthorized', 'suspicious', 'termination', 'legal action', 'revoked'],
        'weight': 0.35,
        'label': 'Fear-based Language',
        'explanation': 'Uses intimidating language or threats of negative consequences to cause panic.'
    },
    'reward': {
        'words': ['free', 'scholarship approved', 'exclusive offer', 'prize', 'winner', 'awarded', 'grant', 'gift', 'congratulations', 'claim now', 'cash', 'reward', 'fund'],
        'weight': 0.25,
        'label': 'Reward Bait',
        'explanation': 'Promises benefits or rewards to lure you into taking action.'
    },
    'consequences': {
        'words': ['access denied', 'disabled', 'revoked', 'illegal', 'prosecuted', 'fined', 'penalty fee'],
        'weight': 0.2,
        'label': 'Consequences of Inaction',
        'explanation': 'Implicitly or explicitly threatens loss of service if action is not taken.'
    }
}

SAFE_RULES = {
    'informational': {
        'words': ['meeting tomorrow', 'library hours', 'reminder', 'schedule', 'event', 'workshop', 'open', 'closed', 'update', 'newsletter', 'announcement', 'thank you', 'best regards'],
        'label': 'Informational Tone',
        'explanation': 'The message is purely informational without creating pressure.'
    },
    'neutral': {
        'words': ['if you have questions', 'feel free to', 'contact us at', 'available', 'please submit', 'by friday'],
        'label': 'Neutral Language',
        'explanation': 'Uses polite and professional language typical of routine academic communication.'
    }
}

def preprocess_text(text):
    text = str(text).lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    tokens = text.split()
    try:
        stop_words = set(stopwords.words('english'))
        tokens = [t for t in tokens if t not in stop_words]
    except:
        pass
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(t) for t in tokens]
    return " ".join(tokens)

def analyze_message(message):
    message_lower = message.lower()
    
    # 1. Detected Risk Factors
    detected_risks = []
    rule_score = 0
    trigger_words = []
    
    for key, rule in RULES.items():
        found_in_rule = []
        for word in rule['words']:
            if word in message_lower:
                found_in_rule.append(word)
                trigger_words.append(word)
        
        if found_in_rule:
            detected_risks.append({
                'label': rule['label'],
                'explanation': rule['explanation'],
                'triggers': found_in_rule
            })
            rule_score += rule['weight']

    # 2. Detected Safe Signals
    detected_safe = []
    for key, rule in SAFE_RULES.items():
        found_in_rule = []
        for word in rule['words']:
            if word in message_lower:
                found_in_rule.append(word)
        
        if found_in_rule:
            detected_safe.append({
                'label': rule['label'],
                'explanation': rule['explanation'],
                'triggers': found_in_rule
            })

    # 3. ML Score
    ml_prob = 0.5 # Default
    if model and vectorizer:
        clean_msg = preprocess_text(message)
        vector = vectorizer.transform([clean_msg])
        ml_prob = model.predict_proba(vector)[0][1]

    # 4. Final Weighted Score
    # Normalize rule score to max 1.0
    norm_rule_score = min(rule_score, 1.0)
    final_score = (ml_prob * 0.6 + norm_rule_score * 0.4) * 100
    
    # Logic for safe messages (if safe signals outnumber or outweigh risk)
    if not detected_risks and detected_safe:
        final_score = max(5, final_score - 40) # Drastically lower if only safe signals
    
    final_score = round(final_score, 1)
    
    # 5. Risk Level and Color
    if final_score < 30:
        risk_level = "LOW"
        risk_color = "#238636"
    elif final_score < 70:
        risk_level = "MEDIUM"
        risk_color = "#d29922"
    else:
        risk_level = "HIGH"
        risk_color = "#f85149"

    # 6. Overall Explanation & Actions
    if risk_level == "HIGH":
        summary = "This message attempts to create panic or extreme interest using urgency and authority to force action without verification."
        action = "DO NOT click links or provide info. Verify by contacting the sender via a known, official channel."
    elif risk_level == "MEDIUM":
        summary = "This message contains suspicious patterns that could be manipulative. Exercise caution."
        action = "Check the sender's actual email address and avoid clicking links directly."
    else:
        summary = "This message appears to be routine communication and lacks typical manipulative triggers."
        action = "Safe to read, but always remain vigilant for unexpected requests."

    # 7. Legitimate Elements
    legit_elements = []
    if len(message) > 50: legit_elements.append("Complete sentence structure")
    if "regards" in message_lower or "sincerely" in message_lower: legit_elements.append("Professional closing")
    if "hi" in message_lower or "dear" in message_lower: legit_elements.append("Standard greeting")

    return {
        'score': final_score,
        'level': risk_level,
        'color': risk_color,
        'risks': detected_risks,
        'safe_signals': detected_safe,
        'explanation': summary,
        'action': action,
        'legit_elements': legit_elements,
        'confidence': round(ml_prob * 100, 1)
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    message = request.form.get('message', '')
    if not message:
        return "No message provided", 400
    
    result = analyze_message(message)
    return render_template('result.html', **result)

if __name__ == '__main__':
    app.run(debug=True)

