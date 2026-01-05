import datetime
from collections import defaultdict

def get_date_input(prompt_message):
    """
    Asks the user for a date.
    Returns a datetime.date object or None if the user presses Enter.
    """
    date_format = "%d/%m/%Y"
    prompt = f"{prompt_message} (in {date_format}) or press Enter: "
    
    while True:
        date_str = input(prompt)
        if not date_str:
            return None
        try:
            date_obj = datetime.datetime.strptime(date_str, date_format).date()
            return date_obj
        except ValueError:
            print(f"Invalid date format. Please use '{date_format}' or press Enter.")
            
def filter_by_date(date_obj, start_date, end_date):
    """Checks if a date is within the optional range."""
    if (start_date and date_obj < start_date) or \
       (end_date and date_obj > end_date):
        return False
    return True

def parse_line(line, date_format):
    """
    Helper function to parse a single line.
    Returns (date_obj, author) or (None, None) if invalid.
    """
    try:
        # 1. Check for date
        date_str = line.split(',')[0]
        date_obj = datetime.datetime.strptime(date_str, date_format).date()

        # 2. Extract author
        hyphen_index = line.find(' - ')
        if hyphen_index == -1:
            return None, None # Not a user message (e.g., multi-line)
        
        colon_index = line.find(':', hyphen_index + 3) # Find colon *after* hyphen
        
        if colon_index > hyphen_index:
            # This is a user message: "date - author: message"
            author = line[hyphen_index + 3 : colon_index].strip()
            return date_obj, author
        else:
            return None, None # System message (e.g., "User left")
            
    except ValueError:
        return None, None # Failed date parsing (e.g., multi-line)
    except IndexError:
        return None, None # Malformed line