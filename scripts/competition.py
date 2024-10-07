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
    koala_classes = get_koala_classes()

    # Step 1: Pick a random koala class for the correct answer
    correct_koala_class = random.choice(koala_classes)
    quiz_image = get_quiz_image(correct_koala_class)  # Get unseen image from the correct class

    # Check if the user has already submitted this quiz
    if f"submitted_{quiz_index}" not in st.session_state:
        st.session_state[f"submitted_{quiz_index}"] = False

    # If the quiz is submitted, show the "Quiz is submitted" message
    if st.session_state[f"submitted_{quiz_index}"]:
        st.error(f"Quiz {quiz_index + 1} is submitted.")
    else:
        # Generate a quiz with 4 choices: 1 correct and 3 incorrect
        st.write(f"### Quiz {quiz_index + 1}: Identify the Koala")
        st.write("Select the correct koala for the image below:")

        # Step 2: Select 3 incorrect options (other koala classes)
        false_koala_classes = random.sample([cls for cls in koala_classes if cls != correct_koala_class], 3)

        # Step 3: Combine correct and false answers, then shuffle the choices
        choices = false_koala_classes + [correct_koala_class]  # Include the correct answer
        random.shuffle(choices)  # Shuffle the choices to randomize the position of the correct answer

        # Step 4: Show the quiz image and options
        img = resize_image(quiz_image, size=(200, 200))  # Resize the quiz image
        st.image(img, width=400)

        # Show the radio buttons for the user to select an option
        selected_koala = st.radio(f"Which koala is this?", choices, key=f"radio_{quiz_index}")

        # Step 5: Handle the submission and scoring
        if st.button("Submit Answer", key=f"submit_{quiz_index}"):
            # Mark the quiz as submitted
            st.session_state[f"submitted_{quiz_index}"] = True

            # Initialize score if not already done
            if 'score' not in st.session_state:
                st.session_state['score'] = 0

            # Check if the answer is correct
            if selected_koala == correct_koala_class:
                st.success(f"Correct! This is {correct_koala_class}.")
                st.session_state['score'] += 1  # Add 1 point for a correct answer
            else:
                st.error(f"Wrong! This was {correct_koala_class}.")
                # Only subtract a point if the score is greater than 0
                if st.session_state['score'] > 0:
                    st.session_state['score'] -= 1  # Subtract 1 point for an incorrect answer

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

