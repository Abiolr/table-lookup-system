from flask import Flask, request, jsonify
import mysql.connector
import os

app = Flask(__name__)

db_config = {
    'host': 'nozomi.proxy.rlwy.net',
    'user': 'root',
    'password': os.environ.get('RLWY_PASS'),
    'database': 'railway',
    'port': 14254
}

def get_db_connection():
    """Helper function to get database connection"""
    return mysql.connector.connect(**db_config)

@app.route('/get_table_number', methods=['GET'])
def get_table_number():
    """Original endpoint - get table number by ticket number"""
    try:
        ticket = request.args.get('ticket')
        if not ticket:
            return jsonify({'error': 'Missing ticket parameter'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT Table_Number FROM tickets_to_tables WHERE Ticket_Number = %s", (ticket,))
        result = cursor.fetchone()

        conn.close()

        if result:
            return jsonify({'table_number': result[0]})
        else:
            return jsonify({'error': 'Ticket not found'}), 404

    except Exception as e:
        print("🔥 Exception:", e)
        return jsonify({'error': 'Server error', 'details': str(e)}), 500

@app.route('/get_ticket_details', methods=['GET'])
def get_ticket_details():
    """Get complete ticket details by ticket number"""
    try:
        ticket = request.args.get('ticket')
        if not ticket:
            return jsonify({'error': 'Missing ticket parameter'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT Serial_Number, Table_Number, Category, Name, Ticket_Number 
            FROM tickets_to_tables 
            WHERE Ticket_Number = %s
        """, (ticket,))
        result = cursor.fetchone()

        conn.close()

        if result:
            return jsonify({
                'serial_number': result[0],
                'table_number': result[1],
                'category': result[2],
                'name': result[3],
                'ticket_number': result[4]
            })
        else:
            return jsonify({'error': 'Ticket not found'}), 404

    except Exception as e:
        print("🔥 Exception:", e)
        return jsonify({'error': 'Server error', 'details': str(e)}), 500

@app.route('/get_table_guests', methods=['GET'])
def get_table_guests():
    """Get all guests assigned to a specific table"""
    try:
        table = request.args.get('table')
        if not table:
            return jsonify({'error': 'Missing table parameter'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT Serial_Number, Table_Number, Category, Name, Ticket_Number 
            FROM tickets_to_tables 
            WHERE Table_Number = %s
            ORDER BY Ticket_Number
        """, (table,))
        results = cursor.fetchall()

        conn.close()

        if results:
            guests = []
            for row in results:
                guests.append({
                    'serial_number': row[0],
                    'table_number': row[1],
                    'category': row[2],
                    'name': row[3],
                    'ticket_number': row[4]
                })
            return jsonify({
                'table_number': int(table),
                'guest_count': len(guests),
                'guests': guests
            })
        else:
            return jsonify({'error': 'No guests found for this table'}), 404

    except Exception as e:
        print("🔥 Exception:", e)
        return jsonify({'error': 'Server error', 'details': str(e)}), 500

@app.route('/get_all_tables', methods=['GET'])
def get_all_tables():
    """Get summary of all tables with guest counts"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT Table_Number, COUNT(*) as guest_count, 
                   GROUP_CONCAT(DISTINCT Category SEPARATOR ', ') as categories
            FROM tickets_to_tables 
            GROUP BY Table_Number 
            ORDER BY Table_Number
        """)
        results = cursor.fetchall()

        conn.close()

        if results:
            tables = []
            for row in results:
                tables.append({
                    'table_number': row[0],
                    'guest_count': row[1],
                    'categories': row[2]
                })
            return jsonify({
                'total_tables': len(tables),
                'tables': tables
            })
        else:
            return jsonify({'error': 'No tables found'}), 404

    except Exception as e:
        print("🔥 Exception:", e)
        return jsonify({'error': 'Server error', 'details': str(e)}), 500

@app.route('/get_database_stats', methods=['GET'])
def get_database_stats():
    """Get overall database statistics"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Get total records
        cursor.execute("SELECT COUNT(*) FROM tickets_to_tables")
        total_tickets = cursor.fetchone()[0]

        # Get table count
        cursor.execute("SELECT COUNT(DISTINCT Table_Number) FROM tickets_to_tables")
        total_tables = cursor.fetchone()[0]

        # Get category breakdown
        cursor.execute("""
            SELECT Category, COUNT(*) as count 
            FROM tickets_to_tables 
            GROUP BY Category 
            ORDER BY count DESC
        """)
        category_results = cursor.fetchall()

        # Get ticket number range
        cursor.execute("SELECT MIN(Ticket_Number), MAX(Ticket_Number) FROM tickets_to_tables")
        ticket_range = cursor.fetchone()

        conn.close()

        categories = []
        for row in category_results:
            categories.append({
                'category': row[0],
                'count': row[1]
            })

        return jsonify({
            'total_tickets': total_tickets,
            'total_tables': total_tables,
            'ticket_range': {
                'min': ticket_range[0],
                'max': ticket_range[1]
            },
            'categories': categories
        })

    except Exception as e:
        print("🔥 Exception:", e)
        return jsonify({'error': 'Server error', 'details': str(e)}), 500

@app.route('/search_by_name', methods=['GET'])
def search_by_name():
    """Search for tickets by guest name (partial match)"""
    try:
        name = request.args.get('name')
        if not name:
            return jsonify({'error': 'Missing name parameter'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT Serial_Number, Table_Number, Category, Name, Ticket_Number 
            FROM tickets_to_tables 
            WHERE Name LIKE %s
            ORDER BY Name
        """, (f'%{name}%',))
        results = cursor.fetchall()

        conn.close()

        if results:
            matches = []
            for row in results:
                matches.append({
                    'serial_number': row[0],
                    'table_number': row[1],
                    'category': row[2],
                    'name': row[3],
                    'ticket_number': row[4]
                })
            return jsonify({
                'search_term': name,
                'match_count': len(matches),
                'matches': matches
            })
        else:
            return jsonify({'error': f'No guests found matching "{name}"'}), 404

    except Exception as e:
        print("🔥 Exception:", e)
        return jsonify({'error': 'Server error', 'details': str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    """API documentation endpoint"""
    return jsonify({
        'message': 'YFC Gala Table Lookup API',
        'endpoints': {
            '/get_table_number?ticket=X': 'Get table number for ticket X',
            '/get_ticket_details?ticket=X': 'Get complete details for ticket X',
            '/get_table_guests?table=X': 'Get all guests at table X',
            '/get_all_tables': 'Get summary of all tables',
            '/get_database_stats': 'Get database statistics',
            '/search_by_name?name=X': 'Search for guests by name'
        }
    })

if __name__ == '__main__':
    app.run(debug=True)