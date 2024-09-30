import streamlit as st
from utils.auth import signup, login

# Initialize session state variables if they don't exist
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "user_email" not in st.session_state:
    st.session_state["user_email"] = ""

# Main application
def main():
    st.title("Koala Recognition Competition")

    # Check query params to automatically show the welcome page if logged in
    query_params = st.query_params
    if "logged_in" in query_params and query_params["logged_in"] == ["True"]:
        st.session_state["logged_in"] = True

    # If the user is logged in, show only the welcome page
    if st.session_state["logged_in"]:
        show_welcome_page()
    else:
        show_login_signup_form()

# Function to display the login/signup form if the user is not logged in
def show_login_signup_form():
    # Show login or signup form
    option = st.selectbox("Choose action", ["Login", "Sign Up"])
    
    if option == "Sign Up":
        st.subheader("Create a new account")
        email = st.text_input("Email", value="", placeholder="Enter your email")
        password = st.text_input("Password", value="", placeholder="Enter a strong password", type="password")
        
        if st.button("Sign Up"):
            if email and password:
                success, message = signup(email, password)
                if success:
                    st.success(message)
                else:
                    st.error(message)
            else:
                st.error("Please enter both email and password.")
    
    elif option == "Login":
        st.subheader("Login to your account")
        email = st.text_input("Email", value="", placeholder="Enter your email")
        password = st.text_input("Password", value="", placeholder="Enter your password", type="password")
        
        if st.button("Login"):
            if email and password:
                success, message = login(email, password)
                if success:
                    # Set session state to indicate the user is logged in
                    st.session_state["logged_in"] = True
                    st.session_state["user_email"] = email
                    # Redirect using query params to reflect login state
                    st.query_params = {"logged_in": "True"}
                else:
                    st.error(message)
            else:
                st.error("Please enter both email and password.")

# Function to display the welcome page after login
def show_welcome_page():
    st.title("Welcome to the Koala Recognition Competition!")
    st.write(f"Hello, {st.session_state['user_email']}! Glad to have you here.")
    
    # Button to start the competition
    if st.button("Start Competition"):
        st.write("Competition page content goes here.")  # Placeholder for competition logic

    # Log out option
    if st.button("Log Out"):
        st.session_state["logged_in"] = False
        st.session_state["user_email"] = ""
        st.query_params = {}  # Clear query params on logout

if __name__ == "__main__":
    main()
