# 🎟️ Table Lookup System

A voice-activated table assignment system using Siri Shortcuts as the user interface and a Flask + MySQL backend. Designed for event organizers, restaurants, or any setting with ticketed seating, this tool allows staff or guests to quickly retrieve their assigned table numbers by simply asking Siri. Once the backend is set up and the database is populated, users can speak their ticket number aloud, and Siri will instantly respond with the corresponding table number—streamlining check-ins and improving guest experience with minimal friction.

## 🧰 Purpose

This project showcases how to:
- Use **Flask** and **MySQL** to build a lightweight API backend.
- Connect Siri Shortcuts with a backend server through HTTP.
- Deploy a **MySQL database using Railway**.
- Speak results back to the user using **Siri's text-to-speech** functionality.
- Provide comprehensive event management endpoints for organizers.

## 🔧 Features

- 🎤 Siri Shortcut Integration
- 🐍 Flask API for ticket queries
- 🗃️ MySQL DB deployed with Railway
- 🌐 Hosted backend on Render with HTTPS
- 🔒 Error handling and secure routing
- 📊 Complete event management API with multiple endpoints
- 🔍 Search functionality by name and ticket
- 📋 Table management and guest listing
- 📈 Database statistics and analytics

## 🧠 How It Works

1. User says to Siri:  
   **"What is the table number for ticket number 123?"**

2. Shortcut sends a request to:  
   `https://ticket-system-h7px.onrender.com/get_table_number?ticket=123`

3. Flask queries your Railway-hosted MySQL DB:
   ```sql
   SELECT table_number FROM tickets_to_tables WHERE ticket_number = 123;
   ```

4. The response is parsed and Siri speaks:
   - ✅ Success: "For ticket number 123, your assigned table number is 16."
   - ❌ Failure: "Ticket number 123 not found."

## 🧩 Tech Stack

