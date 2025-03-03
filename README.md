# Web Application Exercise

A Flask-based forum application that allows users to create, edit, delete posts and add comments. You can search for posts by title, content, or username.

## Features

- Create, edit, and delete posts
- Add comments to posts
- Search functionality to find posts by title, content, or username
- Users can login to have the capability to create, edit, delete, and add comments
- Users can create an account to login
- Responsive design for mobile application
- Support for both MongoDB and mock database for development

## Steps to Run the Software

1. Clone the repository
2. Make sure you have Python 3.x installed
3. Install Flask:
   ```bash
   pip install Flask
   ```
4. Run the application:
   ```bash
   python3 app.py
   ```
5. Open your browser and navigate to `http://localhost:5000`

## Development Notes

- The application can run with either MongoDB or a mock database for development
- For MongoDB setup, create a `.env` file based on `env.example` and add your MongoDB connection string
- For local development, the mock database is used by default

## User Stories

Our user stories are tracked in the GitHub Projects board. They include:

- As a user, I can create new posts to share my thoughts
- As a user, I want to click on any brief of a post to view the whole post
- As a user, I want to be able to see all briefs of posts to choose which one to click on
- As a user, I can edit my existing posts to update information
- As a user, I can delete my posts when they are no longer relevant
- As a user, I can comment on posts to engage in discussions
- As a user, I want to see the comments on a post to read the discussion
- As a user, I can search for posts by title to find topics I want to see
- As a user, I want to search for posts by author to find discussion from one person
- As a user, I want to search for posts by keywords in the content to see discussion related to a topic
- As a user, I want to login to create and comment on posts
- As a user, I want to create an account to have login capabilities
- As a user, I want to logout to go back to the public screen

[Link to User Stories Board](https://github.com/software-students-spring2025/2-web-app-msje/projects)

## Task Boards

Our development progress is tracked using GitHub Projects. You can view our:

- [Sprint Planning Board](https://github.com/software-students-spring2025/2-web-app-msje/projects)
- [Bug Tracking Board](https://github.com/software-students-spring2025/2-web-app-msje/projects)
- [Feature Request Board](https://github.com/software-students-spring2025/2-web-app-msje/projects)
