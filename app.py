import streamlit as st
from utils.auth import signup, login

# Streamlit app for common signup/login page
def main():
    st.title("Koala Recognition Competition")
    
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
                    st.success(message)
                    st.session_state["logged_in"] = True
                    st.session_state["user_email"] = email
                else:
                    st.error(message)
            else:
                st.error("Please enter both email and password.")
    
    # If logged in, display a welcome message and competition link
    if st.session_state.get("logged_in"):
        st.write(f"Welcome, {st.session_state['user_email']}!")
        st.write("[Start the competition](competition.py)")

if __name__ == "__main__":
    main()
