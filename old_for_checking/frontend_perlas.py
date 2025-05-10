# Streamlit is required for this app.
# Please make sure you have Streamlit installed by running:
# pip install streamlit

try:
    import ast
    import streamlit as st
    import time
    import pandas as pd
    from app.handler import teams, handler_analytics, exercise, user
    from chatollamabot import ChatOllamabot
    
    

except ModuleNotFoundError:
    raise ModuleNotFoundError("Required modules are not installed. Please install them using 'pip install streamlit'")

# --- Simulated simple ChatBot ---
bot = ChatOllamabot()

user_handler = user.UserHandler()

# --- Session state to track login and theme ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'userid' not in st.session_state:
    st.session_state.userid = ''

if 'page' not in st.session_state:
    st.session_state.page = 'Login'

if 'theme' not in st.session_state:
    st.session_state.theme = 'Light'

# Apply new professional theme styles
st.markdown(f"""
    <style>
    body {{
        background-color: #F9FAFB;
        color: #111827;
        font-family: 'Inter', 'sans-serif';
    }}
    .stButton>button {{
        background-color: #1A56DB;
        color: white;
        border-radius: 8px;
        height: 3em;
        width: 100%;
        font-size: 16px;
        font-family: 'Inter', 'sans-serif';
    }}
    .stTextInput>div>div>input {{
        background-color: #FFFFFF;
        color: #111827;
        font-family: 'Inter', 'sans-serif';
    }}
    .stForm {{
        background-color: #FFFFFF;
        padding: 2em;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        font-family: 'Inter', 'sans-serif';
    }}
    </style>
""", unsafe_allow_html=True)

# Initialize chat history
if 'messages' not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Let's start chatting!"}]
if 'history' not in st.session_state:
    st.session_state.history = []

# --- Functions ---
def signup(email, username, password):
    try:
        userid = user_handler.create_user(username, password, email)
        return userid
    except Exception as e:
        st.error(f"Signup error: {e}")
        return False

def login(username, password):
    userid,memory = user_handler.user_exists(username, password)
    if userid:
        st.session_state.logged_in = True
        st.session_state.username = username 
        st.session_state.userid = userid
        st.session_state.history = ast.literal_eval(memory)
        return True
    return False


def logout():
    user_handler.insert_memory(st.session_state.userid, str(st.session_state.history))
    st.session_state.logged_in = False
    st.session_state.userid = ''
    st.session_state.messages = [{"role": "assistant", "content": "Let's start chatting!"}]
    st.session_state.history = []
    st.session_state.page = 'Login'
    st.rerun()
# --- Callback Functions for Buttons ---
def switch_to_signup():
    st.session_state.page = 'Sign Up'

def switch_to_login():
    st.session_state.page = 'Login'


   
    
def show_login():
    st.markdown(f"""
        <h1 style='text-align: center; color: #1A56DB;'>Welcome to SportsTracker</h1>
        <p style='text-align: center;'>Your ultimate destination for real-time sports updates, team stats, and athlete profiles.</p>
    """, unsafe_allow_html=True)

    st.subheader("Sign in to your account")

    with st.form("login_form"):
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", placeholder="Enter your password", type="password")
        submitted = st.form_submit_button("Sign In")

    if submitted:
          if login(username, password):
              st.success("Login successful!")
              st.rerun()
          else:
              st.error("Invalid username or password.")
   
    if st.button("Don't have an account? Sign Up Here"):
        st.session_state.page = "Sign Up"
        st.rerun()

def show_signup():
    st.markdown(f"""
        <h1 style='text-align: center; color: #1A56DB;'>Welcome to SportsTracker</h1>
    """, unsafe_allow_html=True)

    st.subheader("Create your account")

    with st.form("signup_form"):
        email = st.text_input("Email", placeholder="Enter your email")
        username = st.text_input("Username", placeholder="Enter your username (4-20 characters)")
        password = st.text_input("Password", placeholder="Enter your password (min. 8 characters)", type="password")
        confirm_password = st.text_input("Confirm Password", placeholder="Confirm your password", type="password")
        submitted = st.form_submit_button("Create Account")

        if submitted:
            if password != confirm_password:
                st.error("Passwords do not match.")
            elif len(password) < 8:
                st.error("Password must be at least 8 characters.")
            elif signup(email, username, password):
                st.success("Account created successfully! Logging in...")
                login(username, password)
                st.rerun()
            
            else:
                st.error("Username already exists. Try another.")

    if st.button("Already have an account? Sign In Here"):
        st.session_state.page = "Login"

