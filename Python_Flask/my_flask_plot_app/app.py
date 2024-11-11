from flask import Flask, render_template
import seaborn as sns
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

@app.route('/')
def home():
    # Generate a plot using seaborn
    sns.set(style="whitegrid")
    tips = sns.load_dataset("tips")
    plt.figure(figsize=(10, 6))
    plot = sns.scatterplot(x="total_bill", y="tip", data=tips)
    
    # Save the plot to a BytesIO object
    img = io.BytesIO()
    plot.figure.savefig(img, format='png')
    img.seek(0)
    
    # Encode the image to base64 string
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    
    # Render the template with the plot
    return render_template('index.html', plot_url=plot_url)

if __name__ == '__main__':
    app.run(debug=True)
