import pandas as pd
import tkinter as tk
from tkinter import messagebox

# Load the dataset
df = pd.read_csv('election_results_2024 (1).csv')

# Function to get constituencies won by a party
def get_constituencies_by_party(party_name):
    won_constituencies = df[df['Leading Party'] == party_name]['Constituency'].tolist()
    return won_constituencies

# Function to compare candidates
def compare_candidates(candidate1, candidate2):
    c1_data = df[df['Leading Candidate'] == candidate1]
    c2_data = df[df['Leading Candidate'] == candidate2]
    return c1_data, c2_data

# Function to get the constituency with the highest voting percentage
def highest_voting_percentage():
    highest_percentage = df['Voting Percentage'].max()
    constituency = df[df['Voting Percentage'] == highest_percentage]['Constituency'].values[0]
    return constituency, highest_percentage

# Function to get parties fighting in a given constituency
def get_parties_by_constituency(constituency):
    parties = df[df['Constituency'] == constituency]['Leading Party'].unique().tolist()
    return parties

# GUI functions
def show_constituencies():
    party_name = party_entry.get()
    if party_name:
        constituencies = get_constituencies_by_party(party_name)
        if constituencies:
            messagebox.showinfo("Constituencies", f"Constituencies won by {party_name}: {', '.join(constituencies)}")
        else:
            messagebox.showwarning("No Results", f"No constituencies found for the party {party_name}.")
    else:
        messagebox.showwarning("Input Error", "Please enter a party name.")

def show_comparison():
    candidate1 = candidate1_entry.get()
    candidate2 = candidate2_entry.get()
    if candidate1 and candidate2:
        c1_data, c2_data = compare_candidates(candidate1, candidate2)
        if not c1_data.empty and not c2_data.empty:
            comparison_result = f"{candidate1}:\n{c1_data.to_string(index=False)}\n\n{candidate2}:\n{c2_data.to_string(index=False)}"
            messagebox.showinfo("Comparison", comparison_result)
        else:
            messagebox.showwarning("No Results", "One or both candidates not found in the dataset.")
    else:
        messagebox.showwarning("Input Error", "Please enter both candidate names.")

def show_highest_voting_percentage():
    constituency, percentage = highest_voting_percentage()
    messagebox.showinfo("Highest Voting Percentage", f"Constituency with highest voting percentage: {constituency} ({percentage}%)")

def show_parties():
    constituency = constituency_entry.get()
    if constituency:
        parties = get_parties_by_constituency(constituency)
        if parties:
            messagebox.showinfo("Parties", f"Parties fighting in {constituency}: {', '.join(parties)}")
        else:
            messagebox.showwarning("No Results", f"No parties found for the constituency {constituency}.")
    else:
        messagebox.showwarning("Input Error", "Please enter a constituency name.")

# GUI setup
root = tk.Tk()
root.title("Election Data Analysis")

party_label = tk.Label(root, text="Enter Party Name:")
party_label.pack()
party_entry = tk.Entry(root)
party_entry.pack()
party_button = tk.Button(root, text="Show Constituencies", command=show_constituencies)
party_button.pack()

candidate1_label = tk.Label(root, text="Enter Candidate 1:")
candidate1_label.pack()
candidate1_entry = tk.Entry(root)
candidate1_entry.pack()
candidate2_label = tk.Label(root, text="Enter Candidate 2:")
candidate2_label.pack()
candidate2_entry = tk.Entry(root)
candidate2_entry.pack()
comparison_button = tk.Button(root, text="Compare Candidates", command=show_comparison)
comparison_button.pack()

highest_voting_button = tk.Button(root, text="Highest Voting Percentage", command=show_highest_voting_percentage)
highest_voting_button.pack()

constituency_label = tk.Label(root, text="Enter Constituency:")
constituency_label.pack()
constituency_entry = tk.Entry(root)
constituency_entry.pack()
parties_button = tk.Button(root, text="Show Parties", command=show_parties)
parties_button.pack()

root.mainloop()
