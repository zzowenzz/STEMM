import streamlit as st
from scripts.images import get_reference_images, get_quiz_image, get_koala_classes, resize_image
from scripts.leaderboard import update_leaderboard
import random
import os

# Function to show competition rules
def show_competition_rules():
    st.write("""
        Welcome to the Koala Individual Recognition Competition!
        
        **Competition Rules**:
        - You will be shown images of koalas.
        - First, you'll see some reference images of koalas, which will help you identify them.
        - Then, you'll be asked to identify koalas in unseen images.
        - Select the correct koala from multiple choices. Your score will depend on your accuracy.
        - You can compete as many times as you like, and the leaderboard will record your highest score!
    """)

# Function to show reference images
def show_reference_images():
    koala_classes = get_koala_classes()
    st.write("### Reference Images")

    # Loop over each koala class and display them in their own row
    for koala_class in koala_classes:
        # Display the koala class name, centered
        st.markdown(f"""
            <div style='text-align: center; font-size:18px; font-weight:bold;'>
                {koala_class}
            </div>
        """, unsafe_allow_html=True)

        reference_images = get_reference_images(koala_class)

        # Create a row for the reference images of this class
        image_columns = st.columns(len(reference_images))  # Create a column for each reference image

        # Display each reference image in the row
        for idx, img_path in enumerate(reference_images):
            img = resize_image(img_path, size=(200, 200))  # Resize the image to 200x200
            with image_columns[idx]:
                # st.write(os.path.basename(img_path).split('.')[0])  # Show image name on top (without extension)
                st.image(img, width=150)  # Display the resized image with explicit width (200 pixels)

# Function to show a single quiz
def show_quiz(quiz_index):
    # Initialize session state for the quiz if not already set
    if f"quiz_{quiz_index}_initialized" not in st.session_state:
        # Pick a random koala class for the correct answer
        correct_koala_class = random.choice(get_koala_classes())
        # Get an unseen image from the correct class
        quiz_image = get_quiz_image(correct_koala_class)
        # Select 3 incorrect options (other koala classes)
        false_koala_classes = random.sample(
            [cls for cls in get_koala_classes() if cls != correct_koala_class], 3
        )
        # Combine correct and false answers, then shuffle the choices
        choices = false_koala_classes + [correct_koala_class]
        random.shuffle(choices)

        # Store everything in session state
        st.session_state[f"quiz_{quiz_index}_initialized"] = True
        st.session_state[f"quiz_{quiz_index}_image"] = quiz_image
        st.session_state[f"quiz_{quiz_index}_correct"] = correct_koala_class
        st.session_state[f"quiz_{quiz_index}_choices"] = choices

    # Retrieve the stored state
    quiz_image = st.session_state[f"quiz_{quiz_index}_image"]
    correct_koala_class = st.session_state[f"quiz_{quiz_index}_correct"]
    choices = st.session_state[f"quiz_{quiz_index}_choices"]

    # Display the quiz
    st.write(f"### Quiz {quiz_index + 1}: Identify the Koala")
    st.write("Select the correct koala for the image below:")

    # Show the quiz image
    img = resize_image(quiz_image, size=(200, 200))
    st.image(img, width=400)

    # Display the radio buttons
    selected_koala = st.radio(f"Which koala is this?", choices, key=f"radio_{quiz_index}")

    # Check if the quiz has already been submitted
    if f"submitted_{quiz_index}" not in st.session_state:
        st.session_state[f"submitted_{quiz_index}"] = False

    # Display the submit button only if the quiz has not been submitted
    if not st.session_state[f"submitted_{quiz_index}"]:
        if st.button("Submit Answer", key=f"submit_{quiz_index}"):
            # Mark the quiz as submitted
            st.session_state[f"submitted_{quiz_index}"] = True

            # Initialize the score if not done yet
            if 'score' not in st.session_state:
                st.session_state['score'] = 0

            # Check if the user's answer is correct
            if selected_koala == correct_koala_class:
                st.success(f"Correct! This is {correct_koala_class}.")
                st.session_state['score'] += 1  # Increase score by 1
            else:
                st.error(f"Wrong! This was {correct_koala_class}.")
                # Decrease score by 1 if it's greater than 0
                if st.session_state['score'] > 0:
                    st.session_state['score'] -= 1


# Function to show multiple quizzes and track the score
def show_multiple_quizzes(num_quizzes=3, user_email="user@example.com"):
    st.write(f"## You will be shown {num_quizzes} quizzes")

    for i in range(num_quizzes):
        show_quiz(quiz_index=i)

    # Show the final score after all quizzes are submitted
    if all(st.session_state.get(f"submitted_{i}", False) for i in range(num_quizzes)):
        st.write(f"## Your final score is: {st.session_state['score']}")

        # Update the leaderboard with the user's email and final score
        update_leaderboard(user_email, st.session_state['score'])

