# Streamlit is required for this app.
# Please make sure you have Streamlit installed by running:
# pip install streamlit

try:
    import streamlit as st
    import time
except ModuleNotFoundError:
    raise ModuleNotFoundError("Required modules are not installed. Please install them using 'pip install streamlit'")

# --- Simulated simple ChatBot ---
class ChatOllamaBot:
    def chat(self, prompt):
        return f"Echo: {prompt} (Simulated Response)"

# --- Simulated user database (dictionary for this example) ---
user_db = {}

# --- Session state to track login and theme ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'username' not in st.session_state:
    st.session_state.username = ''

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

bot = ChatOllamaBot()

# --- Functions ---
def login(username, password):
    if username in user_db and user_db[username]['password'] == password:
        st.session_state.logged_in = True
        st.session_state.username = username
        return True
    else:
        return False

def signup(email, username, password):
    if username not in user_db:
        user_db[username] = {'email': email, 'password': password}
        return True
    else:
        return False

def logout():
    st.session_state.logged_in = False
    st.session_state.username = ''
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
            st.session_state.logged_in = True
            st.session_state.username = username

    if st.button("Don't have an account? Sign Up Here"):
        st.session_state.page = "Sign Up"

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
                st.success("Account created successfully! Please sign in.")
                st.session_state.page = "Login"
            else:
                st.error("Username already exists. Try another.")

    if st.button("Already have an account? Sign In Here"):
        st.session_state.page = "Login"

def show_dashboard():
    st.markdown(f"""
        <h1 style='text-align: center; color: #1A56DB;'>Welcome {st.session_state.username}, to SportsTracker</h1>
        <h3 style='text-align: center;'>I am The Play Maker, your sports AI assistant</h3>
    """, unsafe_allow_html=True)

    st.subheader("Chat with SportsBot")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask me anything about sports!"):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            assistant_response = bot.chat(prompt)
            for chunk in assistant_response.split():
                full_response += chunk + " "
                time.sleep(0.05)
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

    st.subheader("Choose a Statistical Query")
    queries = ["Player Performance Trends", "Team Win/Loss Ratio", "Season Statistics", "Player Rankings", "League Standings"]
    selected_query = st.selectbox("Select a query:", queries)
    st.success(f"You selected: {selected_query}")

    st.subheader("Statistics Visualization")
    st.line_chart({
        'Data': [400, 300, 500, 700, 450]
    })

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
        © 2025 SportsTracker. All rights reserved.
    </div>
""", unsafe_allow_html=True)
