# Phishing Deetection Application Web Application

This is the **Flask web application** that provides a user interface for the phishing detection system.
It willintegrate with the backend service to allow users / admins to test emails and manage access via authentication.

## Features

- **User Authentication**
  - Login / Sign up system
  - Password hashing and secure session management
- **Admin Dashboard**
  - Admin page for managing users and logs history
  - Access to classified emails (legitimate / illegitimate)
- **Prediction page**
  - Paste or type the emai'ls **subject** and or **body**.
  - Submit to get phishing / non-phishing result.
  - Reset button to clear the form

- **Database**
  - SQLite database for storing users and classification history.

- **Frontend**
  - Templates for login, register, admin panel, and prediction page.
  - Static assets for styling

## Project Structure

```bash
app/
├── auth/ #Authentication
│   └── forms.py
│   └── models.py
├── instance/ #Database instance
├── static/ #static assets
│   └──── js/
│     └── form-validation.js
│── templates/ #HTML templates (using Jinja2)
│   └──── admin/
│   │  └── admin_dashboard.html
│   │  └── classification_log.html
│   │  └── edit_log.html
│   │  └── edit_users.html
│   └── baser.html
│   └── index.html
│   └── login.html
│   └── register.html
├── unit_tests/ #Tests for web app
│   └──── test_run_app.py
├── init.py
├── classified_log.csv #log of classifciatyions
├── database.db #SQLite database
├── extensions.py
├── init_db.py #Database initialization
├── run_app.py #Main fie for flask app
├── README.md

````

## Installation

```bash
cd flask_app
python3 -m venv venv
source venv/bin/activate
pip install -r ../app/requirements.txt
```

## How to use

Then open  `http://127.0.0.1:5000/`

### Admin Features

```bash
/ - Home page
/login - Login Page
/register - User registration
/admin - Admin dashboard
/classification_log - Classification log of Emails page
```
