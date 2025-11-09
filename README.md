# Campaign Tracker

A small, self-contained Campaign Tracker web app (demo) that lets you add, view, update, and delete marketing campaigns.

This project is implemented as a lightweight Flask backend that serves a static HTML/CSS/JS frontend. Data is persisted to a JSON file.

---

## Features

- Add a new campaign (Campaign Name, Client Name, Start Date, Status)
- View list of campaigns
- Update campaign status (Active / Paused / Completed)
- Delete a campaign
- Simple login (demo credentials)
- Search and filter campaigns
- Dashboard summary (total/active/paused/completed)

---

## Tech stack

- Backend: Python 3 + Flask
- Frontend: Static HTML/CSS/JavaScript (`gin.html`)
- Persistence: JSON files (`campaigns.json`, `users.json`)

---

## Files of interest

- `app.py` - Flask application and REST API
- `gin.html` - Frontend UI (served at `/`)
- `campaigns.json` - Stores campaign records
- `users.json` - Stores user credentials (created automatically)
- `add.js` - Small unrelated snippet (not used by the app)

---

## Quick start (Windows - cmd.exe)

1. (Optional) Create a Python virtual environment and activate it:

```cmd
python -m venv venv
venv\Scripts\activate
```

2. Install required Python packages:

```cmd
pip install Flask flask-cors
```

3. Start the backend server:

```cmd
python app.py
```

4. Open your browser and visit:

```
http://127.0.0.1:5000
```

5. Login (demo credentials shown on the page):
```
username:admin
password:1234
```
---

## REST API

Base URL: `http://127.0.0.1:5000/api`

Endpoints:

- `POST /api/login` - Login (JSON body: `{ "username": "admin", "password": "1234" }`)
- `POST /api/logout` - Logout (no body)
- `GET /api/check-login` - Check session
- `GET /api/campaigns` - Get campaigns (query params: `status`, `search`)
- `POST /api/campaigns` - Add a campaign (requires session)
- `PUT /api/campaigns/<id>` - Update a campaign (requires session)
- `DELETE /api/campaigns/<id>` - Delete a campaign (requires session)
- `GET /api/summary` - Dashboard summary


Request notes:
- Add / Update / Delete endpoints require being logged in. The frontend uses cookie-based sessions and sends credentials with fetch calls.

<img width="1200" height="600" alt="Screenshot 2025-10-12 222614" src="https://github.com/user-attachments/assets/3149380d-e0df-4692-b93c-01c35b01ace1" />
<img width="1200" height="600" alt="Screenshot 2025-10-12 222600" src="https://github.com/user-attachments/assets/737ddd90-7625-41fa-a097-dad19141ee91" />








