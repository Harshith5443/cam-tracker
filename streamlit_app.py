import streamlit as st
import json
import os
import time

# Constants
CAMPAIGN_FILE = 'campaigns.json'
USER_FILE = 'users.json'

# Utility Functions
def load_json(filename):
    """Load data from a JSON file."""
    if not os.path.exists(filename):
        return []
    with open(filename, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_json(filename, data):
    """Save data to a JSON file."""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def init_users():
    """Create a default user if users.json doesn't exist."""
    if not os.path.exists(USER_FILE):
        default_user = {
            "username": "admin",
            "password": "1234"
        }
        save_json(USER_FILE, [default_user])

# Initialize users on startup
init_users()

# Streamlit App
st.set_page_config(page_title="Campaign Tracker", page_icon="📊", layout="wide")

# Session state for login
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = None

def login():
    st.sidebar.title("Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        users = load_json(USER_FILE)
        user = next((u for u in users if u['username'] == username and u['password'] == password), None)
        if user:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.rerun()
        else:
            st.sidebar.error("Invalid credentials")

def logout():
    st.session_state['logged_in'] = False
    st.session_state['username'] = None
    st.rerun()

def main_app():
    st.title("Campaign Tracker")

    # Logout button in sidebar
    if st.sidebar.button("Logout"):
        st.session_state['logged_in'] = False
        st.session_state['username'] = None
        st.rerun()

    # Load data
    campaigns = load_json(CAMPAIGN_FILE)

    # Summary
    total = len(campaigns)
    active = sum(1 for c in campaigns if c['status'] == 'Active')
    paused = sum(1 for c in campaigns if c['status'] == 'Paused')
    completed = sum(1 for c in campaigns if c['status'] == 'Completed')

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total", total)
    col2.metric("Active", active)
    col3.metric("Paused", paused)
    col4.metric("Completed", completed)

    # Search and Filter
    st.subheader("Search & Filter")
    search = st.text_input("Search by campaign or client")
    status_filter = st.selectbox("Filter by Status", ["All", "Active", "Paused", "Completed"])

    # Filter campaigns
    filtered_campaigns = campaigns
    if status_filter != "All":
        filtered_campaigns = [c for c in filtered_campaigns if c['status'] == status_filter]
    if search:
        filtered_campaigns = [c for c in filtered_campaigns if search.lower() in c['name'].lower() or search.lower() in c['client'].lower()]

    # Add Campaign Form
    st.subheader("Add New Campaign")
    with st.form("add_campaign"):
        name = st.text_input("Campaign Name")
        client = st.text_input("Client Name")
        start_date = st.date_input("Start Date")
        status = st.selectbox("Status", ["Active", "Paused", "Completed"])
        submitted = st.form_submit_button("Add Campaign")
        if submitted:
            if name and client and start_date:
                new_campaign = {
                    'id': int(time.time() * 1000),
                    'name': name,
                    'client': client,
                    'startDate': str(start_date),
                    'status': status
                }
                campaigns.append(new_campaign)
                save_json(CAMPAIGN_FILE, campaigns)
                st.success("Campaign added!")
                st.rerun()
            else:
                st.error("All fields are required")

    # Display Campaigns
    st.subheader("Campaigns")
    if filtered_campaigns:
        # Prepare data for dataframe
        df_data = []
        for c in filtered_campaigns:
            df_data.append({
                'ID': c['id'],
                'Name': c['name'],
                'Client': c['client'],
                'Start Date': c['startDate'],
                'Status': c['status']
            })

        # Display as dataframe
        st.dataframe(df_data, use_container_width=True)

        # Edit and Delete
        st.subheader("Edit Status or Delete")
        for c in filtered_campaigns:
            col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 1])
            col1.write(c['name'])
            col2.write(c['client'])
            col3.write(c['startDate'])
            new_status = col4.selectbox(f"Status for {c['id']}", ["Active", "Paused", "Completed"], index=["Active", "Paused", "Completed"].index(c['status']), key=f"status_{c['id']}")
            if new_status != c['status']:
                # Update status
                for camp in campaigns:
                    if camp['id'] == c['id']:
                        camp['status'] = new_status
                        save_json(CAMPAIGN_FILE, campaigns)
                        st.rerun()
            if col5.button("Delete", key=f"delete_{c['id']}"):
                campaigns = [camp for camp in campaigns if camp['id'] != c['id']]
                save_json(CAMPAIGN_FILE, campaigns)
                st.success("Campaign deleted!")
                st.rerun()
    else:
        st.write("No campaigns found.")

if st.session_state['logged_in']:
    main_app()
else:
    # Main front page login with color
    st.markdown("""
    <style>
    .title {
        color: #4f46e5;
        font-size: 2rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 10px;
    }
    .subtitle {
        color: #06b6d4;
        font-size: 1.2rem;
        text-align: center;
        margin-bottom: 20px;
    }
    .demo-credentials {
        background: #e0f2fe;
        padding: 16px;
        border-radius: 8px;
        color: #0c4a6e;
        font-size: 1.1rem;
        font-weight: 500;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="title">Campaign Tracker</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Login to access Campaign Tracker</div>', unsafe_allow_html=True)

    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    if st.button("Login"):
        users = load_json(USER_FILE)
        user = next((u for u in users if u['username'] == username and u['password'] == password), None)
        if user:
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            st.rerun()
        else:
            st.error("Invalid credentials")

    st.markdown('<div class="demo-credentials"><b>Demo Credentials:</b><br><b>Username:</b> <code>admin</code><br><b>Password:</b> <code>1234</code></div>', unsafe_allow_html=True)
