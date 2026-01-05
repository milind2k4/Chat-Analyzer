from collections import defaultdict
from helpers import *

# --- (Function 1) Extract Daily Counts ---
def extract_messages_per_day(filepath, start_date=None, end_date=None):
    message_counts = defaultdict(int)
    date_format = "%d/%m/%Y"
    print("\nProcessing file for daily counts...")

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                date_obj, author = parse_line(line, date_format)
                if author and filter_by_date(date_obj, start_date, end_date):
                    message_counts[date_obj] += 1
        
        print(f"File processed. Found messages across {len(message_counts)} days.")
        return message_counts
    except FileNotFoundError:
        print(f"Error: The file '{filepath}' was not found.")
        return None
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return None

# --- (Function 2) Extract Author Counts ---
def extract_messages_per_person(filepath, start_date=None, end_date=None):
    author_counts = defaultdict(int)
    date_format = "%d/%m/%Y"
    print("\nProcessing file for author counts...")

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                date_obj, author = parse_line(line, date_format)
                if author and filter_by_date(date_obj, start_date, end_date):
                    author_counts[author] += 1
        
        print(f"File processed. Found messages from {len(author_counts)} authors.")
        return author_counts
    except FileNotFoundError:
        print(f"Error: The file '{filepath}' was not found.")
        return None
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return None

# --- (Function 3) Extract Daily Author Counts ---
def extract_messages_per_person_per_day(filepath, start_date=None, end_date=None):
    """
    Parses a chat file and counts messages per person, per day.
    Returns: {date: {author: count, ...}, ...}
    """
    daily_author_counts = defaultdict(lambda: defaultdict(int))
    date_format = "%d/%m/%Y"
    print("\nProcessing file for daily author counts...")

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                date_obj, author = parse_line(line, date_format)
                if author and filter_by_date(date_obj, start_date, end_date):
                    daily_author_counts[date_obj][author] += 1
        
        print(f"File processed. Found data across {len(daily_author_counts)} days.")
        return daily_author_counts
    except FileNotFoundError:
        print(f"Error: The file '{filepath}' was not found.")
        return None
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return None