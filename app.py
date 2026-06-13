from flask import Flask, request, jsonify
import database

app = Flask(__name__)

# Load the ticket -> table mapping once at startup
df = database.load_data()


@app.route('/get_table_number', methods=['GET'])
def get_table_number():
    """Get table number by ticket number"""
    try:
        ticket = request.args.get('ticket')
        if not ticket:
            return jsonify({'error': 'Missing ticket parameter'}), 400

        try:
            ticket_number = int(ticket)
        except ValueError:
            return jsonify({'error': 'Ticket must be a number'}), 400

        table_number = database.get_table_number(df, ticket_number)

        if table_number is not None:
            return jsonify({'table_number': table_number})
        else:
            return jsonify({'error': 'Ticket not found'}), 404

    except Exception as e:
        print("🔥 Exception:", e)
        return jsonify({'error': 'Server error', 'details': str(e)}), 500


@app.route('/get_ticket_details', methods=['GET'])
def get_ticket_details():
    """Get details for a ticket number.

    Note: the current dataset only contains Ticket Number and Table Number,
    so serial_number, category, and name are not available.
    """
    try:
        ticket = request.args.get('ticket')
        if not ticket:
            return jsonify({'error': 'Missing ticket parameter'}), 400

        try:
            ticket_number = int(ticket)
        except ValueError:
            return jsonify({'error': 'Ticket must be a number'}), 400

        table_number = database.get_table_number(df, ticket_number)

        if table_number is not None:
            return jsonify({
                'ticket_number': ticket_number,
                'table_number': table_number
            })
        else:
            return jsonify({'error': 'Ticket not found'}), 404

    except Exception as e:
        print("🔥 Exception:", e)
        return jsonify({'error': 'Server error', 'details': str(e)}), 500


@app.route('/get_table_guests', methods=['GET'])
def get_table_guests():
    """Get all ticket numbers assigned to a specific table"""
    try:
        table = request.args.get('table')
        if not table:
            return jsonify({'error': 'Missing table parameter'}), 400

        try:
            table_number = int(table)
        except ValueError:
            return jsonify({'error': 'Table must be a number'}), 400

        tickets = database.get_table_guests(df, table_number)

        if tickets:
            return jsonify({
                'table_number': table_number,
                'guest_count': len(tickets),
                'ticket_numbers': tickets
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
        tables = database.get_all_tables(df)

        if tables:
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
    """Get overall dataset statistics"""
    try:
        return jsonify(database.get_database_stats(df))

    except Exception as e:
        print("🔥 Exception:", e)
        return jsonify({'error': 'Server error', 'details': str(e)}), 500


@app.route('/search_by_name', methods=['GET'])
def search_by_name():
    """Not available - the current dataset does not include guest names"""
    return jsonify({
        'error': 'Name search is not available',
        'details': 'The current ticket-to-table dataset only contains Ticket Number and Table Number.'
    }), 501


@app.route('/', methods=['GET'])
def home():
    """API documentation endpoint"""
    return jsonify({
        'message': 'NCAC Gala Table Lookup API',
        'endpoints': {
            '/get_table_number?ticket=X': 'Get table number for ticket X',
            '/get_ticket_details?ticket=X': 'Get ticket number and table number for ticket X',
            '/get_table_guests?table=X': 'Get all ticket numbers at table X',
            '/get_all_tables': 'Get summary of all tables',
            '/get_database_stats': 'Get dataset statistics',
            '/search_by_name?name=X': 'Not available in this dataset'
        }
    })


if __name__ == '__main__':
    app.run(debug=True)
