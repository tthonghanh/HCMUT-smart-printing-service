from flask import *
from config import *
# Create the Flask app with custom static and template paths
app = Flask(
    __name__,
    static_folder='../View',         # Static files root directory
    template_folder='../View/layout'  # Templates directory
)
app.secret_key = 'your_secret_key'


# Routes for HTML templates
@app.route('/')
def home():
    if 'user_logged_in' in session and session['user_logged_in']:
        # If logged in, redirect to the student home page
        return redirect(url_for('student_home_page'))
    # Otherwise, render the home page
    return render_template('home.html')

@app.route('/info-summary')
def info_summary():
    return render_template('info-summary.html')

@app.route('/printing-history')
def printing_history():
    return render_template('printing-history.html')

@app.route('/role-selection', methods=['GET', 'POST'])
def role_selection():
    role = request.args.get('role')  # Get the selected role from the query string
    # print(role)
    if request.method == 'POST' or role:
        # Save the selected role in the session
        session['role'] = role
        return redirect(url_for('sso'))
    return render_template('role-selection.html')

@app.route('/select-printer')
def select_printer():
    return render_template('select-printer.html')

@app.route('/select-printing-property')
def select_printing_property():
    return render_template('select-printing-property.html')

@app.route('/login', methods=['GET', 'POST'])
def sso():
    if "role" not in session:
        return redirect(url_for('role_selection'))
    if request.method == 'POST':
        # Validate user credentials (this is just an example)
        print(request.form)
        username = request.form['username']
        password = request.form['password']
        if session['role'] == 'User':
            if username in STUDENT_ACCOUNT.keys(): 
                if STUDENT_ACCOUNT[username] == password:
                    session['user_logged_in'] = True
                    return redirect(url_for('student_home_page'))
                else:
                    flash('Invalid credentials, please try again!', 'error')
            else:
                flash('Invalid credentials, please try again!', 'error')
        elif session['role'] == 'Admin':
            if username in MANAGER_ACCOUNT.keys(): 
                if MANAGER_ACCOUNT[username] == password:
                    session['user_logged_in'] = True
                    return redirect(url_for('admin_dashboard'))
                else:
                    flash('Invalid credentials, please try again!', 'error')
        else:
            flash('Invalid credentials, please try again!', 'error')
    return render_template('sso.html')

@app.route('/student-home-page')
def student_home_page():
    return render_template('student-home-page.html')

@app.route('/success-request')
def success_request():
    return render_template('success-request.html')

@app.route('/upload')
def upload():
    return render_template('upload.html')

# Serve images from the `View/image` folder
@app.route('/image/<path:filename>')
def serve_image(filename):
    return send_from_directory('../View/image', filename)

# Serve JavaScript from the `View/js` folder
@app.route('/js/<path:filename>')
def serve_js(filename):
    return send_from_directory('../View/js', filename)

# Serve CSS from the `View/style` folder
@app.route('/style/<path:filename>')
def serve_css(filename):
    return send_from_directory('../View/style', filename)

@app.route('/admin-dashboard')
def admin_dashboard():
    return "NOT IMPLEMENTED YET"
@app.route('/dev')
def dev():
    # List of all routes with their paths and names
    routes = [
        {'name': 'Home', 'path': url_for('home')},
        {'name': 'Info Summary', 'path': url_for('info_summary')},
        {'name': 'Printing History', 'path': url_for('printing_history')},
        {'name': 'Role Selection', 'path': url_for('role_selection')},
        {'name': 'Select Printer', 'path': url_for('select_printer')},
        {'name': 'Select Printing Property', 'path': url_for('select_printing_property')},
        {'name': 'SSO', 'path': url_for('sso')},
        {'name': 'Student Home Page', 'path': url_for('student_home_page')},
        {'name': 'Success Request', 'path': url_for('success_request')},
        {'name': 'Upload', 'path': url_for('upload')}
    ]
    return render_template('dev.html', routes=routes)
# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
