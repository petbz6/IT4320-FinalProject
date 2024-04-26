from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Route for main menu
@app.route('/')
def main_menu():
    return render_template('main_menu.html')


# Connect to database
def connect_db():
    return sqlite3.connect('reservations.db')

# Route for admin menu
@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    error_message = None
    if request.method == 'POST':
        admin_username = request.form['admin-username']
        admin_password = request.form['admin-password']
        
        conn = connect_db()
        cursor = conn.cursor()  
        cursor.execute('SELECT * FROM admins WHERE username = ? AND password = ?', (admin_username, admin_password))
        admin = cursor.fetchone()
        conn.close()

        if admin:
            return redirect(url_for('admin_menu')) # may have to change this depending on what the admin menu gets named
        else:
            error_message = 'Invalid username/password combination'
    return render_template('admin_login.html', error_message=error_message)


if __name__ == '__main__':
    app.run(debug=True)