def show_dashboard():
    st.markdown(f"""
        <h1 style='text-align: center; color: #1A56DB;'>Welcome {st.session_state.username}, to SportsTracker</h1>
        <h3 style='text-align: center;'>I am The Play Maker, your exercises AI assistant</h3>
    """, unsafe_allow_html=True)

    st.subheader("Chat with The Play Maker")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask me anything about exercises!"):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            assistant_response, st.session_state.history = bot.chat(prompt,st.session_state.history)
            for chunk in assistant_response.split():
                full_response += chunk + " "
                time.sleep(0.05)
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

    # st.subheader("Choose a Statistical Query")
    # queries = ["Player Performance Trends", "Team Win/Loss Ratio", "Season Statistics", "Player Rankings", "League Standings"]
    # selected_query = st.selectbox("Select a query:", queries)
    # st.success(f"You selected: {selected_query}")

    # st.subheader("Statistics Visualization")
    # st.line_chart({
    #     'Data': [400, 300, 500, 700, 450]
    # })

    # Dropdown Menu
    st.subheader("View Statistics")
    queries = [
        "Top 3 Teams with Most Championships",
        "Team Count per Sport",
        "Sports Popularity Ranking",
        "Teams with Most Championship Wins",
        "Top 5 Most Performed Exercises",
        "Exercises by Muscle Group",
        "Most Complex Exercises"
    ]
    selected_query = st.selectbox("Select a statistic:", queries)

     # Input for Muscle (only if needed)
    if selected_query == "Exercises by Muscle Group":
        muscle_options = [
            "abductors",
            "biceps",
            "lower back",
            "glutes",
            "calves",
            "quadriceps",
            "shoulders",
            "triceps",
            "neck",
            "adductors",
            "chest",
            "abdominals",
            "hamstrings",
            "forearms",
            "traps",
            "middle back",
            "lats"
        ]
        muscle_text = st.selectbox("Select a Muscle Group", muscle_options)

    confirm_button = st.button("Confirm Selection", use_container_width=False)

    # Fetch and Plot
    st.subheader("Statistics Visualization")


    if confirm_button:

        if selected_query == "Top 3 Teams with Most Championships":
            data = teams.TeamHandler().getTopTeams(jsonify_result=False)
            df = pd.DataFrame(data)
            st.bar_chart(df.set_index('name')['championships_won'])

        elif selected_query == "Team Count per Sport":
            data = teams.TeamHandler().getSportsDistribution(jsonify_result=False)
            df = pd.DataFrame(data)
            st.bar_chart(df.set_index('sport')['team_count'])

        elif selected_query == "Sports Popularity Ranking":
            data = handler_analytics.AnalyticsHandler().getSportPopularity(jsonify_result=False)
            df = pd.DataFrame(data)
            st.bar_chart(df.set_index('sport')['athlete_count'])

        elif selected_query == "Teams with Most Championship Wins":
            data = handler_analytics.AnalyticsHandler().getMostChampionshipWins(jsonify_result=False)
            df = pd.DataFrame(data)
            st.bar_chart(df.set_index('name')['total_wins'])

        elif selected_query == "Top 5 Most Performed Exercises":
            data = exercise.ExerciseHandler().get_most_performed_exercises(jsonify_result=False)
            df = pd.DataFrame(data)
            st.bar_chart(df.set_index('name')['sports_related'])

        elif selected_query == "Exercises by Muscle Group" and muscle_text:
            cleaned_muscle = muscle_text.strip().lower()  # Normalize input
            try:
                data = exercise.ExerciseHandler().get_exercises_by_muscle(cleaned_muscle, jsonify_result=False)
                if data:
                    df = pd.DataFrame(data)
                    st.dataframe(df)
                    #st.dataframe(df[["name"]])  # used to only show names
                else:
                    st.warning(f"No exercises found for muscle group: '{muscle_text}'")
            except Exception as e:
                st.error(f"Error: {str(e)}")

        # elif selected_query == "Most Complex Exercises":
        #     data = exercise.ExerciseHandler().get_most_complex_exercises(jsonify_result=False)
        #     df = pd.DataFrame(data)
        #     st.bar_chart(df.set_index('name')['muscle_groups'])

        # elif selected_query == "Exercises by Muscle Group" and muscle_text:
        #     data = exercise.ExerciseHandler().get_exercises_by_muscle(muscle_text, jsonify_result=False)
        #     df = pd.DataFrame(data)

        #     if not df.empty:
        #         # Assign 1 to each exercise (for graph purposes)
        #         df['count'] = 1
        #         st.bar_chart(df.set_index('name')['count'])
        #     else:
        #         st.warning("No exercises found for this muscle group.")

        elif selected_query == "Most Complex Exercises":
            data = exercise.ExerciseHandler().get_most_complex_exercises(jsonify_result=False)
            # Convert the list of muscle groups into a count
            for exercise_item in data:
                exercise_item['muscle_group_count'] = len(exercise_item['muscle_groups'])

            df = pd.DataFrame(data)
            st.bar_chart(df.set_index('name')['muscle_group_count'])


        else:
            st.warning("Please select a query.")

    if st.button("Logout"):
        logout()

# --- App ---
if st.session_state.logged_in:
    show_dashboard()
else:
    if st.session_state.page == "Login":
        show_login()
    elif st.session_state.page == "Sign Up":
        show_signup()

# Footer
st.markdown("""
    <hr>
    <div style='text-align: center; color: #6B7280;'>
        © 2025 PHGA SportsTracker. All rights reserved.
    </div>
""", unsafe_allow_html=True)
