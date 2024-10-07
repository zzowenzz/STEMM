import streamlit as st
from scripts.auth import register_user, login_user
from scripts.competition import show_competition_rules, show_reference_images, show_multiple_quizzes
from scripts.leaderboard import show_leaderboard

# Initialize session state for user login and navigation
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['email'] = ""
    st.session_state['page'] = "home"  # Default to home page

# Top Navigation Bar
def show_top_navbar():
    # Create a navigation bar with three columns for the buttons
    nav_col = st.columns([1, 1, 1])  # Allocate equal space for each button

    with nav_col[0]:
        if st.button("Home", key="home_btn", use_container_width=True):
            st.session_state['page'] = "home"

    with nav_col[1]:
        if st.button("Competition", key="compete_btn", use_container_width=True):
            st.session_state['page'] = "competition"

    with nav_col[2]:
        if st.button("Rank", key="rank_btn", use_container_width=True):
            st.session_state['page'] = "leaderboard"

# Display the navigation bar on top of every page
show_top_navbar()

# Function to display the home page
def show_home():
    st.write("## Welcome to our site")
    st.write("""
        This is a STEMM Experience Day on 17 October. This event will be at Nathan and Gold Coast, Griffith University.
        Our aim is to entice high school students and to use for future Open Days.
    """)
    st.write("""
        Come and compete against AI on koala face recognition! Guess who will win? You will also learn how the AI system works, when it is connected to hundreds of cameras to monitor and analyse koala road crossing behaviour, and to reduce koala vehicle strikes.
    """)

    st.write("### Login or Signup")
    option = st.selectbox("Login or Signup", ["Login", "Signup"])

    if option == "Signup":
        email = st.text_input("Email", "")
        password = st.text_input("Password", type="password")
        if st.button("Signup"):
            success, message = register_user(email, password)
            st.write(message)
            if success:
                st.session_state['logged_in'] = True
                st.session_state['email'] = email
                st.session_state['page'] = "competition"  # Redirect to competition page after signup

    elif option == "Login":
        email = st.text_input("Email", "")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            success, message = login_user(email, password)
            st.write(message)
            if success:
                st.session_state['logged_in'] = True
                st.session_state['email'] = email
                st.session_state['page'] = "competition"  # Redirect to competition page after login

# Handle user navigation and authentication
if st.session_state['logged_in']:
    st.success(f"Logged in as {st.session_state['email']}")

    if st.session_state['page'] == "home":
        show_home()

    elif st.session_state['page'] == "competition":
        show_competition_rules()
        show_reference_images()
        show_multiple_quizzes(num_quizzes=3, user_email=st.session_state['email'])

    elif st.session_state['page'] == "leaderboard":
        show_leaderboard()

    if st.button("Logout"):
        st.session_state['logged_in'] = False
        st.session_state['email'] = ""
        st.session_state['page'] = "home"
        st.success("You have been logged out.")
else:
    if st.session_state['page'] == "home":
        show_home()
    elif st.session_state['page'] == "competition" or st.session_state['page'] == "leaderboard":
        st.warning("You need to be logged in to access this page. Please login or sign up.")
        show_home()
