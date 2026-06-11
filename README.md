# Flask Project for WebTech Class


This repository contains a simple Flask web application with three pages: Home, About, and Contact. It also includes basic styling with CSS. This project is intended to be a starting point for students learning about Flask development.

## Getting Started

To get started with this project, you will need to have Python installed (3.12) on your machine. You can download Python from the official website: https://www.python.org/downloads/

## Download the Repository:

https://gitlab.com/martina.casari.93/flaskproject_webtech

To download the repository, click on the green "Code" button and select "Download ZIP". Once the ZIP file has been downloaded, extract the contents to a folder on your computer.

## PyCharm IDE:

Download PyCharm Professional or Community Edition from the official website: https://www.jetbrains.com/pycharm/download/

Build -> PyCharm 2024.2.4

To open the project in PyCharm, launch the IDE and select "Open" from the welcome screen. Navigate to the folder where you extracted the repository and select the folder. PyCharm will open the project, and you will be able to view the files and directories.

## Set up a Virtual Environment:

To set up a virtual environment in PyCharm, follow these steps:

1. Open the project in PyCharm.
2. Click on the bottom left corner where it says "No Python interpreter" or the current interpreter version.
3. Select "Add Interpreter" from the list.
4. Click on "Virtualenv Environment" and then "Create".
5. Choose a location for the virtual environment (e.g., inside the project folder) and click "Create".
6. Once the virtual environment is created, click "OK" to close the settings window.
7. You should now see the virtual environment listed in the bottom left corner of the PyCharm window.
8. To install the required packages, open the terminal in PyCharm and run the following command:

```
pip install -r requirements.txt
```

This will install the Flask package and its dependencies in the virtual environment.


# Start the First Flask Lesson:

The project need to be properly set up in order to run the Flask application. 

In app.py, you will see a green play button next to the `if __name__ == '__main__':` line. Click on the play button to run the Flask application. You should see output similar to the following:

```
FLASK_APP = app.py
FLASK_ENV = development
FLASK_DEBUG = 0
In folder C:/Users/.../FlaskProject_WebTech/FlaskProject_WebTech
C:\Users\...\FlaskProject_WebTech\FlaskProject_WebTech\.venv\Scripts\python.exe -m flask run 
 * Serving Flask app 'app.py'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
```

Clicking on the link `http://127.0.0.1:5000` will open the Flask application in your default web browser. You should see the Home page with links to the About and Contact pages.
