# Mental Health Support and Counselling Portal

## Overview
This project is a web-based Mental Health Support and Counselling Portal built with Flask (Python). It provides a safe, anonymous platform for users to access mental health resources, track moods, engage in simulated counselling chats, and reach emergency support. The portal emphasizes privacy, accessibility, and user-friendly design to help bridge gaps in traditional mental health services.

### Problem Statement
Mental health issues affect millions, but barriers like stigma, cost, and limited access hinder timely support. This portal addresses these by offering:
- Anonymous registration and secure access.
- Tools for self-management (e.g., mood tracking, resources).
- Virtual counselling simulation.
- Quick emergency resources.

### Key Features
- **User Authentication**: Secure login/registration with hashed passwords.
- **Dashboard**: Central hub for accessing features.
- **Resource Library**: Curated articles, videos, and exercises on mental health topics.
- **Mood Tracker**: Log daily moods with visualizations using Chart.js.
- **Virtual Counselling Chat**: Simulated real-time chat with a counsellor (AJAX-based; integrate APIs for production).
- **Emergency Page**: Crisis hotlines, calming tips, and disclaimers.
- **Admin Dashboard**: For counsellors to manage users (restricted access).
- **Responsive Design**: Mobile-friendly UI with Bootstrap.

### Technologies Used
- **Backend**: Python, Flask, Flask-Login, Flask-SQLAlchemy, Flask-WTF.
- **Frontend**: HTML, CSS (Bootstrap), JavaScript (Chart.js for charts).
- **Database**: SQLite (for development; upgrade to PostgreSQL for production).
- **Other**: Werkzeug for security, AJAX for chat interactivity.
