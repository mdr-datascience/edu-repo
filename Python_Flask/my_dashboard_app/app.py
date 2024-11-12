from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import seaborn as sns
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# Initialize the SQLite database
def init_db():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            value REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Route for the home page with form to add data
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        category = request.form['category']
        value = request.form['value']
        
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute('INSERT INTO data (category, value) VALUES (?, ?)', (category, value))
        conn.commit()
        conn.close()
        
        return redirect(url_for('index'))
    
    return render_template('index.html')

# Route to display the dashboard with seaborn plots
@app.route('/dashboard')
def dashboard():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('SELECT category, value FROM data')
    data = c.fetchall()
    conn.close()
    
    # Convert data to a DataFrame
    import pandas as pd
    df = pd.DataFrame(data, columns=['Category', 'Value'])
    
    # Create a seaborn plot
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Category', y='Value', data=df)
    
    # Save the plot to a PNG image in memory
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    
    # Encode the image to base64 string
    plot_url = base64.b64encode(img.getvalue()).decode()
    
    return render_template('dashboard.html', plot_url=plot_url)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)