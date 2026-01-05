import json
from datetime import datetime, timezone
import pytz # You must install this library: pip install pytz

# --- Configuration ---
INPUT_FILE = "Database/result/916204411717swhatsappnet.json"
OUTPUT_FILE = "formatted_chat.json"
AUTHOR_ME = "Milind"
AUTHOR_THEM = "Ojou sama"
TIMEZONE_IST = pytz.timezone('Asia/Kolkata')
# ---------------------

def convert_timestamp_to_iso_string(ts):
    """Converts a Unix timestamp to a human-readable ISO 8601 string in IST."""
    try:
        # Create a datetime object in UTC from the timestamp
        dt_utc = datetime.fromtimestamp(ts, tz=timezone.utc)
        # Convert it to the desired IST timezone
        dt_ist = dt_utc.astimezone(TIMEZONE_IST)
        # Format it as a standard ISO 8601 string
        return dt_ist.isoformat()
    except Exception as e:
        print(f"Error converting timestamp {ts}: {e}")
        return None

def process_chat_data(chat_data):
    """
    Processes the raw chat dictionary into a formatted list of messages.
    """
    
    # First Pass: Build a map of all messages by their key_id.
    # This is essential for looking up the content of replied-to messages.
    key_id_to_message_map = {}
    for msg in chat_data.values():
        if "key_id" in msg and msg["key_id"]:
            key_id_to_message_map[msg["key_id"]] = msg

    formatted_messages = []
    
    # Sort messages by timestamp to ensure the final list is chronological
    try:
        sorted_message_items = sorted(
            chat_data.items(), 
            key=lambda item: item[1].get("timestamp", 0)
        )
    except Exception as e:
        print(f"Warning: Could not sort messages by timestamp. {e}")
        sorted_message_items = chat_data.items()

    # Second Pass: Transform each message
    for _, msg in sorted_message_items:
        
        # Filter out messages without a timestamp (e.g., metadata)
        if not msg.get("timestamp"):
            continue 

        new_msg = {}

        # 1. Convert author
        new_msg["author"] = AUTHOR_ME if msg.get("from_me") else AUTHOR_THEM

        # 2. Convert timestamp to ISO 8601 format
        new_msg["timestamp"] = convert_timestamp_to_iso_string(msg["timestamp"])

        # 3. --- NEW: Consolidate 'data' and 'caption' into 'text' ---
        data_content = msg.get("data")
        caption_content = msg.get("caption")
        
        # Prioritize 'data', but fall back to 'caption'
        new_msg["text"] = data_content if data_content is not None else caption_content
        new_msg["media"] = msg.get("media", False)
        
        # 4. Handle replies and rename "quoted_data" to "reply_to"
        reply_key = msg.get("reply")
        quoted_data = msg.get("quoted_data")
        reply_to_content = None

        if reply_key:
            if quoted_data:
                reply_to_content = quoted_data
            else:
                original_msg = key_id_to_message_map.get(reply_key)
                if original_msg:
                    # The content we want is the *caption* of the original message
                    # (which is now in its 'text' field if we processed it,
                    # but safer to look at the original data)
                    reply_to_content = original_msg.get("caption")
                    if not reply_to_content:
                        reply_to_content = "[Replied to a media message]"
                else:
                    reply_to_content = "[Replied to a message that could not be found]"

        new_msg["reply_to"] = reply_to_content
            
        # 5. --- NEW: Aggressive filtering ---
        # Skip any message that has no text, no media, and no reply context
        is_text_empty = not new_msg.get("text") # Checks for None or ""
        is_media_false = not new_msg.get("media")
        is_reply_to_empty = not new_msg.get("reply_to")
        
        if is_text_empty and is_media_false and is_reply_to_empty:
            continue # Skip this "empty" message
            
        formatted_messages.append(new_msg)

    return formatted_messages

def main():
    """
    Main function to load, process, and save the chat data.
    """
    try:
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Input file '{INPUT_FILE}' not found.")
        return
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{INPUT_FILE}'.")
        return
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return

    print(f"Loaded data from '{INPUT_FILE}'.")

    if not isinstance(data, dict) or not data:
        print(f"Error: Expected a non-empty JSON object, but got {type(data)}")
        return
        
    try:
        first_key = next(iter(data))
    except StopIteration:
        print("Error: The JSON file is an empty object.")
        return
        
    chat_content = data[first_key]
    
    if not isinstance(chat_content, dict) or "messages" not in chat_content:
        print(f"Error: Could not find 'messages' key in the JSON structure for chat {first_key}.")
        return
        
    message_data = chat_content["messages"]
    
    if not isinstance(message_data, dict):
        print(f"Error: 'messages' key does not contain a valid message dictionary.")
        return
    
    print(f"Found {len(message_data)} messages for chat {first_key}.")
    
    # Process the data
    formatted_data = process_chat_data(message_data)
    
    # Save the new formatted data
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(formatted_data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"An error occurred while writing the file: {e}")
        return

    print(f"Successfully processed and saved formatted data to '{OUTPUT_FILE}'.")

if __name__ == "__main__":
    main()

