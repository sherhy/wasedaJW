from flask import Flask, render_template
from db.seed import course

app = Flask(__name__)


@app.route('/')
def index():
	return render_template('ClassInfoPage.html', course = course)