from flask import Flask, render_template, request, flash, url_for, redirect
import sqlite3

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = 'your secret key'
app.secret_key = 'your secret key'

# Route for main menu
@app.route('/', methods=('GET', 'POST'))
def main_menu():
    # If page was requested with POST, get form data
    if request.method == 'POST':
        # Get the form data
        option = request.form.get('option')
        # Redirect the user to the appropriate page based on the selection
        if option == 'reservations':
            return redirect(url_for('reservations'))
        elif option == 'admin':
            return redirect(url_for('admin'))
        # If no option is selected, display an error message and remain on the main menu
        else:
            flash("An option must be selected!")

    return render_template('main_menu.html')


# Route for the admin page
@app.route('/admin-panel')
def admin():
    return render_template('admin.html')

# Route for making reservation
@app.route('/reserve', methods=['GET', 'POST'])
def reservations():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        passenger_name = first_name
        seat_row = request.form['seat_row']
        seat_column = request.form['seat_column']
        # Create function for e-ticket generation
        e_ticket_number = 123
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO reservations (passengerName, seatRow, seatColumn, eTicketNumber)
                          VALUES (?, ?, ?, ?)''', (passenger_name, seat_row, seat_column, e_ticket_number))
        conn.commit()
        conn.close()
        
    return render_template('reservation.html')

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
