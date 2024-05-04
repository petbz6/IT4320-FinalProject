from flask import Flask, render_template, request, flash, url_for, redirect
import sqlite3
from eticket import generate_e_ticket_number
from FlightChart import flight_chart

app = Flask(__name__)

# Route for main menu
@app.route('/', methods=('GET', 'POST'))
def main_menu():
    error_message=None
    if request.method == 'POST':
        option = request.form.get('option')
        
        if option == 'reservations':
            return redirect(url_for('reservations'))
        elif option == 'admin':
            return redirect(url_for('admin'))
        else:
            error_message = "An option must be selected!"

    return render_template('main_menu.html', error_message=error_message)


# Route for the admin page
@app.route('/admin-panel')
def admin():
    return render_template('admin.html')

# Route for making reservation
@app.route('/reserve', methods=['GET', 'POST'])
def reservations():
    success_message = None
    error_message = None
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        passenger_name = first_name
        seat_row = request.form['seat_row']
        seat_column = request.form['seat_column']
        e_ticket_number = generate_e_ticket_number(first_name)
        
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if the seat row and column combo are already present in the db
        cursor.execute('''SELECT * FROM reservations WHERE seatRow = ? AND seatColumn = ?''', (seat_row, seat_column))
        existing_reservation = cursor.fetchone()
        if existing_reservation:
            error_message = f"Row: {seat_row} Seat: {seat_column} is already assigned. Choose again."
        else:
            # Insert reservation into the database
            cursor.execute('''INSERT INTO reservations (passengerName, seatRow, seatColumn, eTicketNumber)
                              VALUES (?, ?, ?, ?)''', (passenger_name, seat_row, seat_column, e_ticket_number))
            conn.commit()
            success_message = f"Congratulations {first_name}! Row: {seat_row}, Seat: {seat_column} is now reserved for you. Enjoy your trip! Your e-ticket number is: {e_ticket_number}"

        conn.close()

    # Fetch flight chart data
    seat_chart = flight_chart()

    return render_template('reservation.html', success_message=success_message, error_message=error_message, seat_chart=seat_chart)

# Checking admin login
@app.route('/admin', methods=('GET', 'POST'))
def admin_login():
    error_message = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        conn = get_db_connection()
        cursor = conn.cursor()  
        cursor.execute('SELECT * FROM admins WHERE username = ? AND password = ?', (username, password))
        admin = cursor.fetchone()
        conn.close()

        if admin:
            return redirect(url_for('admin_menu'))
        else:
            error_message = 'Invalid username/password combination'
    return render_template('admin.html', error_message=error_message)

# Route for admin menu
@app.route('/admin-menu')
def admin_menu():
    seat_chart = flight_chart()
    total_sales = calculate_total_sales()

    return render_template('admin_menu.html', seat_chart=seat_chart, total_sales=total_sales)

# Cost matrix
def get_cost_matrix():
    cost_matrix = [[100, 75, 50, 100] for row in range(12)]
    return cost_matrix

# Calculate total sales
def calculate_total_sales():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT seatRow, seatColumn FROM reservations')
    reservations = cursor.fetchall()
    conn.close()

    cost_matrix = get_cost_matrix()
    total_sales = 0
    for seat_row, seat_column in reservations:
        seat_row_index = seat_row - 1
        seat_column_index = seat_column - 1

        if 0 <= seat_row_index < len(cost_matrix) and 0 <= seat_column_index < len(cost_matrix[0]):
            total_sales += cost_matrix[seat_row_index][seat_column_index]

    return total_sales


# Establishes a connection to database 'reservations.db'
def get_db_connection():
    conn = sqlite3.connect('reservations.db')
    conn.row_factory = sqlite3.Row
    return conn

# Initializes the database
def init_db():
    with app.app_context():
        conn = get_db_connection()
        cursor = conn.cursor()

        # Create the reservations table if it doesn't exist
        cursor.execute('''CREATE TABLE IF NOT EXISTS reservations (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            passengerName TEXT NOT NULL,
                            seatRow INTEGER NOT NULL,
                            seatColumn INTEGER NOT NULL,
                            eTicketNumber INTEGER NOT NULL
                        )''')

        conn.commit()
        conn.close()

if __name__ == '__main__':
    init_db()
    app.run(debug=True)