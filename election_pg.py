import pandas as pd
import tkinter as tk
import seaborn as sns
from tkinter import messagebox, PhotoImage
from tkinter import ttk
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Load the dataset
df = pd.read_csv('election_results_2024 (2).csv')
df['Margin'] = pd.to_numeric(df['Margin'], errors='coerce')


# Function to show winning and trailing candidates with margin
def show_candidates():
    constituency = constituency_entry.get()
    if constituency:
        constituency_data = df[df['Constituency'] == constituency]
        if not constituency_data.empty:
            leading_candidate = constituency_data['Leading Candidate'].values[0]
            trailing_candidate = constituency_data['Trailing Candidate'].values[0]
            margin = constituency_data['Margin'].values[0]
            leading_party = constituency_data['Leading Party'].values[0]
            trailing_party = constituency_data['Trailing Party'].values[0]
            result = (f"Leading Candidate: {leading_candidate} (Party: {leading_party})\n"
                      f"Trailing Candidate: {trailing_candidate} (Party: {trailing_party})\n"
                      f"Margin: {int(margin)} votes")
            messagebox.showinfo("Candidates Result", result)
        else:
            messagebox.showwarning("No Results", f"No data found for the constituency {constituency}.")
    else:
        messagebox.showwarning("Input Error", "Please enter a constituency name.")

# Function to show winning constituencies by party in tabular form
def show_winning_constituencies():
    party_name = party_entry.get()
    if party_name:
        winning_constituencies = df[df['Leading Party'] == party_name][['Constituency', 'Leading Candidate','Margin']]
        if not winning_constituencies.empty:
            win_table = tk.Toplevel(root)
            win_table.title(f"Winning Constituencies for {party_name}")
            cols = ('Constituency', 'Leading Candidate' , 'Margin')
            tree = ttk.Treeview(win_table, columns=cols, show='headings')
            for col in cols:
                tree.heading(col, text=col)
            for index, row in winning_constituencies.iterrows():
                tree.insert("", "end", values=list(row))
            tree.pack(pady=10)
        else:
            messagebox.showwarning("No Results", f"No winning constituencies found for the party {party_name}.")
    else:
        messagebox.showwarning("Input Error", "Please enter a party name.")

# Function to show pie chart of constituencies won by each party
def show_pie_chart():
    party_counts = df['Leading Party'].value_counts()
    plt.figure(figsize=(10, 7))
    plt.pie(party_counts, autopct=lambda p: f'{int(p * sum(party_counts) / 100)}', startangle=140)
    plt.legend(title="Parties", loc="upper left", labels=[f"{party} ({count} seats)" for party, count in party_counts.items()])
    plt.title('Total Number of Constituencies Won by Each Party')
    plt.axis('equal')
    plt.show()


def plot_votes_for_candidates():
    
    rahul_entries = df[df['Leading Candidate'] == 'RAHUL GANDHI']
    modi_entries = df[df['Leading Candidate'] == 'NARENDRA MODI']
    amit_entries = df[df['Leading Candidate'] == 'AMIT SHAH']
    tejasvi_entries = df[df['Leading Candidate'] == 'TEJASVI SURYA']

    # Get the votes for Rahul Gandhi, Narendra Modi, and Amit Shah
    rahul_votes = rahul_entries['Margin'].values
    modi_votes = modi_entries['Margin'].values[0] if not modi_entries.empty else 0
    tejasvi_votes = tejasvi_entries['Margin'].values[0] if not tejasvi_entries.empty else 0
    amit_votes = amit_entries['Margin'].values[0] if not amit_entries.empty else 0

    # Get the original constituency names for Rahul Gandhi
    rahul_constituencies = list(rahul_entries['Constituency'])

    # Get the original constituency name for Narendra Modi
    modi_constituency = modi_entries['Constituency'].values[0] if not modi_entries.empty else "Modi Constituency"

    # Get the original constituency name for Amit Shah
    amit_constituency = amit_entries['Constituency'].values[0] if not amit_entries.empty else "Amit Shah Constituency"

    # Get the original constituency name for tejasvi_surya
    tejasvi_constituency = tejasvi_entries['Constituency'].values[0] if not amit_entries.empty else "Tejasvi Surya Constituency"

    # Combine the data
    data_to_plot = pd.DataFrame({
        'Candidate': ['Rahul Gandhi'] * len(rahul_votes) + ['Narendra Modi', 'Amit Shah', 'Tejasvi Surya'],
        'Constituency': rahul_constituencies + [modi_constituency, amit_constituency, tejasvi_constituency],
        'Votes': list(rahul_votes) + [modi_votes, amit_votes, tejasvi_votes]
    })

    # Plot the comparison
    plt.figure(figsize=(12, 6))
    sns.barplot(data=data_to_plot, x='Constituency', y='Votes', hue='Candidate', palette='muted')
    plt.title('Comparison of Votes for Rahul Gandhi, Narendra Modi, Amit Shah and Tejasvi Surya')
    plt.xlabel('Constituency')
    plt.ylabel('Votes')
    plt.xticks(rotation=45)
    plt.subplots_adjust(bottom=0.3)
    plt.show()






