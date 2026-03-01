import pandas as pd
import random
import os

# Paths
base_dir = r'c:\Users\hmewa\OneDrive\Desktop\emotion_shield\emotion_shield'
input_path = os.path.join(base_dir, 'dataset', 'sample_dataset.csv')
output_path = os.path.join(base_dir, 'dataset', 'large_dataset.csv')

# Load the base dataset
df = pd.read_csv(input_path)

urgency_variations = ["5 minutes", "10 minutes", "30 minutes", "1 hour", "immediately"]
authority_variations = ["Dean", "Registrar", "Admin Office", "Compliance Team", "IT Department"]

expanded_rows = []

for _, row in df.iterrows():
    text = str(row["text"])
    label = row["label"]

    # Add the original row first
    expanded_rows.append({"text": text, "label": label})

    # Create 5 variations per row as requested
    for i in range(5):
        new_text = text
        
        if label == 1:
            # Note: This will only replace exact matches of "10 minutes" or "Dean"
            # Since the user logic is specific, we follow it but also try to catch "Office of the Dean" etc.
            new_text = new_text.replace("10 minutes", random.choice(urgency_variations))
            new_text = new_text.replace("Dean", random.choice(authority_variations))

        expanded_rows.append({"text": new_text, "label": label})

expanded_df = pd.DataFrame(expanded_rows)

# Save the new large dataset
expanded_df.to_csv(output_path, index=False)

print(f"Dataset expanded successfully! Total rows: {len(expanded_df)}")
print(f"Saved to: {output_path}")
