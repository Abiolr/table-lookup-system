import pandas as pd

# Path to the ticket -> table mapping CSV, exported from
# Gala_Guest_Checking_List_formatted.xlsx (Ticket_Table_Lookup sheet).
# Columns: Ticket_Number, Table_Number
CSV_PATH = 'tickets_to_tables.csv'


def load_data(csv_path=CSV_PATH):
    """Load the ticket-to-table mapping CSV into a DataFrame."""
    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip()
    df['Ticket_Number'] = df['Ticket_Number'].astype(int)
    df['Table_Number'] = df['Table_Number'].astype(int)
    return df


def get_table_number(df, ticket_number):
    """Return the table number for a given ticket number, or None if not found."""
    match = df.loc[df['Ticket_Number'] == ticket_number, 'Table_Number']
    return int(match.iloc[0]) if not match.empty else None


def get_table_guests(df, table_number):
    """Return sorted ticket numbers assigned to a given table."""
    tickets = df.loc[df['Table_Number'] == table_number, 'Ticket_Number'].sort_values()
    return tickets.tolist()


def get_all_tables(df):
    """Return ticket counts per table, sorted by table number."""
    counts = df.groupby('Table_Number')['Ticket_Number'].count().sort_index()
    return [{'table_number': int(table), 'guest_count': int(count)} for table, count in counts.items()]


def get_database_stats(df):
    """Return overall stats about the ticket-to-table mapping."""
    return {
        'total_tickets': int(len(df)),
        'total_tables': int(df['Table_Number'].nunique()),
        'ticket_range': {
            'min': int(df['Ticket_Number'].min()),
            'max': int(df['Ticket_Number'].max())
        }
    }


if __name__ == '__main__':
    # Quick sanity check when run directly
    data = load_data()
    print(f"📊 Loaded {len(data)} ticket-to-table mappings from {CSV_PATH}")
    print(get_database_stats(data))
