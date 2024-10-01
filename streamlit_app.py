import streamlit as st
from scripts.auth import register_user, login_user
import random
import os

# Paths to images (update these paths based on your folder structure)
KOALA_IMAGE_PATH = './images/'
koala_classes = ["Koala_1", "Koala_2"]

# Example function to get images from a class folder
def get_reference_images(koala_class):
    images_path = os.path.join(KOALA_IMAGE_PATH, koala_class)
    return [os.path.join(images_path, img) for img in os.listdir(images_path) if 'reference' in img]

# Example function to get unseen quiz images
def get_quiz_image(koala_class):
    images_path = os.path.join(KOALA_IMAGE_PATH, koala_class)
    unseen_images = [img for img in os.listdir(images_path) if 'unseen' in img]
    return os.path.join(images_path, random.choice(unseen_images))

# Initialize session state to track if the user is logged in and for navigation
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['email'] = ""
    st.session_state['page'] = "home"  # Initialize page to home

# Function to log out the user and reset session state
def logout():
    st.session_state['logged_in'] = False
    st.session_state['email'] = ""
    st.session_state['page'] = "home"
    st.success("You have been logged out.")

# If the user is not logged in, show the login/signup forms
if not st.session_state['logged_in']:
    st.session_state['page'] = "home"  # Reset to home if logged out
    option = st.selectbox("Login or Signup", ["Login", "Signup"])

    if option == "Signup":
        st.subheader("Create a new account")
        email = st.text_input("Email", "")
        password = st.text_input("Password", type="password")
        if st.button("Signup"):
            success, message = register_user(email, password)
            st.write(message)
            if success:
                st.session_state['logged_in'] = True
                st.session_state['email'] = email

    elif option == "Login":
        st.subheader("Login to your account")
        email = st.text_input("Email", "")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            success, message = login_user(email, password)
            st.write(message)
            if success:
                st.session_state['logged_in'] = True
                st.session_state['email'] = email

# If the user is logged in and on the home page, show the "Start to compete" button and logout button
if st.session_state['logged_in'] and st.session_state['page'] == "home":
    st.success(f"Logged in as {st.session_state['email']}")
    
    # Show the "Start to compete" button
    if st.button("Start to compete", key="start_competition"):
        st.session_state['page'] = "competition"  # Switch to competition page

    # Show the "Logout" button
    if st.button("Logout", key="home_logout"):
        logout()  # Call the logout function to reset session state

# Competition page logic
if st.session_state['logged_in'] and st.session_state['page'] == "competition":
    st.subheader("Koala Recognition Competition")
    
    # Competition rules description
    st.write("""
        Welcome to the Koala Individual Recognition Competition!
        
        **Competition Rules**:
        - You will be shown images of koalas.
        - First, you'll see some reference images of 5 koalas, which will help you identify them.
        - Then, you'll be asked to identify koalas in unseen images.
        - Select the correct koala from multiple choices. Your score will depend on your accuracy.
        - You can compete as many times as you like, and the leaderboard will record your highest score!
    """)

    # Display reference images for each koala class, one class per column
    st.write("### Reference Images")
    columns = st.columns(len(koala_classes))
    for idx, koala_class in enumerate(koala_classes):
        with columns[idx]:
            st.write(f"**{koala_class}**")
            reference_images = get_reference_images(koala_class)
            for img_path in reference_images:
                st.image(img_path, use_column_width=True, caption=f"{koala_class} Reference")

    # Quiz section
    st.write("### Quiz: Identify the Koala")
    st.write("Select the correct koala for the image below:")

    # Get a random unseen image from one of the koala classes
    quiz_koala_class = random.choice(koala_classes)
    quiz_image = get_quiz_image(quiz_koala_class)
    st.image(quiz_image, caption="Unseen Koala", use_column_width=True)

    # Create multiple-choice options for the quiz
    options = koala_classes
    selected_koala = st.radio("Which koala is this?", options)

    if st.button("Submit Answer", key="submit_answer"):
        if selected_koala == quiz_koala_class:
            st.success(f"Correct! This is {quiz_koala_class}.")
            # Score can be calculated here and stored in leaderboard
        else:
            st.error(f"Wrong! This was {quiz_koala_class}. Better luck next time!")
        # Optionally, return to the home page or restart the competition
        if st.button("Try again", key="try_again"):
            st.session_state['page'] = "competition"

    # Add a button to return to the homepage
    if st.button("Return to Home", key="return_home"):
        st.session_state['page'] = "home"

    # Show the "Logout" button on the competition page too
    if st.button("Logout", key="competition_logout"):
        logout()  # Call the logout function to reset session state
