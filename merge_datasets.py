import pandas as pd
import os
import re

base_dir = r'c:\Users\hmewa\OneDrive\Desktop\emotion_shield\emotion_shield'
dataset_dir = os.path.join(base_dir, 'dataset')

# 1. Load our high-quality student manipulation dataset
large_df = pd.read_csv(os.path.join(dataset_dir, 'large_dataset.csv'))
# We want to give this dataset "priority" by duplicating it or making sure it's clean
large_df['source'] = 'student'

# 2. Load and CLEAN emails1.csv
emails1_path = os.path.join(dataset_dir, 'emails1.csv')
if os.path.exists(emails1_path):
    e1_df = pd.read_csv(emails1_path)
    e1_df = e1_df.rename(columns={'text': 'text', 'spam': 'label'})
    # CRITICAL: Remove "Subject: " prefix which is biasing the model
    e1_df['text'] = e1_df['text'].str.replace(r'^Subject: ', '', regex=True, flags=re.IGNORECASE)
    # Remove generic signatures or corporate-specific names if possible
    # (Just prefix removal is a huge start)
    e1_df['source'] = 'generic_email'
else:
    e1_df = pd.DataFrame(columns=['text', 'label', 'source'])

# 3. Load and CLEAN spam.csv
spam_path = os.path.join(dataset_dir, 'spam.csv')
if os.path.exists(spam_path):
    try:
        s_df = pd.read_csv(spam_path, encoding='latin-1')
        s_df = s_df[['v1', 'v2']].rename(columns={'v1': 'label', 'v2': 'text'})
        s_df['label'] = s_df['label'].map({'ham': 0, 'spam': 1})
        s_df['source'] = 'sms_spam'
    except:
        s_df = pd.DataFrame(columns=['text', 'label', 'source'])
else:
    s_df = pd.DataFrame(columns=['text', 'label', 'source'])

# Combine
# Let's oversample the student dataset right here to make it 50% of the data
other_data = pd.concat([e1_df, s_df], ignore_index=True)
other_data = other_data.dropna(subset=['text', 'label'])

# Oversample our "perfect" student data to match the size of the larger generic sets
# This forces the model to treat student-specific scams as core patterns
target_size = len(other_data) // 2
student_oversampled = large_df.sample(n=target_size, replace=True, random_state=42)

final_df = pd.concat([student_oversampled, other_data], ignore_index=True)
final_df = final_df.dropna(subset=['text', 'label'])

# Save
output_path = os.path.join(dataset_dir, 'final_training_dataset.csv')
final_df.to_csv(output_path, index=False)

print(f"Merged and Cleaned into {output_path}")
print(f"Total rows: {len(final_df)}")
print(f"Student data weight: {len(student_oversampled)} rows")
print(f"Generic data weight: {len(other_data)} rows")
print(f"Labels:\n{final_df['label'].value_counts()}")
