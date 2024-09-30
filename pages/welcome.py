import streamlit as st

# Welcome page that user is redirected to after login
def main():
    st.title("Welcome to the Koala Recognition Competition")
    
    # Check if user is logged in
    if not st.session_state.get("logged_in"):
        st.error("You need to log in to access this page.")
        st.stop()
    
    # Display welcome message
    user_email = st.session_state.get("user_email", "")
    st.write(f"Welcome, {user_email}!")

    # Button to start the competition
    if st.button("Start Competition"):
        st.write("Competition starting soon...")  # Placeholder action
        # You can redirect to the competition page here if needed
        # st.experimental_rerun() or other logic to navigate

if __name__ == "__main__":
    main()
