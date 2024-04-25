from flask import Flask, render_template, request, flash, url_for, redirect

#create a flask app object and set app variables
app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SECRECT_KEY"] = 'your secret key'
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

# Route for the reservations page
@app.route('/reservations')
def reservations():

    return render_template('reservation.html')
if __name__ == '__main__':
    app.run(debug=True)
