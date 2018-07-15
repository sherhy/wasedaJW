from flask import Flask, render_template
import seed

app = Flask(__name__)


@app.route('/')
def index():
	return render_template('ClassInfoPage_1.2.htm', course = seed.course)