def plot_margin_comparison():
    df['Margin'] = pd.to_numeric(df['Margin'], errors='coerce')
    highest_margin = df.nlargest(1, 'Margin')
    lowest_margin = df.nsmallest(1, 'Margin')
    margin_data = pd.concat([highest_margin, lowest_margin])
    plt.figure(figsize=(10, 6))
    plt.bar(margin_data['Leading Candidate'], margin_data['Margin'], color=['orange', 'blue'])
    for index, row in margin_data.iterrows():
        plt.text(index, row['Margin'], row['Leading Party'], ha='center', va='bottom')
    plt.xlabel('Candidates with Highest and Lowest Margin of Victory')
    plt.ylabel('Margin of Victory (Votes)')
    plt.title('Comparison of Highest and Lowest Margin of Victory')
    plt.ylim(0, margin_data['Margin'].max() + 10000)  # Add some space above the highest bar
    plt.yticks(range(0, int(margin_data['Margin'].max()) + 200000, 100000))  # Set y-axis ticks in steps of 10000
    plt.legend()
    plt.show()

    # Function to plot top 10 trailing parties by votes
def plot_top_trailing_parties():
    
    trailing_party_votes = df.groupby('Trailing Party')['Margin'].sum().sort_values(ascending=False)
    trailing_party_seats = df['Trailing Party'].value_counts()
    plt.figure(figsize=(12, 8))
    plt.subplot(1, 2, 2)
    sns.barplot(x=trailing_party_seats.index[:10], y=trailing_party_seats.values[:10], palette='viridis')
    plt.title('Top 10 Trailing Parties by Seats')
    plt.xlabel('Party')
    plt.ylabel('Number of Seats')
    plt.xticks(rotation=90)
    plt.subplots_adjust(left=-0.5,right=0.85,top=0.9,bottom=0.6)
    plt.show()

def plot_top_trailing_parties_by_vote():
    trailing_party_votes = df.groupby('Trailing Party')['Margin'].sum().sort_values(ascending=False)
    plt.figure(figsize=(30, 12))

    # Plot votes distribution by trailing party
    plt.subplot(1, 2, 1)
    sns.barplot(x=trailing_party_votes.index[:10], y=trailing_party_votes.values[:10], palette='viridis')
    plt.title('Top 10 Trailing Parties by Votes')
    plt.xlabel('Party')
    plt.ylabel('Total Votes')
    plt.xticks(rotation=90)
    plt.subplots_adjust(right=1.75,bottom=0.4)
    plt.show()

def party_seat_won():
    party_votes = df.groupby('Leading Party')['Margin'].sum().sort_values(ascending=False)
    df['Margin'] = pd.to_numeric(df['Margin'], errors='coerce')

    # Party with highest and lowest margin of victory
    highest_margin = df.loc[df['Margin'].idxmax()]
    lowest_margin = df.loc[df['Margin'].idxmin()]
    leading_party_highest_votes = party_votes.idxmax()
    leading_party_lowest_votes = party_votes.idxmin()

    # Number of seats won by each party
    seats_won = df['Leading Party'].value_counts()

    # Plot number of seats won by each party
    plt.figure(figsize=(20, 8))
    sns.barplot(x=seats_won.index, y=seats_won.values, palette='viridis')
    plt.title('Number of Seats Won by Each Party')
    plt.xlabel('Party')
    plt.ylabel('Seats Won')
    plt.xticks(rotation=270)
    plt.subplots_adjust(bottom=0.5)
    plt.show()
    


# GUI setup
root = tk.Tk()
root.title("Election Data Analysis")


# Load the background image
bg_image = PhotoImage(file="mapimage (1).png")

# Create a Canvas widget to place the image
canvas = tk.Canvas(root, width=1920, height=1080)
canvas.pack()

# Display the background image
canvas.create_image(0, 0, anchor=tk.NW, image=bg_image)


constituency_label = tk.Label(root, text="Enter Constituency:", bg='lightpink',width=30)
constituency_label.place(x=99,y=58)
constituency_entry = tk.Entry(root,width=36)
constituency_entry.place(x=99,y=88)
constituency_button = tk.Button(root, text="Show Candidates", bg='lightblue',width=30, command = show_candidates)
constituency_button.place(x=99,y=115)



party_label = tk.Label(root, text="Enter Party Name:",width=30)
party_label.place(x=99,y=180)
party_entry = tk.Entry(root,width=36)
party_entry.place(x=99,y=210)
party_button = tk.Button(root, text="Show Winning Constituencies", bg='yellow' ,width=30, command=show_winning_constituencies)
party_button.place(x=99,y=235)

party_chart_button = tk.Button(root, text="Number of Seats Won by Each Party",bg='lime' , width=30,command=party_seat_won)
party_chart_button.place(x=99,y=280)

pie_chart_button = tk.Button(root, text="Show Constituency Percentage Pie Chart",bg='silver' , width=30,command=show_pie_chart)
pie_chart_button.place(x=99,y=320)

votes_button = tk.Button(root, text="Plot Votes for Specific Candidates",bg='gold', width=30,command=plot_votes_for_candidates)
votes_button.place(x=99,y=360)

margin_button = tk.Button(root, text="Plot Margin Comparison", bg='lightgreen' , width=30,command=plot_margin_comparison)
margin_button.place(x=99,y=400)

trailing_button = tk.Button(root, text="Plot Top 10 Trailing Parties", width=30,command=plot_top_trailing_parties)
trailing_button.place(x=99,y=440)

votes_trailing_button = tk.Button(root, text="Plot Top 10 Trailing Parties by votes", fg= 'white' , bg= "blue",width=30,command=plot_top_trailing_parties_by_vote)
votes_trailing_button.place(x=99,y=480)

root.mainloop()
