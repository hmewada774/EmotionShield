import joblib
import os
import numpy as np

base_dir = r'c:\Users\hmewa\OneDrive\Desktop\emotion_shield\emotion_shield'
model = joblib.load(os.path.join(base_dir, 'model', 'emotion_model.pkl'))
vectorizer = joblib.load(os.path.join(base_dir, 'model', 'vectorizer.pkl'))

feature_names = vectorizer.get_feature_names_out()
coefficients = model.coef_[0]

# Get top 20 positive and negative features
top_positive_indices = np.argsort(coefficients)[-20:]
top_negative_indices = np.argsort(coefficients)[:20]

print("--- Top 20 Manipulative Features ---")
for i in reversed(top_positive_indices):
    print(f"{feature_names[i]}: {coefficients[i]:.4f}")

print("\n--- Top 20 Safe Features ---")
for i in top_negative_indices:
    print(f"{feature_names[i]}: {coefficients[i]:.4f}")
