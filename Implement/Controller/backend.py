from flask import *
from config import *
import os
import PyPDF2
import docx2pdf
import json
import ast
# Create the Flask app with custom static and template paths
app = Flask(
    __name__,
    static_folder='../View',         # Static files root directory
    template_folder='../View/layout'  # Templates directory
)
app.secret_key = 'your_secret_key'

app.config["UPLOAD_FOLDER"] = "uploaded_files"
if os.path.exists(app.config["UPLOAD_FOLDER"]):
    # If the upload folder exists, remove all files in it
    for file in os.listdir(app.config["UPLOAD_FOLDER"]):
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], file)
        if os.path.isfile(file_path):
            os.remove(file_path)
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
# Routes for HTML templates
@app.route('/')
def home():
    if 'user_logged_in' in session and session['user_logged_in']:
        # If logged in, redirect to the student home page
        return redirect(url_for('student_home_page'))
    # Otherwise, render the home page
    return render_template('home.html')

@app.route('/info-summary', methods=['GET', 'POST'])
def info_summary():
    config={}
    if request.method == 'GET':
        config = request.args.get('config')
        config = json.loads(config)
        print(config)
    return render_template('info-summary.html',config=config)

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

@app.route('/select-printer', methods=['GET', 'POST'])
def select_printer():
    config={}
    if request.method == 'GET':
        config = request.args.get('config')
        config = json.loads(config)  # Convert the JSON string to a dictionary
        # print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA", config)
    # config = {}
    elif request.method == 'POST':
        config                    = ast.literal_eval(request.form.get('config'))
        printer, printer_location = request.form.get('printer').split(';')
        # print(type(config),printer,printer_location)
        config['printer'] = printer
        config['printer_location'] = printer_location
        
        return redirect(url_for('info_summary', config=json.dumps(config)))
    return render_template('select-printer.html',config=config)

def get_file_pages(config):
    # Read the PDF file and get the number of pages
    if config['file_type'] == 'pdf':
        pdf_file = open(os.path.join(app.config['UPLOAD_FOLDER'],config['file_to_print']), 'rb')
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        num_pages = len(pdf_reader.pages)
    elif config['file_type'] == 'docx':
        doc_file = open(os.path.join(app.config['UPLOAD_FOLDER'],config['file_to_print']), 'rb')
        doc_file = docx2pdf.convert(config['file_to_print'], f"{config['file_type'].split('.')[0]}.pdf")
        pdf_reader = PyPDF2.PdfReader(doc_file)
        if os.path.exists(f"{config['file_type'].split('.')[0]}.pdf"):
            os.remove(f"{config['file_type'].split('.')[0]}.pdf")
        num_pages = len(pdf_reader.pages)

    return num_pages
@app.route('/select-printing-property', methods=['GET', 'POST'])
def select_printing_property():
    # If the form is submitted
    config = {}
    file_to_print=None
    if request.method == 'GET':
        try:
            file_to_print = request.args.get('file_to_print')  # The file path passed from upload
        except:
            file_to_print = request.form.get('file_to_print') # The file
        print(file_to_print)
        config['file_to_print'] = os.path.basename(file_to_print)
        config['file_name']     = ".".join(config['file_to_print'].split('.')[:-1])
        config['file_type']     = config['file_to_print'].split('.')[-1]
        config['num_pages']     = get_file_pages(config)
        config['file_size']     =  os.path.getsize(file_to_print)
    else:
        config['file_to_print'] = request.form.get('file_to_print')
        config['file_name']     = request.form.get('file_name')
        config['file_type']     = request.form.get('file_type')
        config['num_pages']     = request.form.get('num_pages')
        config['file_size']     = request.form.get('file_size')
        print(config)
    if request.method == 'POST':
        # Get the values from the form
        print(request.form)
        try:
            copies = request.form.get('copies')  # Number of copies to print
            paper_type = request.form.get('paper_type')  # Selected paper type
            sides = request.form.get('sides')  # Number of sides (single/double)

            # Validate input
            # if not config['file_to_print']:
            #     flash('No file selected for printing', 'error')
            #     print("WHAT")
            #     return redirect(url_for('select_printing_property', config=config))

            # Store the configuration settings in the dictionary
            config['copies'] = copies
            config['paper_type'] = paper_type
            config['sides'] = sides

            # Flash a success message and redirect to a confirmation page (or the next step)
            flash('Printing settings configured successfully!', 'success')
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
            print('Error: ', e)
            return redirect(url_for('select_printing_property', config=config))
        # Redirect to a page where printing or further processing can occur
        return redirect(url_for('select_printer', config=json.dumps(config)))
    return render_template('select-printing-property.html', config=config)
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

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        # Check if a file is in the request
        if 'uploaded-file' not in request.files:
            flash('No file part', 'error')
            return render_template('upload.html')
        # Get the file
        files = request.files.getlist('uploaded-file')
        print(files)
        if not files:
            flash('No selected files', 'error')
            return render_template('upload.html')
        
        for file in files:
            if file.filename == '':
                flash('No selected file', 'error')
                return render_template('upload.html')
            # Save the file
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            flash(f'File "{file.filename}" uploaded successfully!', 'success')
        
        return redirect(url_for('select_printing_property', file_to_print=file_path))  # Redirect after upload
    
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
    return render_template('admin-dashboard.html')

@app.route('/account-info')
def account_info():
    return "NOT IMPLEMENTED YET"

@app.route('/payment-history')
def payment_history():
    return render_template('payment-history.html')

@app.route('/buy-pages', methods=['GET', 'POST'])
def buy_pages():
    return render_template('select-number-of-pages.html')
@app.route('/logout')
def logout():
    # Clear the session
    session.clear()
    # Redirect to the home page
    return redirect(url_for('home'))
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
        {'name': 'Upload', 'path': url_for('upload')},
        {'name': 'Admin Dashboard', 'path': url_for('admin_dashboard')},

    ]
    return render_template('dev.html', routes=routes)
# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
