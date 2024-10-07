import pandas as pd
import streamlit as st
import os

LEADERBOARD_FILE = './data/leaderboard.csv'

# Function to load the leaderboard from a CSV file
def load_leaderboard():
    if os.path.exists(LEADERBOARD_FILE):
        return pd.read_csv(LEADERBOARD_FILE)
    else:
        # If the leaderboard doesn't exist, return an empty dataframe
        return pd.DataFrame(columns=['email', 'attempts', 'highest_score'])

# Function to save the leaderboard back to the CSV file
def save_leaderboard(leaderboard_df):
    leaderboard_df.to_csv(LEADERBOARD_FILE, index=False)

# Function to update the leaderboard after each competition
def update_leaderboard(email, score):
    leaderboard_df = load_leaderboard()

    # Check if the user already exists in the leaderboard
    if email in leaderboard_df['email'].values:
        # Update existing user record
        user_row = leaderboard_df[leaderboard_df['email'] == email].iloc[0]
        leaderboard_df.loc[leaderboard_df['email'] == email, 'attempts'] += 1
        if score > user_row['highest_score']:
            leaderboard_df.loc[leaderboard_df['email'] == email, 'highest_score'] = score
    else:
        # Add a new user to the leaderboard
        new_user = pd.DataFrame({
            'email': [email],
            'attempts': [1],
            'highest_score': [score]
        })
        leaderboard_df = pd.concat([leaderboard_df, new_user], ignore_index=True)

    # Save the updated leaderboard
    save_leaderboard(leaderboard_df)

# Function to display the leaderboard
def show_leaderboard():
    leaderboard_df = load_leaderboard()

    if leaderboard_df.empty:
        st.write("No users have competed yet.")
    else:
        # Sort the leaderboard by highest score in descending order
        leaderboard_df = leaderboard_df.sort_values(by='highest_score', ascending=False)

        # Display the leaderboard table
        st.write("### Leaderboard")
        st.write(leaderboard_df.rename(columns={
            'email': 'Username',
            'attempts': 'Number of Trials',
            'highest_score': 'Highest Score'
        }))
