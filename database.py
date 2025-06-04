import pandas as pd
import mysql.connector

# Load your CSV
df = pd.read_csv('/Users/abiolaraji/Downloads/ticket-table-assignment.csv')

# Connect to MySQL
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',  # Replace if needed
    database='ticket_system'  # Replace with your DB name
)

cursor = conn.cursor()

# Create table (only run once)
cursor.execute("""
CREATE TABLE IF NOT EXISTS tickets_to_tables (
    Name VARCHAR(100),
    Email VARCHAR(100),
    Ticket_Number INT,
    Table_Number INT
)
""")

# Insert rows
for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO tickets_to_tables (Name, Email, Ticket_Number, Table_Number)
        VALUES (%s, %s, %s, %s)
    """, tuple(row))

conn.commit()
conn.close()
