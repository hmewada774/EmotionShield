import pandas as pd
import os

data = [
    # Manipulative (Label 1)
    ["URGENT: Your student account will be suspended in 10 minutes. Click here to verify now!", 1],
    ["Official Notice from the Dean: Immediate action required regarding your scholarship eligibility.", 1],
    ["Final Warning: Your library access has been cancelled due to a security violation. Reactivate now.", 1],
    ["Congratulations! You have been selected for an exclusive $5000 reward. Claim your prize here!", 1],
    ["Legal Notice: A penalty has been issued against your student ID. View compliance details immediately.", 1],
    ["Your password expires in 1 hour. Follow this link to avoid being blocked from the system.", 1],
    ["Security Alert: We detected an unauthorized login to your portal from a new device. Secure it now.", 1],
    ["Exclusive Offer: Get free access to premium study materials for the next 5 minutes only.", 1],
    ["Dean's Office: Your internship application is at risk of being rejected. Update your info now.", 1],
    ["IMPORTANT: Administrative hold placed on your account. Contact legal notice department immediately.", 1],
    ["Last chance to claim your student discount before the deadline tonight!", 1],
    ["Violation detected in your last assignment submission. Review the penalty details in this link.", 1],
    ["System Update: Your email will be deactivated unless you confirm your identity within 30 minutes.", 1],
    ["Action Required: Your student health insurance has been suspended. Re-enroll now.", 1],
    ["Emergency Alert: Report to the compliance office or face immediate suspension.", 1],
    ["You have been awarded a special grant! Please provide your bank details to receive the funds.", 1],
    ["Official notification: Your campus parking permit has been revoked. Click to appeal.", 1],
    ["Your tuition payment failed. Pay within 20 minutes to avoid late fees and cancellation.", 1],
    ["Winner! You are one of the 10 lucky students to win a new laptop. Click to claim.", 1],
    ["Urgent message from IT: Complete the security audit now or your network access will be cut off.", 1],

    # Safe (Label 0)
    ["Hey, don't forget we have a group study session in the library at 4 PM tomorrow.", 0],
    ["The campus cafeteria will be serving special tacos this Friday for lunch.", 0],
    ["Hi! I just wanted to share the notes from today's Biology lecture. Hope they help.", 0],
    ["Reminder: The career fair is happening on Wednesday in the main hall from 10 AM to 3 PM.", 0],
    ["Can you please return my textbook when you're done with it? Thanks!", 0],
    ["The basketball game starts at 7 PM tonight. Let's go cheer for our team!", 0],
    ["Hello students, the library hours have been extended for the finals week.", 0],
    ["Are you coming to the club meeting today? We're discussing the new project.", 0],
    ["Just a quick note to say Happy Birthday! Hope you have a great day.", 0],
    ["The student union is hosting a movie night this Friday. Free popcorn for everyone!", 0],
    ["Hi Mom, I'll be coming home this weekend for the holidays. See you soon.", 0],
    ["Please find attached the syllabus for the 'Introduction to Psychology' course.", 0],
    ["Great job on the presentation today! You really covered all the key points.", 0],
    ["The gym is undergoing maintenance this Sunday and will be closed from 8 AM to 12 PM.", 0],
    ["Don't forget to submit your lab report by the end of the week. No rush!", 0],
    ["Hi there, I'm looking for a roommate for the next semester. Let me know if interested.", 0],
    ["The weather forecast says it might rain tomorrow, better bring an umbrella.", 0],
    ["Thank you for volunteering at the food drive last Saturday. Your help was appreciated.", 0],
    ["Let's meet at the coffee shop after class to discuss our group assignment.", 0],
    ["The student portal will be down for scheduled maintenance tonight from midnight to 2 AM.", 0]
]

df = pd.DataFrame(data, columns=['text', 'label'])
output_path = r'c:\Users\hmewa\OneDrive\Desktop\emotion_shield\emotion_shield\dataset\sample_dataset.csv'
df.to_csv(output_path, index=False)
print(f"Dataset created with {len(df)} rows at {output_path}")
