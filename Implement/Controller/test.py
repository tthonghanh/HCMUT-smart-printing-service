from flask import *
from flask.views import MethodView
import os
import PyPDF2
import docx2pdf
import json
import ast
from config import *
from classes import *
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

# Method View Classes

class HomePage(MethodView):
    def get(self):
        if 'user_logged_in' in session and session['user_logged_in']:
            if session['role'] == 'User':
                return redirect(url_for('student_home_page'))
            else:
                return redirect(url_for('admin_dashboard'))
        return render_template('home.html')

class InfoSummary(MethodView):
    def get(self):
        config = request.args.get('config')
        config = json.loads(config) if config else {}
        return render_template('info-summary.html', config=config)
    
    def post(self):
        config = request.form.get('config')
        if not config:
            config = request.form.get('config')
        print(config)
        config = ast.literal_eval(config)

        return redirect(url_for('success_request', config=json.dumps(config)))

class PrintingHistory(MethodView):
    def get(self):
        return render_template('printing-history.html')

class RoleSelection(MethodView):
    def get(self):
        role = request.args.get('role')
        if role:
            session['role'] = role
            return redirect(url_for('sso'))
        return render_template('role-selection.html')


class SelectPrinter(MethodView):
    def get(self):
        config = request.args.get('config')
        config = json.loads(config) if config else {}
        return render_template('select-printer.html', config=config)

    def post(self):
        config = ast.literal_eval(request.form.get('config'))
        printer, printer_location = request.form.get('printer').split(';')
        config['printer'] = printer
        config['printer_location'] = printer_location
        return redirect(url_for('info_summary', config=json.dumps(config)))

class SelectPrintingProperty(MethodView):
    def get(self):
        try:
            file_to_print = request.args.get('file_to_print')
        except:
            file_to_print = request.form.get('file_to_print')
        
        file = File(file_to_print)
        config = {
            'file_to_print': file_to_print,
            'file_name': '.'.join(os.path.basename(file_to_print).split('.')[:-1]),
            'file_type': file_to_print.split('.')[-1],
            'num_pages': file.get_pages(),
            'file_size': file.get_size()
        }

        return render_template('select-printing-property.html', config=config)

    def post(self):
        config = {
            'file_to_print': request.form.get('file_to_print'),
            'file_name': request.form.get('file_name'),
            'file_type': request.form.get('file_type'),
            'num_pages': request.form.get('num_pages'),
            'file_size': request.form.get('file_size'),
            'copies': request.form.get('copies'),
            'paper_type': request.form.get('paper_type'),
            'sides': request.form.get('sides')
        }
        flash('Printing settings configured successfully!', 'success')
        return redirect(url_for('select_printer', config=json.dumps(config)))

    
class SSO(MethodView):
    def get(self):
        if "role" not in session:
            return redirect(url_for('role_selection'))
        return render_template('sso.html')

    def post(self):
        username = request.form['username']
        password = request.form['password']
        print(session)
        if session['role'] == 'User':
            user = StudentAccount(username=username, password=password)
        elif session['role'] == 'Admin':
            user = AdminAccount(username=username, password=password)
        

        if user.authenticate():
            flash(f'Welcome {username}!', 'success')
            return redirect(url_for('student_home_page') if session['role'] == 'User' else url_for('admin_dashboard'))
        else:
            flash('Invalid credentials/role, please try again!', 'error')
        return redirect(url_for('sso'))

class Upload(MethodView):
    def get(self):
        return render_template('upload.html')

    def post(self):
        if 'uploaded-file' not in request.files:
            flash('No file part', 'error')
            return render_template('upload.html')
        files = request.files.getlist('uploaded-file')
        if not files:
            flash('No selected files', 'error')
            return render_template('upload.html')
        print(files)
        for file in files:
            if file.filename == '':
                flash('No selected file', 'error')
                return render_template('upload.html')
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            flash(f'File "{file.filename}" uploaded successfully!', 'success')

        return redirect(url_for('select_printing_property', file_to_print=file_path))

class StudentHomePage(MethodView):
    def get(self):
        return render_template('student-home-page.html')

class SuccessRequest(MethodView):
    def get(self):
        ## Simulating send request to printers 
        config = json.loads(request.args.get('config')) if request.args.get('config') else None
        if config:
            printing_properties = Config()
            printing_properties.setAttributes(config)

            printer_name     = printing_properties.get('printer')
            printer_location = printing_properties.get('printer_location')
            
            # This code block simulate sending request to printer and print
            printer       = Printer(printer_name, printer_location, printing_properties)
            print(config)
            file_to_print = File(config['file_to_print'])

            printer.print_file(file_to_print)
            flash(f'Printing request sent to {printer_name} at {printer_location}', 'info')
        return render_template('success-request.html')

class AdminDashboard(MethodView):
    def get(self):
        return render_template('admin-dashboard.html')

class PaymentHistory(MethodView):
    def get(self):
        return render_template('payment-history.html')

class BuyPages(MethodView):
    def get(self):
        return render_template('select-number-of-page.html')
    
    def post(self):
        num_pages = request.form.get('quantity')
        return redirect(url_for('success_payment', num_pages=num_pages))

class SuccessPaymentView(MethodView):
    def get(self):
        # You can add more logic to process payment info here if necessary
        num_pages = request.args.get('num_pages')
        flash(f'You bought {num_pages} pages.', 'info')
        return render_template('success-payment.html', quantity=num_pages, total_price=int(num_pages)*200)
class Logout(MethodView):
    def get(self):
        session.clear()
        return redirect(url_for('home'))

class Dev(MethodView):
    def get(self):
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

# Register class-based views with Flask
app.add_url_rule('/', view_func=HomePage.as_view('home'))
app.add_url_rule('/info-summary', view_func=InfoSummary.as_view('info_summary'))
app.add_url_rule('/printing-history', view_func=PrintingHistory.as_view('printing_history'))
app.add_url_rule('/role-selection', view_func=RoleSelection.as_view('role_selection'))
app.add_url_rule('/select-printer', view_func=SelectPrinter.as_view('select_printer'))
app.add_url_rule('/select-printing-property', view_func=SelectPrintingProperty.as_view('select_printing_property'))
app.add_url_rule('/login', view_func=SSO.as_view('sso'))
app.add_url_rule('/upload', view_func=Upload.as_view('upload'))
app.add_url_rule('/student-home-page', view_func=StudentHomePage.as_view('student_home_page'))
app.add_url_rule('/success-request', view_func=SuccessRequest.as_view('success_request'))
app.add_url_rule('/admin-dashboard', view_func=AdminDashboard.as_view('admin_dashboard'))
app.add_url_rule('/payment-history', view_func=PaymentHistory.as_view('payment_history'))
app.add_url_rule('/buy-pages', view_func=BuyPages.as_view('buy_pages'))
app.add_url_rule('/logout', view_func=Logout.as_view('logout'))
app.add_url_rule('/dev', view_func=Dev.as_view('dev'))
app.add_url_rule('/payment-success', view_func=SuccessPaymentView.as_view('success_payment'))

@app.route('/account-info')
def account_info():
    return "Not implemented"

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
# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
