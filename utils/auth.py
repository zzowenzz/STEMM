import pandas as pd
import bcrypt
import os

# Path to the user data CSV
USER_DATA_PATH = "./data/users.csv"

# Helper function to load user data
def load_user_data():
    if os.path.exists(USER_DATA_PATH):
        return pd.read_csv(USER_DATA_PATH)
    else:
        return pd.DataFrame(columns=["email", "password_hash"])

# Helper function to save user data
def save_user_data(df):
    df.to_csv(USER_DATA_PATH, index=False)

# Function to sign up a new user
def signup(email, password):
    users_df = load_user_data()
    
    # Check if email is already registered
    if email in users_df["email"].values:
        return False, "This email is already registered."
    
    # Hash the password
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    
    # Add the new user
    new_user = pd.DataFrame({"email": [email], "password_hash": [password_hash]})
    users_df = pd.concat([users_df, new_user], ignore_index=True)
    
    # Save the updated user data
    save_user_data(users_df)
    return True, "Signup successful!"

# Function to authenticate user login
def login(email, password):
    users_df = load_user_data()
    
    # Check if the email exists
    if email not in users_df["email"].values:
        return False, "This email is not registered."
    
    # Retrieve the stored password hash
    password_hash = users_df.loc[users_df["email"] == email, "password_hash"].values[0]
    
    # Compare the provided password with the stored hash
    if bcrypt.checkpw(password.encode(), password_hash.encode()):
        return True, "Login successful!"
    else:
        return False, "Incorrect password."
