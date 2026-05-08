from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/calculate', methods=['POST'])
def calculate_age():
    try:
        birth_year = int(request.form['birth_year'])
        today = datetime.now().year

        if birth_year > today or birth_year < 1900:
            birth_year = int(birth_year_str)
            age = today - birth_year
            return render_template('result.html', age=age)
        else: