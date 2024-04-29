@app.route('/flight_chart')
def flight_chart():
    # Initialize a 12x4 matrix to represent seat availability
    # '0' represents available seat, '1' represents booked seat
    seat_chart = [[0 for _ in range(4)] for _ in range(12)]
    
    # Connect to the database and fetch booked seats
    conn = connect_db()
    cursor = conn.execute('SELECT seat_row, seat_column FROM reservations')
    for row in cursor:
        row_index = row['seat_row'] - 1
        col_index = row['seat_column'] - 1
        seat_chart[row_index][col_index] = 1
    conn.close()
    
    return render_template('flight_chart.html', seat_chart=seat_chart)
