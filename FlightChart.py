import sqlite3

def flight_chart():
    seat_chart = [[0 for _ in range(4)] for _ in range(12)]

    conn = get_db_connection()
    cursor = conn.execute('SELECT seatRow, seatColumn FROM reservations')
    for row in cursor:
        row_index = row[0] - 1
        col_index = row[1] - 1
        seat_chart[row_index][col_index] = 1
    conn.close()

    return seat_chart

def get_db_connection():
    conn = sqlite3.connect('reservations.db')
    conn.row_factory = sqlite3.Row
    return conn
