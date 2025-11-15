# Smart Study Buddy Matchmaker

An intelligent agent-based application that matches college students for optimal study partnerships using the PEAS model.

## PEAS Model Implementation

### Performance Measures
- Match accuracy based on weighted similarity scores
- User satisfaction ratings (1-5 scale)
- Compatibility percentage display

### Environment
- College student user base
- Web-based interface (Streamlit)
- Persistent data storage (pickle file)

### Actuators
- Match recommendations display
- Invitation system (send/accept/decline)
- Real-time chat messaging
- Study session scheduling
- Feedback collection forms

### Sensors
- User profile inputs (subjects, interests, study style, availability)
- Invitation responses
- Chat messages
- Session feedback ratings
- User activity tracking

## Features

- **Login System**: Secure user authentication with pre-loaded demo accounts
- **Smart Matching Algorithm**: Multi-factor weighted similarity scoring
  - 40% Subject overlap
  - 30% Schedule compatibility
  - 20% Common interests
  - 10% Study style match
- **Invitation System**: Send, receive, accept, or decline study partner requests
- **Real-time Chat**: Message accepted study buddies with unread indicators
- **Study Sessions**: Schedule and manage study sessions with partners
- **Feedback System**: Rate completed study sessions (1-5 stars)
- **Dashboard**: View statistics, recent activity, and feedback history

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
streamlit run app_complete.py
```

## Demo Accounts
- alice / alice123
- bob / bob123
- carol / carol123
- david / david123
- emma / emma123

## Technical Implementation

### AI Concepts Used
- **Rule-based Agent**: Uses predefined weighted algorithm for matching
- **Multi-criteria Decision Making**: Combines multiple factors for compatibility scoring
- **Jaccard Similarity**: Measures overlap between user attribute sets
- **Ranking Algorithm**: Sorts and displays top 5 compatible matches

### Data Storage
- Pickle file (study_buddy_data.pkl) for persistent data
- Stores: accounts, user profiles, invitations, messages, sessions, feedback

### Architecture
- Single-file Streamlit application
- Session state management for user authentication
- Tab-based navigation interface