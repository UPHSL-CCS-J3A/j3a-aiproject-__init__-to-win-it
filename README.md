Presentors: Raxell Constantino, Miguel Laxamana, and Jullie Temporosa
Smart Study Buddy Matchmaker

Problem Description
Many college students struggle to find compatible study partners or group members who share similar academic goals, schedules, and learning styles. This often leads to unproductive study sessions, poor collaboration, and reduced academic performance.

Proposed Solution Overview
The Smart Study Buddy Matchmaker system aims to intelligently pair students based on shared subjects, compatible study habits, and mutual availability. Using data-driven algorithms, it analyzes user profiles, preferences, and past collaboration feedback to suggest the best possible study partners or small groups.

PEAS Model
1. Performance Measure
Description: The metrics used to evaluate the agent's success and efficiency.
Measures: Match accuracy, User satisfaction ratings, Successful study sessions (e.g., sessions leading to a high rating), Fairness of recommendations, and System response time
2. Environment
Description: The complete setting in which the agent operates.
Details: 
    The college's student user base
    Stored profile data (academic and personal preferences)
    The app's digital interface (web or mobile platform)
3. Actuators
Description: The mechanisms the agent uses to affect the environment and communicate with users.
Actions:
    Displaying match suggestions
    Sending study invitations
    Recommending schedules
    Updating user matches based on continuous feedback
4. Sensors
Description: The agent's inputs—how it receives information from the environment.
Inputs:
    User inputs (profile information, subjects, interests, time availability)
    Feedback ratings (post-session reviews)
    Chat activity
    System usage logs


AI Concepts Used
1. Intelligent Agent Type:
    Goal-based and learning agent, the system’s goal is to create optimal matches and it learns from user feedback to improve future recommendations.

2. Search or Optimization Strategy:
    Similarity-based matching and preference optimization using algorithms such as k-nearest neighbors (KNN) or weighted cosine similarity to find the best partner combinations.

3. Learning or Decision Component:
    Machine learning (supervised or reinforcement learning) is used to refine match accuracy over time based on feedback data, improving pairing outcomes dynamically.

