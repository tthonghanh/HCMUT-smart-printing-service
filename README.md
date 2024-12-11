# Student Smart Printing System Project

## Project overview
This project is a Student Smart Printing System (SSPS) developed by Group 11 - CC04 - HCMUT. The system includes a user page and an admin page with distinct functionalities to streamline student management processes. It is designed to provide an intuitive interface for both end users and administrators to perform their respective tasks efficiently.
In this project, we mainly focus on Printing Module, including use cases: upload document, choose printer, specify printing properties, pay for more printing pages, log payment, print documents, log printing actions

## Version
Current version: 1.6

## Features
### Student page:
- Login to the system
- Upload document
- Specify printing properties
- Choose printer
- Buy more printing pages
- Send print request
- View printing history
- View payment history

### SPSO (Student Printing Service Officers) page:
- Admin dashboard
- We did not implement the features of SPSO because we just focused on printing module.

## Document
- A final report that contains all the information of the system
- Images used in report
- Version change

## Flask Project Setup Guide

This project is a simple Flask application. Follow the instructions below to set up the environment and run the application.

### Prerequisites

- Python 3.10 or higher
- `pip` (Python package manager)

If you don't know how to set up a Python environment, we recommend using **Conda** (a package manager for Python). You can install Conda from [here](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html).

### Setup Instructions

#### 1. Create a Virtual Environment

If you are using **Conda**, you can create a new environment with the following command:

```bash
conda create --name flask-env python=3.10
```

Activate the environment:

```bash
conda activate flask-env
```

If you're using **virtualenv** or other methods, create and activate your environment as appropriate.

#### 2. Install Dependencies

After activating your environment, install the required dependencies from the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

#### 3. Run the Flask Application

Once the dependencies are installed, you can start the Flask server by running:

```bash
python src/Controller/backend.py
```
or
```bash
python3 src/Controller/backend.py
```

By default, Flask will run on `http://127.0.0.1:5000/`.

#### 4. Access the Application

Open your web browser and go to [http://127.0.0.1:5000](http://127.0.0.1:5000) to access the running Flask application.

---

That's it! You should now have the Flask application running locally.
