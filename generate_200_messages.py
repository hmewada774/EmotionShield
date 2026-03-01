import random
import pandas as pd
import os

# Categories for generation
authorities = ["Office of the Dean", "IT Administration", "Financial Aid Office", "Campus Security", "Registrar's Office", "Library Services", "Student Health Center", "Academic Affairs", "Legal Department", "Compliance Division"]
subjects = ["Scholarship", "Student Account", "Email Access", "Library Privileges", "Housing Application", "Parking Permit", "Course Registration", "Financial Aid", "Graduation Eligibility", "Campus ID"]
actions = ["suspended", "deactivated", "cancelled", "placed on hold", "flagged for review", "revoked", "locked", "terminated"]
reasons = ["a security breach", "a policy violation", "missing documentation", "suspicious activity", "an unpaid balance", "failed verification", "administrative error", "unauthorized access attempt"]
urgencies = ["immediately", "within 10 minutes", "by end of the day", "before midnight", "in the next hour", "without delay", "to avoid permanent loss"]
rewards = ["$1000 Emergency Grant", "Presidential Scholarship", "Exclusive Prize Pack", "Free Semester of Books", "Tech Upgrade Voucher", "Campus Gift Card", "Dining Hall Credit", "Research Stipend"]

templates = [
    "{authority} Alert: Your {subject} has been {action} due to {reason}. You must verify your identity {urgency} to prevent permanent closure.",
    "URGENT NOTICE: A {subject} violation was detected in your recent activity. Failure to take action {urgency} will result in a {action} status.",
    "Final Warning from {authority}: Your access will be {action} at midnight. Click here to update your compliance documentation {urgency}.",
    "Congratulations! You've been selected by the {authority} for a {reward}. Claim your {reward} {urgency} before the link expires.",
    "SECURITY BREACH: The {authority} detected a login attempt from a new device. Your {subject} is now {action}. Unlock it {urgency} here.",
    "Official {authority} Statement: Your {subject} status is currently {action}. To restore privileges, complete the mandatory review {urgency}.",
    "Your {subject} payment failed. The {authority} will issue a penalty of $250 if not resolved {urgency}. Pay now to avoid further {action}.",
    "Exclusive {reward} approved for you! The {authority} requires your bank details {urgency} to deposit the funds.",
    "LEGAL NOTICE: The {authority} has flagged your {subject} for {reason}. You must appear for a hearing unless you resolve the matter {urgency}.",
    "System Update: All {subject} credentials must be re-verified. Neglecting this task {urgency} will result in your account being {action}."
]

manipulative_messages = []

# Generate 200 manipulative messages
for i in range(200):
    template = random.choice(templates)
    msg = template.format(
        authority=random.choice(authorities),
        subject=random.choice(subjects),
        action=random.choice(actions),
        reason=random.choice(reasons),
        urgency=random.choice(urgencies),
        reward=random.choice(rewards)
    )
    manipulative_messages.append([msg, 1])

# Also generate ~150 safe messages to balance the dataset better (optional but good practice)
safe_contexts = [
    "Hey, do you want to grab coffee after the {subject} lecture?",
    "Reminder: The {authority} is hosting a workshop on {subject} tomorrow at 2 PM.",
    "I just finished the group work for {subject}. I'll send it over soon.",
    "Does anyone have the notes for the {subject} class we had yesterday?",
    "The {authority} has updated the {subject} handbook for the next semester.",
    "I'm looking forward to the {subject} project presentation next week!",
    "Hi, I noticed the {authority} changed their office hours for Friday.",
    "Could you help me with the {subject} assignment? I'm a bit stuck.",
    "The {authority} is offering free snacks at the student union tonight.",
    "Did you see the announcement about the {subject} exam schedule?"
]

safe_messages = []
for i in range(150):
    template = random.choice(safe_contexts)
    msg = template.format(
        authority=random.choice(authorities),
        subject=random.choice(subjects)
    )
    safe_messages.append([msg, 0])

# Combine with existing data or just create new one
all_data = manipulative_messages + safe_messages
df = pd.DataFrame(all_data, columns=['text', 'label'])

# Save path
output_path = r'c:\Users\hmewa\OneDrive\Desktop\emotion_shield\emotion_shield\dataset\sample_dataset.csv'
df.to_csv(output_path, index=False)

print(f"Generated {len(manipulative_messages)} manipulative and {len(safe_messages)} safe messages.")
print(f"Dataset updated at {output_path}")