- **Backend**: Python (Flask)
- **DB**: MySQL on Railway
- **Deployment**: [Render](https://render.com)
- **Voice Assistant**: Apple Shortcuts + Siri
- **Data Processing**: Pandas for CSV import

## 🗃️ Database Schema

```sql
CREATE TABLE tickets_to_tables (
    Serial_Number INT,
    Table_Number INT,
    Category VARCHAR(255),
    Name VARCHAR(255),
    Ticket_Number INT,
    PRIMARY KEY (Ticket_Number)
);
```

## 🚀 API Endpoints

The system now provides a comprehensive REST API for event management:

### Core Endpoints

| Endpoint | Method | Description | Parameters |
|----------|--------|-------------|------------|
| `/` | GET | API documentation and available endpoints | None |
| `/get_table_number` | GET | Get table number for a specific ticket | `ticket` (required) |
| `/get_ticket_details` | GET | Get complete ticket information | `ticket` (required) |

### Table Management

| Endpoint | Method | Description | Parameters |
|----------|--------|-------------|------------|
| `/get_table_guests` | GET | Get all guests assigned to a table | `table` (required) |
| `/get_all_tables` | GET | Get summary of all tables with guest counts | None |

### Search & Analytics

| Endpoint | Method | Description | Parameters |
|----------|--------|-------------|------------|
| `/search_by_name` | GET | Search for guests by name (partial match) | `name` (required) |
| `/get_database_stats` | GET | Get database statistics and analytics | None |

### Example API Responses

**Get Table Number:**
```json
{
  "table_number": 16
}
```

**Get Ticket Details:**
```json
{
  "serial_number": 1,
  "table_number": 16,
  "category": "VIP",
  "name": "John Doe",
  "ticket_number": 123
}
```

**Get Table Guests:**
```json
{
  "table_number": 16,
  "guest_count": 8,
  "guests": [
    {
      "serial_number": 1,
      "table_number": 16,
      "category": "VIP",
      "name": "John Doe",
      "ticket_number": 123
    }
  ]
}
```

**Search by Name:**
```json
{
  "search_term": "John",
  "match_count": 2,
  "matches": [
    {
      "serial_number": 1,
      "table_number": 16,
      "category": "VIP",
      "name": "John Doe",
      "ticket_number": 123
    }
  ]
}
```

**Database Statistics:**
```json
{
  "total_tickets": 150,
  "total_tables": 20,
  "ticket_range": {
    "min": 1,
    "max": 150
  },
  "categories": [
    {
      "category": "VIP",
      "count": 40
    },
    {
      "category": "General",
      "count": 110
    }
  ]
}
```

## 🛠️ Setup Instructions

### 1. Backend (Flask)

Install dependencies:

```bash
pip install -r requirements.txt
```

Run locally:

```bash
gunicorn app:app
```

### 2. Database Setup

1. Prepare your guest list CSV with columns:
   - `Serial Number`
   - `Table Number`
   - `Category`
   - `Name`
   - `Ticket Number`

2. Run the database import script:
```bash
python database.py
```

### 3. Deployment

Deploy to Render with the provided `render.yaml`:

```yaml
services:
  - type: web
    name: ticket-api
    env: python
    startCommand: gunicorn app:app
```

Set environment variables for MySQL credentials when deploying.

### 4. Shortcut Setup

1. **Ask for Input** (Number)  
   Prompt: "What is the ticket number?"

2. **Get Contents of URL**  
   URL: `https://ticket-system-h7px.onrender.com/get_table_number?ticket=[TicketNumber]`

3. **Get Dictionary Value**  
   Key: `table_number`

4. **Speak Result**  
   - ✅ If found: "For ticket number X, your assigned table number is Y."
   - ❌ If not found: "Ticket number X not found."

## 🔐 Environment Variables

This project uses environment variables to securely manage sensitive MySQL credentials and prevent hardcoding secrets in source files. You'll need to set the following variables in your deployment platform (e.g. Render or Railway):

| Variable Name     | Description                      |
|-------------------|----------------------------------|
| `RLWY_PASS`       | Railway MySQL password          |

**Example configuration:**
```python
db_config = {
    'host': 'nozomi.proxy.rlwy.net',
    'user': 'root',
    'password': os.environ.get('RLWY_PASS'),
    'database': 'railway',
    'port': 14254
}
```

If testing locally, you can create a `.env` file and load it with `python-dotenv`:

```bash
RLWY_PASS=your_railway_password
```

## 🎯 Use Cases

### For Event Organizers
- **Guest Check-in**: Quickly verify table assignments during registration
- **Table Management**: View guest lists for specific tables
- **Search Functionality**: Find guests by name for special requests
- **Analytics**: Monitor guest distribution and categories

### For Staff
- **Voice Lookup**: Use Siri shortcuts for hands-free table lookups
- **Quick Search**: Find guest information without accessing backend systems
- **Table Planning**: View complete table assignments and guest counts

### For Guests
- **Self-Service**: Use voice commands to find their table assignment
- **Quick Access**: Get table information without waiting in line

## 🖼️ Screenshots

![Untitled design (1)](https://github.com/user-attachments/assets/26d86759-cbf5-45d3-bdf2-83655ccc704a)

<img width="634" alt="Screenshot 2025-06-04 at 3 39 50 PM" src="https://github.com/user-attachments/assets/f0952530-fe49-4bc9-8e1d-92daf29c0ffb" />

## 📦 Project Structure

| File              | Purpose                            |
|-------------------|------------------------------------|
| `app.py`          | Main Flask app with all API endpoints |
| `database.py`     | CSV import script and DB setup utility |
| `render.yaml`     | Render deployment configuration    |
| `requirements.txt`| Python dependencies for deployment |
| `.gitignore`      | Git ignore file (excludes .env)   |

## 🚀 Getting Started

1. **Clone the repository**
2. **Set up your CSV file** with guest data
3. **Configure environment variables** for Railway database
4. **Run database import**: `python database.py`
5. **Test locally**: `gunicorn app:app`
6. **Deploy to Render** using the provided configuration
7. **Set up Siri Shortcuts** for voice interaction

## 🔄 API Testing

You can test all endpoints using curl or any HTTP client:

```bash
# Get table number
curl "https://ticket-system-h7px.onrender.com/get_table_number?ticket=123"

# Search by name
curl "https://ticket-system-h7px.onrender.com/search_by_name?name=John"

# Get database stats
curl "https://ticket-system-h7px.onrender.com/get_database_stats"
```