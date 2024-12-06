# Define the classes in a separate module

import os
import PyPDF2
import docx2pdf
import json
from config import *
class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role    
    def authenticate(self):
        raise NotImplementedError("This method should be overridden in subclasses")

class StudentAccount(User):
    def __init__(self, username=None, password=None, config=None,role='Student'):
        if config:
            self.from_json(config)
            self.role = role
        else:
            super().__init__(username, password, role)
            if username in USER_CONFIG.keys():
                self.config = USER_CONFIG[username]
    def authenticate(self):
        from config import STUDENT_ACCOUNT
        return self.username in STUDENT_ACCOUNT and STUDENT_ACCOUNT[self.username] == self.password

    def view_files(self):
        # Functionality for viewing files accessible by students
        return "Student is viewing accessible files."

    def submit_print_request(self, file):
        # Placeholder for submitting a print request
        return f"Print request submitted for file: {file.file_name}"
    def to_json(self):
        return json.dumps({
            'username': self.username,
            'password': self.password,
            'config': self.config
        })
    def from_json(self, json_data):
        data = json.loads(json_data)
        self.username = data['username']
        self.password = data['password']
        self.config = data['config']
class AdminAccount(User):
    def __init__(self, username, password, role='Admin'):
        super().__init__(username, password, role)
    def authenticate(self):
        from config import MANAGER_ACCOUNT
        return self.username in MANAGER_ACCOUNT and MANAGER_ACCOUNT[self.username] == self.password

    def manage_printers(self):
        # Functionality for managing printers
        # Out of this module scope 
        return "Admin is managing printers."

class File:
    def __init__(self, file_path):
        self.file_path = file_path
        self.file_name = os.path.basename(file_path)
        self.file_type = self.file_name.split('.')[-1]
        self.file_size = self.get_size()
        self.num_pages = self.get_pages()
    def get_pages(self):
        if self.file_type == 'pdf':
            pdf_file = open(self.file_path, 'rb')
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            return len(pdf_reader.pages)
        elif self.file_type == 'docx':
            converted_pdf_path = f"{self.file_name.split('.')[0]}.pdf"
            docx2pdf.convert(self.file_path, converted_pdf_path)
            pdf_reader = PyPDF2.PdfReader(open(converted_pdf_path, 'rb'))
            os.remove(converted_pdf_path)
            return len(pdf_reader.pages)
        return 0
    def get_name(self):
        return self.file_name
    def get_size(self):
        return os.path.getsize(self.file_path)
    
class Config:
    def __init__(self):
        self.data = {}

    def update(self, key, value):
        self.data[key] = value
    def get(self, key):
        return self.data.get(key)
    def setAttributes(self, config):
        self.data = config
    
    def getAttributes(self):
        return self.data
    def to_json(self):
        return json.dumps(self.data)

    def from_json(self, json_str):
        self.data = json.loads(json_str)


class Printer:
    def __init__(self, name, location, print_config):
        self.name = name
        self.location = location
        self.printProperties = print_config
    def __str__(self):
        return f"{self.name};{self.location}"

    def print_file(self, file: File):
        # Simulate printing a file
        return f"Printing {file.get_name()} on printer {self.name} located at {self.location}."

class SessionManager:
    @staticmethod
    def init_session():
        from flask import session
        session['role'] = None
        session['user_logged_in'] = False

    @staticmethod
    def set_role(role):
        from flask import session
        session['role'] = role

    @staticmethod
    def is_logged_in():
        from flask import session
        return session.get('user_logged_in', False)

    @staticmethod
    def login_user(user):
        from flask import session
        session['user_logged_in'] = True
        if isinstance(user, StudentAccount):
            session['role'] = 'Student'
        elif isinstance(user, AdminAccount):
            session['role'] = 'Admin'

    @staticmethod
    def logout_user():
        from flask import session
        session.clear()
