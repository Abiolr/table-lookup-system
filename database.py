import pandas as pd
import mysql.connector

# Load your Excel file
df = pd.read_excel('/Users/abiolaraji/Downloads/ticket-table-assignments.xlsx')

# Connect to Railway MySQL
conn = mysql.connector.connect(
    host='nozomi.proxy.rlwy.net',
    user='root',
    password='EGLIjTJqpejbrstwenTgAvVyIYAijYnB',
    database='railway',
    port=14254
)

cursor = conn.cursor()

# Create table if it doesn't exist
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
