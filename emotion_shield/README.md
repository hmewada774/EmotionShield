# EmotionShield – AI-based Emotional Manipulation Detection

## 🛡️ Project Overview
**EmotionShield** is a cybersecurity tool designed for students to detect emotional manipulation patterns in emails and messages. Unlike traditional phishing filters that look for suspicious links, EmotionShield analyzes the **emotional tone** and **linguistic triggers** used to exploit human psychology.

### 🎯 Key Features
- **AI-Powered Analysis:** Uses a Machine Learning model (Logistic Regression + TF-IDF) trained on manipulative vs. safe communication.
- **Rule-Based Enhancement:** Detects specific triggers like Artificial Urgency, Authority Impersonation, Fear-based Language, Reward Bait, and Time Pressure.
- **Explainable Risk Score:** Provides a 0–100 risk score with a clear breakdown of *why* a message is flagged.
- **Safe Action Advice:** Practical steps for students to take when a high-risk message is detected.
- **Privacy First:** Messages are processed in memory and never logged or stored.

---

## 🏗️ Tech Stack
- **Backend:** Python, Flask
- **ML:** Scikit-learn, Pandas, NLTK, Joblib
- **Frontend:** Vanilla HTML5, CSS3 (Cyber Theme), JavaScript

---

## 🚀 How to Run Locally

### 1. Clone or Extract the Project
Ensure you are in the `emotion_shield` directory.

### 2. Install Dependencies
It is recommended to use a virtual environment.
```bash
pip install -r requirements.txt
```

### 3. Generate the Dataset and Train the Model
The project includes a synthetic dataset generator and a training script. 
```bash
# Generate the sample dataset
python dataset_generator.py

# Train the ML model (this will also download necessary NLTK data)
python model/train_model.py
```

### 4. Start the Application
```bash
python app.py
```
Visit `http://127.0.0.1:5000` in your browser.

---

## 📁 Project Structure
- `app.py`: Main Flask application logic.
- `model/`: Contains training script and serialized ML models (`.pkl`).
- `dataset/`: Contains multiple integrated datasets (`final_training_dataset.csv` with 13,000+ rows).
- `static/`: Frontend assets (modern CSS, interactive JS).
- `templates/`: HTML pages (Index and Result views).

---

## 🔐 Privacy Note
EmotionShield is designed with student privacy in mind. No data is stored on the server. All analysis is ephemeral and cleared once the session ends.

---
**Developed for Hackathon: AI + Cybersecurity & Privacy for Students.**
