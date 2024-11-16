from web import create_app

app = create_app()

# Re-run the web server
if __name__ == '__main__':
    app.run(debug=True)