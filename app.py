
from flask import Flask, request, jsonify, send_from_directory, session
from flask_cors import CORS
import json, os, time

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.secret_key = "supersecretkey123" 

CAMPAIGN_FILE = 'campaigns.json'
USER_FILE = 'users.json'

# -------------------- Utility Functions --------------------

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

# -------------------- User Management --------------------

def init_users():
    """Create a default user if users.json doesn't exist."""
    if not os.path.exists(USER_FILE):
        default_user = {
            "username": "admin",
            "password": "1234"
        }
        save_json(USER_FILE, [default_user])

@app.route('/api/login', methods=['POST'])
def login():
    """Login endpoint."""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    users = load_json(USER_FILE)

   
   
    user = next((u for u in users if u['username'] == username and u['password'] == password), None)
    if user:
        session['username'] = username
        return jsonify({'message': 'Login successful', 'username': username})
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/api/logout', methods=['POST'])
def logout():
    """Logout endpoint."""
    session.pop('username', None)
    return jsonify({'message': 'Logged out'})

@app.route('/api/check-login', methods=['GET'])
def check_login():
    """Check if user is logged in."""
    return jsonify({'logged_in': 'username' in session, 'user': session.get('username')})

# -------------------- Campaign Endpoints --------------------

@app.route('/')
def index():
    """Serve frontend HTML."""
    return send_from_directory('.', 'gin.html')

@app.route('/api/campaigns', methods=['GET'])
def get_campaigns():
    """Get all campaigns, with optional filters."""
    campaigns = load_json(CAMPAIGN_FILE)
    status = request.args.get('status', 'All')
    search = request.args.get('search', '').lower()

    if status != 'All':
        campaigns = [c for c in campaigns if c['status'] == status]
    if search:
        campaigns = [c for c in campaigns if search in c['name'].lower() or search in c['client'].lower()]

    return jsonify(campaigns)

@app.route('/api/campaigns', methods=['POST'])
def add_campaign():
    """Add a new campaign."""
    if 'username' not in session:
        return jsonify({'message': 'Unauthorized'}), 401

    data = request.get_json()
    if not all(k in data for k in ['name', 'client', 'startDate', 'status']):
        return jsonify({'message': 'All fields required'}), 400

    campaigns = load_json(CAMPAIGN_FILE)
    new_campaign = {
        'id': int(time.time() * 1000),
        'name': data['name'],
        'client': data['client'],
        'startDate': data['startDate'],
        'status': data['status']
    }
    campaigns.append(new_campaign)
    save_json(CAMPAIGN_FILE, campaigns)
    return jsonify(new_campaign), 201

@app.route('/api/campaigns/<int:id>', methods=['PUT'])
def update_campaign(id):
    """Update a campaign."""
    if 'username' not in session:
        return jsonify({'message': 'Unauthorized'}), 401

    data = request.get_json()
    campaigns = load_json(CAMPAIGN_FILE)
    for c in campaigns:
        if c['id'] == id:
            c['name'] = data.get('name', c['name'])
            c['client'] = data.get('client', c['client'])
            c['startDate'] = data.get('startDate', c['startDate'])
            c['status'] = data.get('status', c['status'])
            save_json(CAMPAIGN_FILE, campaigns)
            return jsonify(c)
    return jsonify({'message': 'Campaign not found'}), 404

@app.route('/api/campaigns/<int:id>', methods=['DELETE'])
def delete_campaign(id):
    """Delete a campaign."""
    if 'username' not in session:
        return jsonify({'message': 'Unauthorized'}), 401

    campaigns = load_json(CAMPAIGN_FILE)
    updated = [c for c in campaigns if c['id'] != id]
    if len(updated) == len(campaigns):
        return jsonify({'message': 'Campaign not found'}), 404
    save_json(CAMPAIGN_FILE, updated)
    return jsonify({'message': 'Deleted successfully'})

@app.route('/api/summary', methods=['GET'])
def summary():
    """Return dashboard summary."""
    campaigns = load_json(CAMPAIGN_FILE)
    summary_data = {
        'total': len(campaigns),
        'active': sum(1 for c in campaigns if c['status'] == 'Active'),
        'paused': sum(1 for c in campaigns if c['status'] == 'Paused'),
        'completed': sum(1 for c in campaigns if c['status'] == 'Completed')
    }
    return jsonify(summary_data)

# -------------- Main -----

if __name__ == '__main__':
    init_users()  
    app.run(debug=True, port=5000)















