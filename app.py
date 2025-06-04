from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Adjust with your actual credentials
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Add password if needed
    'database': 'ticket_system'
}

@app.route('/get_table_number', methods=['GET'])
def get_table_number():
    ticket = request.args.get('ticket')

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT Table_Number FROM tickets_to_tables WHERE Ticket_Number = %s", (ticket,))
    result = cursor.fetchone()
    conn.close()

    if result:
        return jsonify({'table_number': result[0]})
    else:
        return jsonify({'error': 'Ticket not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
