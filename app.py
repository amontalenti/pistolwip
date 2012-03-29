import os
from datetime import datetime

from flask import Flask, render_template, url_for, send_from_directory

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.jinja2.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

def main():
    app.run(debug=True)

if __name__ == '__main__':
    main()
