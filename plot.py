import plotly.graph_objects as go

# --- (Plot 1) Plot Daily Graph ---
def plot_daily_graph(message_counts, start_date=None, end_date=None):
    if not message_counts:
        print("No daily message data found to plot.")
        return
    print("Generating interactive 'Messages per Day' plot...")
    
    sorted_items = sorted(message_counts.items())
    dates, counts = zip(*sorted_items)
    
    fig = go.Figure(data=[go.Bar(x=dates, y=counts)])
    
    title_text = "Daily WhatsApp Message Count (User Messages Only)"
    if start_date and end_date:
        title_text += f"<br>From {start_date.strftime('%d-%b-%Y')} to {end_date.strftime('%d-%b-%Y')}"
    elif start_date:
        title_text += f"<br>From {start_date.strftime('%d-%b-%Y')} onwards"
    elif end_date:
        title_text += f"<br>Up to {end_date.strftime('%d-%b-%Y')}"
    
    fig.update_layout(
        title=title_text,
        xaxis_title="Date",
        yaxis_title="Number of Messages",
        xaxis_rangeslider_visible=True, 
        hovermode="x unified"
    )
    fig.show(renderer="browser")

# --- (Plot 2) Plot Author Graph ---
def plot_author_graph(author_counts):
    if not author_counts:
        print("No author data found to plot.")
        return
    print("Generating interactive 'Messages per Person' plot...")

    sorted_authors = sorted(author_counts.items(), key=lambda item: item[1], reverse=True)
    authors, counts = zip(*sorted_authors)

    fig = go.Figure(data=[go.Bar(x=authors, y=counts, text=counts, textposition='outside')])
    fig.update_layout(
        title="Total Messages per Person",
        xaxis_title="Author",
        yaxis_title="Number of Messages",
        hovermode="x unified"
    )
    fig.show(renderer="browser")

# --- (Plot 3) Plot Daily Author Graph ---
def plot_daily_author_graph(daily_author_counts, start_date=None, end_date=None):
    """
    Plots a grouped bar chart of messages per person, per day.
    """
    if not daily_author_counts:
        print("No daily author data found to plot.")
        return
    print("Generating interactive 'Messages per Person per Day' plot...")

    # 1. Get all unique, sorted dates
    all_dates = sorted(daily_author_counts.keys())
    
    # 2. Get all unique authors
    all_authors = set()
    for date_counts in daily_author_counts.values():
        all_authors.update(date_counts.keys())
    all_authors = sorted(list(all_authors))

    # 3. Create one bar trace for each author
    fig = go.Figure()
    
    for author in all_authors:
        counts_for_this_author = []
        for date in all_dates:
            # Get count for this author on this day, default to 0
            count = daily_author_counts[date].get(author, 0)
            counts_for_this_author.append(count)
        
        fig.add_trace(go.Bar(
            x=all_dates,
            y=counts_for_this_author,
            name=author
        ))

    # --- Customize Layout ---
    title_text = "Daily Messages per Person"
    if start_date and end_date:
        title_text += f"<br>From {start_date.strftime('%d-%b-%Y')} to {end_date.strftime('%d-%b-%Y')}"
    elif start_date:
        title_text += f"<br>From {start_date.strftime('%d-%b-%Y')} onwards"
    elif end_date:
        title_text += f"<br>Up to {end_date.strftime('%d-%b-%Y')}"
    
    fig.update_layout(
        title=title_text,
        xaxis_title="Date",
        yaxis_title="Number of Messages",
        barmode='group',  # This is the key: creates grouped bars
        xaxis_rangeslider_visible=True,
        hovermode="x unified" # Shows all authors for the hovered date
    )
    
    print("Displaying plot in your web browser...")
    fig.show(renderer="browser")

