import streamlit as st
import pickle
import os
from datetime import datetime, timedelta

STORAGE_FILE = "study_buddy_data.pkl"

def load_persistent_data():
    if os.path.exists(STORAGE_FILE):
        try:
            with open(STORAGE_FILE, 'rb') as f:
                return pickle.load(f)
        except:
            pass
    
    return {
        "accounts": {
            "admin": "password123",
            "alice": "alice123",
            "bob": "bob123",
            "carol": "carol123",
            "david": "david123",
            "emma": "emma123"
        },
        "users": {
            "alice": {"name": "Alice Chen", "subjects": ["Math", "Physics"], "interests": ["Technology", "Reading"], "study_style": "Visual", "availability": ["Morning", "Evening"]},
            "bob": {"name": "Bob Martinez", "subjects": ["Computer Science", "Math"], "interests": ["Gaming", "Technology"], "study_style": "Kinesthetic", "availability": ["Afternoon", "Evening"]},
            "carol": {"name": "Carol Johnson", "subjects": ["Biology", "Chemistry"], "interests": ["Sports", "Music"], "study_style": "Auditory", "availability": ["Morning", "Weekend"]},
            "david": {"name": "David Kim", "subjects": ["Physics", "Math"], "interests": ["Technology", "Movies"], "study_style": "Visual", "availability": ["Evening", "Weekend"]},
            "emma": {"name": "Emma Wilson", "subjects": ["Literature", "History"], "interests": ["Reading", "Art"], "study_style": "Reading/Writing", "availability": ["Morning", "Afternoon"]}
        },
        "invitations": [],
        "invitation_counter": 0,
        "messages": [],
        "message_counter": 0,
        "sessions": [],
        "session_counter": 0,
        "feedback": []
    }

def save_persistent_data(data):
    with open(STORAGE_FILE, 'wb') as f:
        pickle.dump(data, f)

def init_session():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'current_user' not in st.session_state:
        st.session_state.current_user = None

def calculate_match_score(user1, user2):
    score = 0
    common_subjects = len(set(user1["subjects"]) & set(user2["subjects"]))
    total_subjects = len(set(user1["subjects"]) | set(user2["subjects"]))
    score += (common_subjects / total_subjects) * 0.4 if total_subjects > 0 else 0
    
    common_times = len(set(user1["availability"]) & set(user2["availability"]))
    total_times = len(set(user1["availability"]) | set(user2["availability"]))
    score += (common_times / total_times) * 0.3 if total_times > 0 else 0
    
    common_interests = len(set(user1["interests"]) & set(user2["interests"]))
    total_interests = len(set(user1["interests"]) | set(user2["interests"]))
    score += (common_interests / total_interests) * 0.2 if total_interests > 0 else 0
    
    score += 0.1 if user1["study_style"] == user2["study_style"] else 0.05
    
    return score

def get_accepted_buddies(username, data):
    """Get list of accepted study buddies"""
    buddies = []
    for inv in data["invitations"]:
        if inv["status"] == "accepted":
            if inv["from_username"] == username:
                buddies.append(inv["to_username"])
            elif inv["to_username"] == username:
                buddies.append(inv["from_username"])
    return list(set(buddies))

def get_unread_count(username, buddy_username, data):
    """Count unread messages from a buddy"""
    if "messages" not in data:
        data["messages"] = []
    count = 0
    for msg in data["messages"]:
        if msg["to_username"] == username and msg["from_username"] == buddy_username and not msg.get("read", False):
            count += 1
    return count

