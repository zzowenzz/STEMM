# STEMM day application for the 2024-2025 school year

## Requirements
- Display some reference images per class
- Create some questions with unseen images, each being a multi-choice task.
- Store user answers and calculate the score.
- Implement a leaderboard that is visible to all users, showing their ranks.

## Rules
- The user must answer all questions.
- For each question, the user can only select one answer and they can only submit their answers once.
- If the user is correct, they will receive 1 point. Otherwise, they will receive 0 points. The lowest score is 0.


## File structure
/koala_recognition_competition
│
├── /images               # Directory for storing koala images
│   ├── /koala_1          # Images for koala 1
│   │   ├── ref_1.jpg     # Reference images
│   │   ├── ref_2.jpg
│   │   ├── unseen_1.jpg  # Unseen images for questions
│   │   ├── unseen_2.jpg
│   │   └── ...
│   ├── /koala_2          # Images for koala 2
│   └── ...               # Similarly for the rest of the koalas
│
├── /data                 # Directory for storing user and leaderboard data
│   ├── users.csv         # CSV file to store user emails and hashed passwords
│   ├── leaderboard.csv   # CSV file to store user scores and number of competitions
│
├── /pages                # Directory for different pages in the app
│   ├── login.py          # User login page
│   ├── signup.py         # User sign-up page
│   ├── leaderboard.py    # Leaderboard page
│   ├── competition.py    # Main competition page for multi-choice tasks
│
├── /utils                # Directory for utility functions
│   ├── auth.py           # Functions for authentication (login, signup)
│   ├── leaderboard.py    # Functions to handle leaderboard (update, calculate)
│   ├── questions.py      # Functions to generate and evaluate questions
│
├── app.py                # Main Streamlit app entry point
├── requirements.txt      # Python package dependencies
├── README.md             # Project overview and instructions
└── .gitignore            # Git ignore file
