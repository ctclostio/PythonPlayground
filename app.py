from flask import Flask, render_template
import subprocess
import sys
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/snake')
def snake():
    # Get the Python executable path
    python_exe = sys.executable
    
    # Launch snake game in a new process
    subprocess.Popen([python_exe, 'snake_game.py'])
    
    # Return a simple page indicating the game has been launched
    return """
    <html>
    <head>
        <title>Snake Game Launched</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                background-color: #f4f4f4;
            }
            .message {
                text-align: center;
                padding: 20px;
                background: white;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
        </style>
    </head>
    <body>
        <div class="message">
            <h2>Snake Game Launched!</h2>
            <p>The game window should open shortly...</p>
            <p><a href="/">Return to Home</a></p>
        </div>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(debug=True)