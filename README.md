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
/koala_competition/
│
├── /images/
│   ├── /koala_1/
│   │   ├── reference_1.jpg
│   │   ├── reference_2.jpg
│   │   ├── reference_3.jpg
│   │   ├── unseen_1.jpg
│   │   ├── unseen_2.jpg
│   ├── /koala_2/
│   │   ├── reference_1.jpg
│   │   ├── reference_2.jpg
│   │   ├── reference_3.jpg
│   │   ├── unseen_1.jpg
│   │   ├── unseen_2.jpg
│   ├── /koala_3/
│   ├── /koala_4/
│   ├── /koala_5/
│
├── /data/
│   ├── leaderboard.csv        # Stores user performance (email, no. of competitions, highest score)
│   ├── users.csv              # Stores user accounts (email, hashed_password)
│
├── /scripts/
│   ├── auth.py                # Handles user authentication (login, signup, hashing passwords)
│   ├── questions.py           # Generates multi-choice questions based on unseen images
│   ├── scoring.py             # Calculates user score based on answers
│   ├── leaderboard.py         # Updates and manages leaderboard data
│
├── streamlit_app.py           # Main Streamlit app file
├── requirements.txt           # List of all dependencies (Streamlit, Pandas, etc.)
└── README.md                  # Project overview and setup instructions


## Working pipeline
1. Requirement Gathering and Planning
- Understand the Problem
- Functional Requirements
    - User authentication
        - signup
        - login
        - Account management
    - Competition
        - Reference page
        - Questions page
        - Score page
    - Leaderboard
        - Ranking
        - Competition history
    - Data storage
        - User data
        - Competition data
        - Leaderboard data
- Non-functional Requirements
    - Performance
    - Security
    - Usability
    - Scalability

2. Design
Wireframes, mockups, and database schema.

3. Technology Stack Selection
Frontend, backend, and database.

4. Development Phase

5. Testing

6. Deployment