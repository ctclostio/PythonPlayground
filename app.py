from flask import Flask, render_template
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/snake')
def snake():
    return render_template('snake.html')

if __name__ == '__main__':
    app.run(debug=True)