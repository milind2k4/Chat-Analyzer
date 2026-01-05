import json
import os
from datetime import datetime

# --- Configuration ---
INPUT_FILE = "formatted_chat.json"
OUTPUT_DIR = "daily_chats"
# ---------------------

def get_filename_from_timestamp(iso_timestamp):
    """
    Parses ISO timestamp and returns a filename string like '22_nov'.
    """
    try:
        dt = datetime.fromisoformat(iso_timestamp)
        # Format: Day_Month (e.g., 22_Nov)
        date_str = dt.strftime("%d_%b")
        # Convert to lowercase to match request (22_nov)
        return date_str.lower()
    except ValueError:
        return "unknown_date"

def split_chat_by_day():
    # 1. Load the formatted chat data
    try:
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            messages = json.load(f)
    except FileNotFoundError:
        print(f"Error: Input file '{INPUT_FILE}' not found.")
        return
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{INPUT_FILE}'.")
        return

    # 2. Create output directory if it doesn't exist
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Created directory: {OUTPUT_DIR}")

    # 3. Group messages by day
    # Dictionary structure: { "22_nov": [msg1, msg2], "23_nov": [msg3] }
    daily_groups = {}

    print(f"Processing {len(messages)} messages...")

    for msg in messages:
        timestamp = msg.get("timestamp")
        if not timestamp:
            continue

        filename_key = get_filename_from_timestamp(timestamp)
        
        # If this is the first message for this day, initialize the list
        if filename_key not in daily_groups:
            daily_groups[filename_key] = []
        
        daily_groups[filename_key].append(msg)

    # 4. Write the grouped messages to files
    for date_key, day_messages in daily_groups.items():
        # Construct filename: daily_chats/22_nov.json
        filename = f"{date_key}.json"
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(day_messages, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error writing {filename}: {e}")

    print(f"Successfully split chat into {len(daily_groups)} files in the '{OUTPUT_DIR}' folder.")

if __name__ == "__main__":
    split_chat_by_day()