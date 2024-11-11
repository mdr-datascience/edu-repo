# Import libraries
from flask import Flask, render_template_string

# Create app
app = Flask(__name__)

# Define homepage route
@app.route('/')
def home():
    # Hello World string
    welcome_string = "Hello World!"

    # Render an HTML template
    html = '''
    <!doctype html>
    <html>
    <head>
        <title>Welcome Page</title>
    </head>
    <body>
        <h1>{{ wstring }}</h1>
    </body>
    </html>
    '''
    
    return render_template_string(html, wstring=welcome_string)

# Run app in debug mode
if __name__ == '__main__':
    app.run(debug=True)