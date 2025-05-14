import pandas as pd
from datetime import datetime, timedelta
import subprocess

# Load the schedule
df = pd.read_csv('/Users/fareesah/Downloads/Fraser Hall Chore Schedule - Sheet1.csv')

# Constants
GROUP_CHAT_NAME = "Fraser Hall Girlies"
WEEK_1_START = datetime(2025, 4, 14)  # Monday of Week 1

# Calculate current week number
today = datetime.now()
week_number = ((today - WEEK_1_START).days // 7) + 1

# Ensure we don't go out of range
if week_number <= 0 or week_number > len(df):
    message = f"No chore data available for Week {week_number}."
else:
    week_data = df.iloc[week_number - 1]
    message_lines = [f"Fraser Hall Chores – Week {week_number}"]
    for chore, person in week_data.items():
        if "Week" not in chore:
            message_lines.append(f"- {chore.strip()}: {person.strip()}")
    message = "\n".join(message_lines)

    # Escape quotes for AppleScript
    message_applescript = message.replace('"', '\\"')

    # AppleScript to send message via iMessage
    apple_script = f'''
    tell application "Messages"
        set targetService to 1st service whose service type = iMessage
        set targetBuddy to buddy "{GROUP_CHAT_NAME}" of targetService
        send "{message_applescript}" to targetBuddy
    end tell
    '''

    # Run the AppleScript
    subprocess.run(["osascript", "-e", apple_script])
