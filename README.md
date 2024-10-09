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
```
/koala_competition/
│   .streamlit/
│   └── secrets.toml
├── /scripts/
│   ├── auth.py                 # For user authentication (register, login, logout)
│   ├── images.py               # For handling reference and unseen images
│   ├── competition.py          # For handling the competition logic (rules, quiz, etc.)
│   ├── leaderboard.py          # For leaderboard management (if needed in the future)
├── /data/
│   ├── users.csv               # User data (email, hashed passwords)
│   ├── leaderboard.csv         # Leaderboard data (scores, number of attempts)
├── /images/                    # Directory containing koala images
│   ├── /Koala 1/               # Images for Koala 1 (reference and unseen images)
│   ├── /Koala 2/
│   ├── /Koala 3/
│   ├── /Koala 4/
│   ├── /Koala 5/
├── streamlit_app.py            # Main Streamlit app file
├── requirements.txt            # Python dependencies
└── README.md                   # Project overview and setup instructions
```


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
As I store the images and data in the local directory, I need to migrate your locally stored data (CSV files) and images to a cloud-based storage solution. 
- Cloud Storage for Images. Store images on AWS S3 bucket.
- Cloud Database for User Data and Leaderboard. Store the ranking data in ASW RDS with Aurora PostgreSQL.
- Generate a Docker image.
- Deploy the Docker image to Heroku.
    - login `heroku login -i `
    - delete the existing app `heroku apps:destroy --app your-app-name --confirm your-app-name`
    - create a new app `heroku create your-app-name`
    - set the deployment method using Docer `heroku stack:set container`
    - prepare Dockerfile, requirements.txt, and Procfile
    - config environment variables like AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, S3_BUCKET_NAME, DATABASE_URL, SECRET_KEY, etc.
    - commit changes and push code to Heroku `git add . && git commit -m "Deploy to Heroku" && git push heroku main
`
