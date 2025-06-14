import pandas as pd
import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv()

# Load your real CSV file
df = pd.read_csv('YFC_gala_guest_list.csv')

print(f"📊 Loaded CSV with {len(df)} rows")
print("Columns:", df.columns.tolist())

# Clean column names (remove extra spaces)
df.columns = df.columns.str.strip()

# Connect to Railway MySQL
conn = mysql.connector.connect(
    host='nozomi.proxy.rlwy.net',
    user='root',
    password=os.environ.get('RLWY_PASS'),
    database='railway',
    port=14254
)

cursor = conn.cursor()

# Drop existing table to start fresh
cursor.execute("DROP TABLE IF EXISTS tickets_to_tables")

# Create updated table structure matching your CSV
cursor.execute("""
CREATE TABLE tickets_to_tables (
    Serial_Number INT,
    Table_Number INT,
    Category VARCHAR(255),
    Name VARCHAR(255),
    Ticket_Number INT,
    PRIMARY KEY (Ticket_Number)
)
""")

print("🗃️ Created fresh table structure")

# Insert all rows from CSV
success_count = 0
error_count = 0

for index, row in df.iterrows():
    try:
        cursor.execute("""
            INSERT INTO tickets_to_tables (Serial_Number, Table_Number, Category, Name, Ticket_Number)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            row['Serial Number'],
            row['Table Number'], 
            row['Category'],
            row['Name'],
            int(row['Ticket Number']) if pd.notna(row['Ticket Number']) else None
        ))
        success_count += 1
    except Exception as e:
        print(f"❌ Error inserting row {index}: {e}")
        print(f"   Row data: {row.to_dict()}")
        error_count += 1

conn.commit()
conn.close()

print(f"✅ Upload complete!")
print(f"   Successfully inserted: {success_count} rows")
print(f"   Errors: {error_count} rows")
print(f"   Total processed: {success_count + error_count} rows")