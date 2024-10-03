import streamlit as st
from scripts.images import get_reference_images, get_quiz_image, get_koala_classes
import random

def show_competition_rules():
    st.write("""
        Welcome to the Koala Individual Recognition Competition!
        
        **Competition Rules**:
        - You will be shown images of koalas.
        - First, you'll see some reference images of 5 koalas, which will help you identify them.
        - Then, you'll be asked to identify koalas in unseen images.
        - Select the correct koala from multiple choices. Your score will depend on your accuracy.
        - You can compete as many times as you like, and the leaderboard will record your highest score!
    """)

def show_reference_images():
    koala_classes = get_koala_classes()
    st.write("### Reference Images")
    columns = st.columns(len(koala_classes))
    for idx, koala_class in enumerate(koala_classes):
        with columns[idx]:
            st.write(f"**{koala_class}**")
            reference_images = get_reference_images(koala_class)
            for img_path in reference_images:
                st.image(img_path, use_column_width=True, caption=f"{koala_class} Reference")

def show_quiz():
    koala_classes = get_koala_classes()
    st.write("### Quiz: Identify the Koala")
    st.write("Select the correct koala for the image below:")

    # Get a random unseen image from one of the koala classes
    quiz_koala_class = random.choice(koala_classes)
    quiz_image = get_quiz_image(quiz_koala_class)
    st.image(quiz_image, caption="Unseen Koala", use_column_width=True)

    # Create multiple-choice options for the quiz
    selected_koala = st.radio("Which koala is this?", koala_classes)

    if st.button("Submit Answer"):
        if selected_koala == quiz_koala_class:
            st.success(f"Correct! This is {quiz_koala_class}.")
        else:
            st.error(f"Wrong! This was {quiz_koala_class}.")
