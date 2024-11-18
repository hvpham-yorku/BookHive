# Motivation 
This project aims to streamline and improve the library management system for both administrators and users. The goal is to provide a more efficient, user-friendly platform for managing library catalogs and improving the overall user experience. The system addresses common issues such as outdated catalog systems, poor user interfaces, and inefficient management practices. By creating a modern, easy-to-use system, this project enhances the management of smaller libraries and ensures a more seamless interaction for users and administrators alike.


# Installations needed (Note that there has been a change in tools for the design! The changes are approved by the professor. For further information please review the Description provided on Project setup -> readme.file tag)
**To run this project, you will need the following tools and software:** 
**1. VSCode** – for writing and running the Python code.
**2. SQL** – for database management and storing library data.
**3. HTML, CSS, JavaScript** – for the frontend integration.
**4. Flask API** - Backend and frontend connection.


# Steps to Set Up:
**1. Install VSCode and Install Python extension:**
- Install VSCode and Python extention package.
- On the terminal run the commands "pip install -flask" and "pip install flask-login" for the API.
- If you get an error, it means the Python app is not installed. Go to https://www.python.org/downloads/ and download Python to your PC and add the Path of it into Environmental variables. Re-run the prompt again and flask should be installed.
 
**2. Install MySQL:**
- On the terminal, run the command pip install flask-sqlalchemy to install the database SQL to the work environment.
- Set up SQL extention database for storing additional library information(Will be needed for list creation).

**3. Set Up the Frontend:**
- VSCode by default support HTML-CSS and Javascript extension.

**4. Run the Project:**
- Import the Python project into VScode. You can make the connection by cloning the assigned repository on github.
- Run the amain.py file and follow the link created on the terminal. You will be redirected to a webpage where you can see the webapp.

# Contribution 
**1. Git Flow:**
- We will use Git flow to manage our branches. This helps maintain a clean, organized workflow.

**2. Branch Naming:**
Use the following naming conventions for branches:
- gui/<feature-name>:  for updates or new features related to the graphical user interface.
- database/<feature-name>: for changes or updates related to the database or its structure.
- code/<feature-name>:  for changes related to the main code or backend logic.
- main for the production-ready version.
   
**3. GitHub Issues:**
- We will use GitHub Issues to report and track bugs. Please create an issue for any bugs you encounter or new features you would like to add.

**4. Pull Requests:**
- After making changes, submit a pull request to the appropriate branch (e.g., gui, database, or code). Keep the pull request description simple and concise, explaining the changes made.


