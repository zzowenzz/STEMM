import streamlit as st
from scripts.auth import register_user, login_user, logout
from scripts.competition import show_competition_rules, show_reference_images, show_multiple_quizzes

# Initialize session state to track if the user is logged in and for navigation
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['email'] = ""
    st.session_state['page'] = "home"  # Default to home page

# Handle user authentication (login, signup)
if not st.session_state['logged_in']:
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

    elif option == "Login":
        email = st.text_input("Email", "")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            success, message = login_user(email, password)
            st.write(message)
            if success:
                st.session_state['logged_in'] = True
                st.session_state['email'] = email

# Main content when logged in
if st.session_state['logged_in']:
    st.success(f"Logged in as {st.session_state['email']}")
    
    # Only show the "Start to compete" button on the home page
    if st.session_state['page'] == "home":
        if st.button("Start to compete"):
            st.session_state['page'] = "competition"  # Switch to competition page

    # Show competition content if user clicked "Start to compete"
    if st.session_state['page'] == "competition":
        show_competition_rules()
        show_reference_images()  # Show the reference images
        show_multiple_quizzes(num_quizzes=3)  # Show multiple quizzes

    # Show the Logout button all the time while logged in
    if st.button("Logout"):
        st.session_state['logged_in'] = False
        st.session_state['email'] = ""
        st.session_state['page'] = "home"
        st.success("You have been logged out.")
