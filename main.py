"""
The `main.py` file serves as the entry point for running the Flask application.

Key Components:
1. Import `create_app`:
   - Imports the `create_app` function from the `website` package.
   - This function initializes and configures the Flask application.

2. Application Initialization:
   - Calls `create_app()` to create and configure the Flask app instance.

3. Run the Application:
   - Checks if the script is executed directly (via `__name__ == '__main__'`).
   - Runs the Flask development server with `debug=True` to enable debugging features.

This file is designed to launch the application locally for testing and development purposes.
"""

from website import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True) 
