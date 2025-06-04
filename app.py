from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

db_config = {
    'host': 'localhost',  # <- change to Railway/PlanetScale later
    'user': 'root',
    'password': '',
    'database': 'ticket_system'
}

@app.route('/get_table_number', methods=['GET'])
def get_table_number():
    try:
        ticket = request.args.get('ticket')
        if not ticket:
            return jsonify({'error': 'Missing ticket parameter'}), 400

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute("SELECT Table_Number FROM tickets_to_tables WHERE Ticket_Number = %s", (ticket,))
        result = cursor.fetchone()

        conn.close()

        if result:
            return jsonify({'table_number': result[0]})
        else:
            return jsonify({'error': 'Ticket not found'}), 404

    except Exception as e:
        print("🔥 Exception:", e)  # This shows up in logs
        return jsonify({'error': 'Server error', 'details': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
