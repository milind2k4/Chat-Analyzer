import sys
from helpers import *
from data_extraction import *
from plot import *

# --- Main Program Execution ---
if __name__ == "__main__":
    
    # 1. SET FILE PATH
    chat_file_path = 'WhatsApp Chat with 𝐎𝐣𝐨𝐮-𝐒𝐚𝐦𝐚✨.txt'
    
    # 2. GET OPTIONAL DATE RANGE
    print("--- WhatsApp Chat Analyzer ---")
    print("Please enter the date range (optional).")
    print("Press Enter at both prompts to analyze the entire file.\n")
    
    start_date = get_date_input("Enter start date")
    end_date = get_date_input("Enter end date")

    if start_date and end_date and start_date > end_date:
        print(f"Error: Start date is after end date.")
        sys.exit()

    # 3. CHOOSE ANALYSIS TYPE
    print("\nWhat analysis would you like to run?")
    print("  1. Messages per Day (Total)")
    print("  2. Messages per Person (Total)")
    print("  3. Messages per Person per Day (Grouped Chart)")
    print("  4. All")
    
    choice = ""
    while choice not in ['1', '2', '3', '4']:
        choice = input("Enter your choice (1-4): ")

    # 4. RUN CHOSEN ANALYSIS
    
    if choice == '1' or choice == '4':
        daily_data = extract_messages_per_day(chat_file_path, start_date, end_date)
        if daily_data:
            plot_daily_graph(daily_data, start_date, end_date)
        else:
            print("Could not generate daily plot (file error or no data).")

    if choice == '2' or choice == '4':
        author_data = extract_messages_per_person(chat_file_path, start_date, end_date)
        if author_data:
            plot_author_graph(author_data)
        else:
            print("Could not generate author plot (file error or no data).")

    if choice == '3' or choice == '4':
        daily_author_data = extract_messages_per_person_per_day(chat_file_path, start_date, end_date)
        if daily_author_data:
            plot_daily_author_graph(daily_author_data, start_date, end_date)
        else:
            print("Could not generate daily author plot (file error or no data).")

    print("\nAnalysis complete.")