# Table Lookup System

A voice-activated table assignment system using Siri Shortcuts as the user interface and a React frontend, both integrated with a Flask/MySQL backend. Designed for event organizers, restaurants, or any setting with ticketed seating, this tool allows staff or guests to quickly retrieve their assigned table numbers by simply asking Siri. Once the backend is set up and the database is populated, users can speak their ticket number aloud, and Siri will instantly respond with the corresponding table number—streamlining check-ins and improving guest experience with minimal friction.

---

## Real-World Impact

This system was deployed as a freelance project for live events in Calgary, AB, serving **600+ and 1,000+ attendees** respectively. Working directly with event organizers, requirements were gathered, testing was conducted on-site, and the system performed seamlessly under real event conditions. The backend architecture was designed for reusability and was successfully refined and redeployed across multiple events, demonstrating scalability and maintainability in a production environment.

---

## Purpose

This project showcases how to:
- Use **Flask** and **MySQL** to build a lightweight API backend.
- Connect Siri Shortcuts with a backend server through HTTP.
- Build a **React frontend** for event organizer use.
- Deploy a **MySQL database using Railway**.
- Speak results back to the user using **Siri's text-to-speech** functionality.

## Features

- Siri Shortcut Integration
- React Frontend for event organizers
- Flask API for ticket queries
- MySQL DB deployed with Railway
- Hosted backend on Render with HTTPS
- Error handling and secure routing

## How It Works

1. User says to Siri:  
   **"What is the table number for ticket number 123?"**

2. Shortcut sends a request to:  
   `https://ticket-system-h7px.onrender.com/get_table_number?ticket=123`

3. Flask queries your Railway-hosted MySQL DB:
   ```sql
   SELECT table_number FROM tickets_to_tables WHERE ticket_number = 123;
   ```

4. The response is parsed and Siri speaks:
   - Success: "For ticket number 123, your assigned table number is 16."
   - Failure: "Ticket number 123 not found."

## Tech Stack

- **Frontend**: React
- **Backend**: Python (Flask)
- **DB**: MySQL on Railway
- **Deployment**: [Render](https://render.com)
- **Voice Assistant**: Apple Shortcuts + Siri

## Table Schema

```sql
CREATE TABLE tickets_to_tables (
    Name VARCHAR(100),
    Email VARCHAR(100),
    Ticket_Number INT,
    Table_Number INT
);
```

## Setup Instructions

### 1. Backend (Flask)

Install dependencies:

```bash
pip install -r requirements.txt
```

Run locally:

```bash
gunicorn app:app
```

### 2. Deployment

Deploy to Render with the provided `render.yaml`:

```yaml
services:
  - type: web
    name: ticket-api
    env: python
    startCommand: gunicorn app:app
```

Set environment variables for MySQL credentials when deploying.

### 3. Shortcut Setup

1. **Ask for Input** (Number)  
   Prompt: "What is the ticket number?"

2. **Get Contents of URL**  
   URL: `https://ticket-system-h7px.onrender.com/get_table_number?ticket=[TicketNumber]`

3. **Get Dictionary Value**  
   Key: `table_number`

4. **Speak Result**  
   - If found: "For ticket number X, your assigned table number is Y."
   - If not found: "Ticket number X not found."


### Environment Variables

This project uses environment variables to securely manage sensitive MySQL credentials and prevent hardcoding secrets in source files. You'll need to set the following variables in your deployment platform (e.g. Render or Railway):

| Variable Name     | Description                      |
|-------------------|----------------------------------|
| `DB_HOST`         | The hostname of your MySQL server |
| `DB_USER`         | Your MySQL username               |
| `DB_PASSWORD`     | Your MySQL password               |
| `DB_NAME`         | Name of the database              |
| `DB_PORT`         | MySQL port number (e.g., `3306`)  |

**Example in Python (`database.py`):**
```python
import os
import mysql.connector

conn = mysql.connector.connect(
    host=os.environ.get("DB_HOST"),
    user=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASSWORD"),
    database=os.environ.get("DB_NAME"),
    port=int(os.environ.get("DB_PORT", 3306))
)
```

If testing locally, you can create a `.env` file and load it with `python-dotenv`:

```bash
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=yourpassword
DB_NAME=ticketdb
DB_PORT=3306
```

## Screenshots

![Untitled design (1)](https://github.com/user-attachments/assets/26d86759-cbf5-45d3-bdf2-83655ccc704a)

<img width="634" alt="Screenshot 2025-06-04 at 3 39 50 PM" src="https://github.com/user-attachments/assets/f0952530-fe49-4bc9-8e1d-92daf29c0ffb" />


## Files

| File              | Purpose                            |
|-------------------|------------------------------------|
| `app.py`          | Main Flask app and route logic     |
| `database.py`     | DB connection utility              |
| `render.yaml`     | Render deployment config           |
| `requirements.txt`| Dependencies list for deployment   |
