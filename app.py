from flask import Flask, render_template

app = Flask(__name__)

# Route for main menu
@app.route('/')
def main_menu():
    return render_template('main_menu.html')

if __name__ == '__main__':
    app.run(debug=True)
