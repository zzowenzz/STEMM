from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, select
import pandas as pd
import streamlit as st
import os

# Set up the database connection using Streamlit secrets
DATABASE_URL = os.environ.get("DATABASE_URL")
engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Define the leaderboard table structure
leaderboard_table = Table(
    'leaderboard', metadata,
    Column('id', Integer, primary_key=True),
    Column('email', String, unique=True),
    Column('attempts', Integer, default=0),
    Column('highest_score', Integer, default=0)
)

# Function to load the leaderboard from the database
def load_leaderboard():
    with engine.connect() as connection:
        result = connection.execute(select([leaderboard_table]))
        # Convert result to a Pandas DataFrame
        leaderboard_df = pd.DataFrame(result.fetchall(), columns=['id', 'email', 'attempts', 'highest_score'])
        leaderboard_df.drop(columns=['id'], inplace=True)  # Drop the ID column as it's not needed
    return leaderboard_df

# Function to update the leaderboard in the database
def update_leaderboard(email, score):
    with engine.connect() as connection:
        # Check if the user already exists in the leaderboard
        existing_user = connection.execute(
            select([leaderboard_table]).where(leaderboard_table.c.email == email)
        ).fetchone()

        if existing_user:
            # Update the existing user record
            attempts = existing_user['attempts'] + 1
            highest_score = max(existing_user['highest_score'], score)

            connection.execute(
                leaderboard_table.update()
                .where(leaderboard_table.c.email == email)
                .values(attempts=attempts, highest_score=highest_score)
            )
        else:
            # Add a new user to the leaderboard
            connection.execute(
                leaderboard_table.insert().values(email=email, attempts=1, highest_score=score)
            )

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
