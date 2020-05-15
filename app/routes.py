from app import app
from flask import render_template, flash, redirect

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html', title='Home')

