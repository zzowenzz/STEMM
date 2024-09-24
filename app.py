import streamlit as st
import random
from PIL import Image

# Koala classes with image paths
koala_classes = {
    "DES_abbey": ["/home/deep/Owen_ssd/code/STEMM/images/DES_abbey_000001.jpg"],
    "DES_alana": ["/home/deep/Owen_ssd/code/STEMM/images/DES_alana_000001.jpg", "/home/deep/Owen_ssd/code/STEMM/images/DES_alana_000002.jpg"],
    "DES_alex": ["/home/deep/Owen_ssd/code/STEMM/images/DES_alex_000016.jpg", "/home/deep/Owen_ssd/code/STEMM/images/DES_alex_000017.jpg"],
    "DES_alice": ["/home/deep/Owen_ssd/code/STEMM/images/DES_alice_000003.jpg", "/home/deep/Owen_ssd/code/STEMM/images/DES_alice_000004.jpg"],
    "KAG_airlie": ["/home/deep/Owen_ssd/code/STEMM/images/KAG_airlie_000001.jpg"]
}

# Unseen images
unseen_images = [
    "/home/deep/Owen_ssd/code/STEMM/images/DES_abbey_000002.jpg", 
    "/home/deep/Owen_ssd/code/STEMM/images/DES_alana_000003.jpg", 
    "/home/deep/Owen_ssd/code/STEMM/images/DES_alana_000004.jpg",
    "/home/deep/Owen_ssd/code/STEMM/images/DES_alex_000018.jpg", 
    "/home/deep/Owen_ssd/code/STEMM/images/DES_alex_000019.jpg",
    "/home/deep/Owen_ssd/code/STEMM/images/DES_alice_000006.jpg", 
    "/home/deep/Owen_ssd/code/STEMM/images/DES_alice_000011.jpg",
    "/home/deep/Owen_ssd/code/STEMM/images/KAG_airlie_000002.jpg"
]

# Initialize session state to keep track of score, submissions, and whether competition has started
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'submitted' not in st.session_state:
    st.session_state.submitted = [False] * 5  # To track each question's submission status
if 'competition_started' not in st.session_state:
    st.session_state.competition_started = False  # Track whether the competition has started
if 'answers' not in st.session_state:
    st.session_state.answers = [None] * 5  # Keep track of user answers
if 'all_questions_answered' not in st.session_state:
    st.session_state.all_questions_answered = False  # To track when all questions are answered
if 'temp_answers' not in st.session_state:
    st.session_state.temp_answers = [None] * 5  # Store temporary answers before submission

# Ensure the number of questions doesn't exceed the number of unseen images available
if len(unseen_images) < 5:
    st.error("Not enough unseen images to create 5 questions!")
else:
    # Randomly assign an unseen image for each question
    questions = random.sample(unseen_images, 5)  # 5 questions, 1 unseen image per question
    selected_classes = random.sample(list(koala_classes.keys()), 5)  # 5 random classes for the 5 questions

    # Layout for the interface
    def display_reference_images():
        st.markdown("### Reference area")
        cols = st.columns(4)
        for i, (class_name, images) in enumerate(koala_classes.items()):
            with cols[i % 4]:  # Display the images in 4 columns
                st.markdown(f"**{class_name}**")
                for img_path in images:
                    img = Image.open(img_path)
                    st.image(img, width=100)

    # Function to check if all questions are submitted
    def check_all_submitted():
        return all(st.session_state.submitted)

    # Function to ask the questions
    def ask_questions():
        st.markdown("---")  # Horizontal line separator between reference and questions

        for idx in range(5):
            if not st.session_state.submitted[idx]:
                st.markdown(f"### Question {idx + 1}: Which image is from {selected_classes[idx]}?")
                cols = st.columns(1)
                with cols[0]:
                    img = Image.open(questions[idx])
                    st.image(img, width=150)

                # Multiple choice options with an initial "Please select an option" choice
                options = ["Please select an option"] + list(koala_classes.keys())
                st.session_state.temp_answers[idx] = st.radio(f"Select the correct class for Question {idx + 1}:",
                                  options, key=f"q{idx}")

                if st.button(f"Submit Question {idx + 1}", key=f"submit_q{idx}"):
                    if st.session_state.temp_answers[idx] != "Please select an option":
                        st.session_state.answers[idx] = st.session_state.temp_answers[idx]
                        if st.session_state.answers[idx] == selected_classes[idx]:
                            st.session_state.score += 1
                            st.success(f"Correct! You gained 1 point. Current Score: {st.session_state.score}")
                        else:
                            st.session_state.score = max(0, st.session_state.score - 1)
                            st.error(f"Incorrect! You lost 1 point. Current Score: {st.session_state.score}")

                        st.session_state.submitted[idx] = True  # Mark question as answered
                        if check_all_submitted():
                            st.session_state.all_questions_answered = True  # Mark all questions answered if true
                    else:
                        st.error("Please select an answer before submitting.")
            else:
                st.info(f"Question {idx + 1} has been answered.")

            # Add separator between each question
            st.markdown("---")

    # Main app layout
    def main():
        st.title("Koala Face Recognition Competition")

        # Display the reference images
        display_reference_images()

        # If competition hasn't started yet, show the "Start to compete" button
        if not st.session_state.competition_started:
            if st.button("Start to Compete"):
                st.session_state.competition_started = True  # Set flag to True when button is clicked

        # If the competition has started, display the questions
        if st.session_state.competition_started:
            ask_questions()

            # Show final score only if all questions are answered
            if st.session_state.all_questions_answered:
                st.write(f"## Your Total Score: {st.session_state.score}")

    if __name__ == "__main__":
        main()
