from flask import Flask, render_template, flash, redirect, url_for
from coursesDAO import CoursesDAO
from db.secret import secretkey
import pymongo, random

client = pymongo.MongoClient(secretkey)
db = client.sils
courses = CoursesDAO(db)
app = Flask(__name__)

@app.route('/')
def index():
	return redirect(url_for('classinfo'))

@app.route("/course_not_found")
def course_not_found():
	return render_template('notFound.html')

def randomKey():
	keys = [d["_id"] for d in courses.get_courses()]
	return random.choice(keys)

@app.route('/classinfo')
@app.route('/classinfo/<permalink>')
def classinfo(permalink=randomKey()):

	print ("about to query on permalink = ", permalink)
	course = courses.get_course_by_permalink(permalink)

	if course is None:
		redirect(url_for("/course_not_found"))

	# init comment form fields for additional comment
	comment = {'name': "", 'body': "", 'email': ""}
	return render_template('classInfoPage.html', course=course)

@app.route('/courselist')
def courselist():
	l = courses.get_courses()
	return render_template("courseList.html", courses=l)

@app.route('/about')
def about():
	return render_template('developers.html', creators = ["alexia","rebekah","jin"])
