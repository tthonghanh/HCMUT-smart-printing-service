# For current development
In this current commit, I have:
- Finish routing every html pages
- Added some exception handling 
- Handle some communication between frontend and backend, including:
  - Set, save and send config of printer and files
  - Config of user account is not implemented yet
  - Missing some frontend files from the lastest commit on branch frontend
Remaining tasks include:
- Add designed classes
- Handle lastest commit on branch frontend
- Wait for testing and feedback
# Flask Project Setup Guide

This project is a simple Flask application. Follow the instructions below to set up the environment and run the application.

## Prerequisites

- Python 3.10 or higher
- `pip` (Python package manager)

If you don't know how to set up a Python environment, we recommend using **Conda** (a package manager for Python). You can install Conda from [here](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html).

## Setup Instructions

### 1. Create a Virtual Environment

If you are using **Conda**, you can create a new environment with the following command:

```bash
conda create --name flask-env python=3.10
```

Activate the environment:

```bash
conda activate flask-env
```

If you're using **virtualenv** or other methods, create and activate your environment as appropriate.

### 2. Install Dependencies

After activating your environment, install the required dependencies from the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### 3. Run the Flask Application

Once the dependencies are installed, you can start the Flask server by running:

```bash
python app.py
```

By default, Flask will run on `http://127.0.0.1:5000/`.

### 4. Access the Application

Open your web browser and go to [http://127.0.0.1:5000](http://127.0.0.1:5000) to access the running Flask application.

---

That's it! You should now have the Flask application running locally.

If you encounter any issues, feel free to reach out.
