from flask import Flask, render_template_string
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

@app.route('/')
def home():
    # Create a simple plot using matplotlib
    plt.figure()
    plt.plot([1, 2, 3, 4], [1, 4, 9, 16])
    plt.title('Simple Plot')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')

    # Save the plot to a BytesIO object and enconde to base64
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    # Render the plot in an HTML template
    html = '''
    <!doctype html>
    <html>
    <head>
        <title>Matplotlib Plot</title>
    </head>
    <body>
        <h1>Matplotlib Plot</h1>
        <img src="data:image/png;base64,{{ plot_url }}">
    </body>
    </html>
    '''
    
    return render_template_string(html, plot_url=plot_url)

if __name__ == '__main__':
    app.run(debug=True)
