import bcrypt
import pandas as pd
import os

# Path to user data
USER_DATA_PATH = './data/users.csv'

# Load users.csv or create an empty DataFrame
def load_user_data():
    if os.path.exists(USER_DATA_PATH):
        return pd.read_csv(USER_DATA_PATH)
    else:
        return pd.DataFrame(columns=["email", "hashed_password"])

# Save the user data back to CSV
def save_user_data(user_df):
    user_df.to_csv(USER_DATA_PATH, index=False)

# Hash password using bcrypt
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed

# Verify password
def verify_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

# Register a new user
def register_user(email, password):
    user_df = load_user_data()

    # Check if the email already exists
    if email in user_df['email'].values:
        return False, "User already exists."

    # Hash the password and store the user
    hashed_password = hash_password(password).decode('utf-8')
    new_user = pd.DataFrame([[email, hashed_password]], columns=["email", "hashed_password"])
    user_df = pd.concat([user_df, new_user], ignore_index=True)
    
    save_user_data(user_df)
    return True, "Registration successful."

# Login a user
def login_user(email, password):
    user_df = load_user_data()

    # Check if the user exists
    if email not in user_df['email'].values:
        return False, "User does not exist."

    # Get stored hashed password
    stored_hashed_password = user_df[user_df['email'] == email]['hashed_password'].values[0]

    # Verify password
    if verify_password(password, stored_hashed_password):
        return True, "Login successful."
    else:
        return False, "Incorrect password."