def main():
    st.set_page_config(page_title="Study Buddy Matchmaker", page_icon="🎓", layout="wide")
    init_session()
    
    data = load_persistent_data()
    
    st.title("🎓 Smart Study Buddy Matchmaker")
    st.caption("AI-Powered Study Partner Matching System")
    
    if not st.session_state.logged_in:
        st.header("🔐 Login")
        
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login", type="primary")
            
            if submitted:
                if username in data["accounts"] and data["accounts"][username] == password:
                    st.session_state.logged_in = True
                    st.session_state.current_user = username
                    st.success(f"✅ Welcome, {data['users'][username]['name']}!")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials")
    
    else:
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.write(f"### 👤 {data['users'][st.session_state.current_user]['name']}")
        with col2:
            buddies = get_accepted_buddies(st.session_state.current_user, data)
            st.metric("Study Buddies", len(buddies))
        with col3:
            if st.button("Logout", type="secondary"):
                st.session_state.logged_in = False
                st.session_state.current_user = None
                # Clear matches when logging out
                st.session_state.show_matches = False
                st.session_state.matches_list = []
                st.rerun()
        
        st.divider()
        
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["🔍 Find Matches", "📬 Invitations", "💬 Chat", "📅 Study Sessions", "⭐ Feedback", "📊 Dashboard"])
        
        with tab1:
            st.header("Find Your Perfect Study Match")
            
            current_user = data["users"][st.session_state.current_user]
            
            with st.expander("📋 My Profile"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**Subjects:**", ", ".join(current_user["subjects"]))
                    st.write("**Study Style:**", current_user["study_style"])
                with col2:
                    st.write("**Interests:**", ", ".join(current_user["interests"]))
                    st.write("**Availability:**", ", ".join(current_user["availability"]))
            
            # Initialize or check if matches belong to current user
            if 'show_matches' not in st.session_state:
                st.session_state.show_matches = False
            if 'matches_list' not in st.session_state:
                st.session_state.matches_list = []
            if 'matches_for_user' not in st.session_state:
                st.session_state.matches_for_user = None
            
            # Reset matches if user changed
            if st.session_state.matches_for_user != st.session_state.current_user:
                st.session_state.show_matches = False
                st.session_state.matches_list = []
                st.session_state.matches_for_user = st.session_state.current_user
            
            if st.button("🎯 Find Compatible Study Partners", type="primary", use_container_width=True):
                st.session_state.show_matches = True
                st.session_state.matches_for_user = st.session_state.current_user
                matches = []
                for username, user_info in data["users"].items():
                    if username != st.session_state.current_user:
                        score = calculate_match_score(current_user, user_info)
                        matches.append((username, user_info, score))
                
                matches.sort(key=lambda x: x[2], reverse=True)
                st.session_state.matches_list = matches[:5]
            
            if st.session_state.show_matches and st.session_state.matches_list:
                st.success(f"✨ Found {len(st.session_state.matches_list)} compatible study partners!")
                st.write("")
                
                for i, (username, user_info, score) in enumerate(st.session_state.matches_list, 1):
                    match_pct = int(score * 100)
                    
                    if match_pct >= 70:
                        badge = "🟢 Excellent"
                    elif match_pct >= 50:
                        badge = "🟡 Good"
                    else:
                        badge = "🟠 Fair"
                    
                    with st.container():
                        st.write(f"### {i}. {user_info['name']}")
                        st.progress(match_pct / 100)
                        st.caption(f"Compatibility Score: {match_pct}% {badge}")
                    
                    col1, col2, col3 = st.columns([2, 2, 1])
                    
                    with col1:
                        st.write("**📚 Subjects:**", ", ".join(user_info["subjects"]))
                        st.write("**🎨 Interests:**", ", ".join(user_info["interests"]))
                    
                    with col2:
                        st.write("**📖 Style:**", user_info["study_style"])
                        st.write("**⏰ Available:**", ", ".join(user_info["availability"]))
                    
                    with col3:
                        already_sent = any(inv["to_username"] == username and inv["from_username"] == st.session_state.current_user 
                                         for inv in data["invitations"])
                        
                        if already_sent:
                            st.button("✅ Sent", key=f"sent_{i}", disabled=True, use_container_width=True)
                        else:
                            if st.button("📨 Invite", key=f"invite_{i}", type="primary", use_container_width=True):
                                data["invitation_counter"] += 1
                                invitation = {
                                    "id": data["invitation_counter"],
                                    "from_username": st.session_state.current_user,
                                    "from_name": current_user["name"],
                                    "to_username": username,
                                    "to_name": user_info["name"],
                                    "match_score": score,
                                    "status": "pending",
                                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                }
                                data["invitations"].append(invitation)
                                save_persistent_data(data)
                                
                                st.balloons()
                                st.success(f"🎉 Invitation sent to {user_info['name']}!")
                                st.rerun()
                    
                    st.divider()
        
        with tab2:
            st.header("Study Partner Invitations")
            
            received = [inv for inv in data["invitations"] if inv["to_username"] == st.session_state.current_user]
            sent = [inv for inv in data["invitations"] if inv["from_username"] == st.session_state.current_user]
            
            st.subheader(f"📨 Received Invitations ({len(received)})")
            
            if received:
                for inv in received:
                    match_pct = int(inv["match_score"] * 100)
                    
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.write(f"### From: {inv['from_name']}")
                        st.write(f"**Compatibility:** {match_pct}%")
                        st.write(f"**Status:** {inv['status'].title()}")
                        st.caption(f"Sent: {inv['timestamp']}")
                    
                    with col2:
                        if inv["status"] == "pending":
                            if st.button("✅ Accept", key=f"accept_{inv['id']}", type="primary", use_container_width=True):
                                for invitation in data["invitations"]:
                                    if invitation["id"] == inv["id"]:
                                        invitation["status"] = "accepted"
                                save_persistent_data(data)
                                st.success("Accepted!")
                                st.rerun()
                            
                            if st.button("❌ Decline", key=f"decline_{inv['id']}", use_container_width=True):
                                for invitation in data["invitations"]:
                                    if invitation["id"] == inv["id"]:
                                        invitation["status"] = "declined"
                                save_persistent_data(data)
                                st.info("Declined")
                                st.rerun()
                    
                    st.divider()
            else:
                st.info("No invitations received yet")
            
            st.write("")
            st.subheader(f"📤 Sent Invitations ({len(sent)})")
            
            if sent:
                for inv in sent:
                    status_emoji = {"pending": "⏳", "accepted": "✅", "declined": "❌"}[inv["status"]]
                    match_pct = int(inv["match_score"] * 100)
                    with st.container():
                        col1, col2, col3 = st.columns([2, 1, 1])
                        with col1:
                            st.write(f"{status_emoji} **{inv['to_name']}**")
                        with col2:
                            st.write(f"Compatibility: {match_pct}%")
                        with col3:
                            st.write(f"{inv['status'].title()}")
                        st.caption(inv['timestamp'])
                        st.divider()
            else:
                st.info("No invitations sent yet. Visit 'Find Matches' to connect with study partners!")
        
        with tab3:
            st.header("💬 Chat with Study Partners")
            
            buddies = get_accepted_buddies(st.session_state.current_user, data)
            
            if buddies:
                col1, col2 = st.columns([1, 3])
                
                with col1:
                    st.subheader("Active Chats")
                    
                    if 'selected_buddy' not in st.session_state:
                        st.session_state.selected_buddy = buddies[0]
                    
                    for buddy in buddies:
                        unread = get_unread_count(st.session_state.current_user, buddy, data)
                        buddy_name = data["users"][buddy]["name"]
                        
                        button_label = f"{buddy_name}"
                        if unread > 0:
                            button_label += f" ({unread} new)"
                        
                        if st.button(button_label, key=f"buddy_{buddy}", use_container_width=True):
                            st.session_state.selected_buddy = buddy
                            # Mark messages as read
                            for msg in data["messages"]:
                                if msg["to_username"] == st.session_state.current_user and msg["from_username"] == buddy:
                                    msg["read"] = True
                            save_persistent_data(data)
                            st.rerun()
                
                with col2:
                    selected_buddy = st.session_state.selected_buddy
                    buddy_name = data["users"][selected_buddy]["name"]
                    
                    st.subheader(f"💬 {buddy_name}")
                    
                    # Display messages
                    if "messages" not in data:
                        data["messages"] = []
                    messages = [msg for msg in data["messages"] 
                               if (msg["from_username"] == st.session_state.current_user and msg["to_username"] == selected_buddy) or
                                  (msg["from_username"] == selected_buddy and msg["to_username"] == st.session_state.current_user)]
                    
                    messages.sort(key=lambda x: x["timestamp"])
                    
                    # Chat container
                    chat_container = st.container(height=400)
                    with chat_container:
                        if messages:
                            for msg in messages:
                                if msg["from_username"] == st.session_state.current_user:
                                    with st.chat_message("user"):
                                        st.write(msg["message"])
                                        st.caption(msg["timestamp"])
                                else:
                                    with st.chat_message("assistant"):
                                        st.write(msg["message"])
                                        st.caption(msg["timestamp"])
                        else:
                            st.info("No messages yet. Start the conversation!")
                    
                    # Message input
                    message_input = st.chat_input("Type your message...")
                    
                    if message_input:
                        if "message_counter" not in data:
                            data["message_counter"] = 0
                        data["message_counter"] += 1
                        new_message = {
                            "id": data["message_counter"],
                            "from_username": st.session_state.current_user,
                            "to_username": selected_buddy,
                            "message": message_input,
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "read": False
                        }
                        data["messages"].append(new_message)
                        save_persistent_data(data)
                        st.rerun()
            else:
                st.info("No active study partners yet. Accept invitations to start chatting!")
        
        with tab4:
            st.header("📅 Schedule & Manage Study Sessions")
            
            buddies = get_accepted_buddies(st.session_state.current_user, data)
            
            if buddies:
                st.subheader("📝 Schedule New Study Session")
                
                with st.form("schedule_session"):
                    buddy = st.selectbox("Study Partner", [data["users"][b]["name"] for b in buddies])
                    session_date = st.date_input("Date", min_value=datetime.now().date())
                    session_time = st.time_input("Time")
                    duration = st.selectbox("Duration", ["30 min", "1 hour", "1.5 hours", "2 hours", "3 hours"])
                    location = st.selectbox("Location", ["Library", "Online (Zoom)", "Online (Google Meet)", "Cafe", "Study Room", "Other"])
                    subject = st.text_input("Subject/Topic")
                    notes = st.text_area("Notes (optional)")
                    
                    if st.form_submit_button("📅 Schedule Session", type="primary"):
                        buddy_username = [u for u, d in data["users"].items() if d["name"] == buddy][0]
                        
                        if "session_counter" not in data:
                            data["session_counter"] = 0
                        if "sessions" not in data:
                            data["sessions"] = []
                        data["session_counter"] += 1
                        session = {
                            "id": data["session_counter"],
                            "user1": st.session_state.current_user,
                            "user2": buddy_username,
                            "date": session_date.strftime("%Y-%m-%d"),
                            "time": session_time.strftime("%H:%M"),
                            "duration": duration,
                            "location": location,
                            "subject": subject,
                            "notes": notes,
                            "status": "scheduled",
                            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                        data["sessions"].append(session)
                        save_persistent_data(data)
                        
                        st.success(f"✅ Session scheduled with {buddy}!")
                        st.balloons()
                        st.rerun()
                
                st.divider()
                st.subheader("📆 Upcoming Study Sessions")
                
                if "sessions" not in data:
                    data["sessions"] = []
                my_sessions = [s for s in data["sessions"] 
                              if (s["user1"] == st.session_state.current_user or s["user2"] == st.session_state.current_user) 
                              and s["status"] == "scheduled"]
                
                if my_sessions:
                    for session in sorted(my_sessions, key=lambda x: x["date"]):
                        partner = session["user2"] if session["user1"] == st.session_state.current_user else session["user1"]
                        partner_name = data["users"][partner]["name"]
                        
                        with st.expander(f"📚 {session['subject']} with {partner_name}", expanded=False):
                            st.write(f"**📅 Date:** {session['date']}")
                            st.write(f"**🕐 Time:** {session['time']}")
                            col1, col2 = st.columns([2, 1])
                            
                            with col1:
                                st.write(f"**Duration:** {session['duration']}")
                                st.write(f"**Location:** {session['location']}")
                                if session['notes']:
                                    st.write(f"**Notes:** {session['notes']}")
                            
                            with col2:
                                if st.button("✅ Complete", key=f"complete_{session['id']}", use_container_width=True):
                                    for s in data["sessions"]:
                                        if s["id"] == session["id"]:
                                            s["status"] = "completed"
                                    save_persistent_data(data)
                                    st.success("Session completed!")
                                    st.rerun()
                                
                                if st.button("❌ Cancel", key=f"cancel_{session['id']}", use_container_width=True):
                                    for s in data["sessions"]:
                                        if s["id"] == session["id"]:
                                            s["status"] = "cancelled"
                                    save_persistent_data(data)
                                    st.info("Session cancelled")
                                    st.rerun()
                else:
                    st.info("No upcoming sessions scheduled. Create one above to get started!")
            else:
                st.info("Accept study partner invitations first to schedule sessions!")
        
        with tab5:
            st.header("⭐ Rate Your Study Sessions")
            
            if "sessions" not in data:
                data["sessions"] = []
            if "feedback" not in data:
                data["feedback"] = []
            completed_sessions = [s for s in data["sessions"] 
                                 if (s["user1"] == st.session_state.current_user or s["user2"] == st.session_state.current_user) 
                                 and s["status"] == "completed"]
            
            if completed_sessions:
                # Check which sessions don't have feedback yet
                sessions_without_feedback = []
                for session in completed_sessions:
                    has_feedback = any(f["session_id"] == session["id"] and f["from_username"] == st.session_state.current_user 
                                      for f in data["feedback"])
                    if not has_feedback:
                        sessions_without_feedback.append(session)
                
                if sessions_without_feedback:
                    st.subheader("📝 Provide Session Feedback")
                    
                    for session in sessions_without_feedback:
                        partner = session["user2"] if session["user1"] == st.session_state.current_user else session["user1"]
                        partner_name = data["users"][partner]["name"]
                        
                        with st.expander(f"Session: {session['subject']} with {partner_name}", expanded=False):
                            st.caption(f"Date: {session['date']}")
                            with st.form(f"feedback_{session['id']}"):
                                rating = st.slider("Rating", 1, 5, 3, key=f"rating_{session['id']}")
                                productivity = st.slider("Productivity", 1, 5, 3, key=f"prod_{session['id']}")
                                would_study_again = st.radio("Would you study with them again?", ["Yes", "Maybe", "No"], key=f"again_{session['id']}")
                                comments = st.text_area("Comments (optional)", key=f"comments_{session['id']}")
                                
                                if st.form_submit_button("Submit Feedback", type="primary"):
                                    feedback = {
                                        "session_id": session["id"],
                                        "from_username": st.session_state.current_user,
                                        "partner_username": partner,
                                        "rating": rating,
                                        "productivity": productivity,
                                        "would_study_again": would_study_again,
                                        "comments": comments,
                                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                    }
                                    data["feedback"].append(feedback)
                                    save_persistent_data(data)
                                    
                                    st.success("Thank you for your feedback!")
                                    st.rerun()
                else:
                    st.success("✅ All completed sessions have been rated! Great job!")
                
                st.divider()
                st.subheader("📜 Your Feedback History")
                
                my_feedback = [f for f in data["feedback"] if f["from_username"] == st.session_state.current_user]
                
                if my_feedback:
                    for fb in my_feedback:
                        partner_name = data["users"][fb["partner_username"]]["name"]
                        st.write(f"⭐ **{partner_name}** - Rating: {fb['rating']}/5 | Productivity: {fb['productivity']}/5 | {fb['timestamp']}")
                        if fb['comments']:
                            st.write(f"  💬 {fb['comments']}")
            else:
                st.info("Complete study sessions first, then you can provide feedback!")
        
        with tab6:
            st.header("📊 Your Activity Dashboard")
            
            if "sessions" not in data:
                data["sessions"] = []
            if "feedback" not in data:
                data["feedback"] = []
            
            received = [inv for inv in data["invitations"] if inv["to_username"] == st.session_state.current_user]
            sent = [inv for inv in data["invitations"] if inv["from_username"] == st.session_state.current_user]
            my_sessions = [s for s in data["sessions"] if s["user1"] == st.session_state.current_user or s["user2"] == st.session_state.current_user]
            my_feedback = [f for f in data["feedback"] if f["from_username"] == st.session_state.current_user]
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("📤 Invitations Sent", len(sent))
            with col2:
                st.metric("📨 Invitations Received", len(received))
            with col3:
                accepted = len([inv for inv in sent if inv["status"] == "accepted"])
                st.metric("✅ Connections Made", accepted)
            with col4:
                completed = len([s for s in my_sessions if s["status"] == "completed"])
                st.metric("📚 Sessions Completed", completed)
            
            st.write("")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("🤝 Your Study Partners")
                buddies = get_accepted_buddies(st.session_state.current_user, data)
                if buddies:
                    for buddy in buddies:
                        buddy_name = data["users"][buddy]["name"]
                        buddy_sessions = len([s for s in my_sessions if (s["user1"] == buddy or s["user2"] == buddy) and s["status"] == "completed"])
                        st.write(f"👥 **{buddy_name}**")
                        st.caption(f"{buddy_sessions} sessions completed")
                        st.divider()
                else:
                    st.info("No study partners yet. Start by finding matches!")
            
            with col2:
                st.subheader("📈 Your Performance")
                if my_feedback:
                    avg_rating = sum(f["rating"] for f in my_feedback) / len(my_feedback)
                    avg_productivity = sum(f["productivity"] for f in my_feedback) / len(my_feedback)
                    st.metric("⭐ Average Session Rating", f"{avg_rating:.1f}/5")
                    st.metric("📈 Average Productivity", f"{avg_productivity:.1f}/5")
                    
                    would_study_again_yes = len([f for f in my_feedback if f["would_study_again"] == "Yes"])
                    if len(my_feedback) > 0:
                        st.metric("🔄 Would Study Again", f"{(would_study_again_yes/len(my_feedback)*100):.0f}%")
                else:
                    st.info("Complete sessions and provide feedback to see your performance metrics!")

if __name__ == "__main__":
    main()