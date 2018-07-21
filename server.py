from flask import Flask, render_template, flash, redirect, url_for, request
import coursesDAO, crawlDAO, sessionDAO
from db.secret import secretkey, appsecret
import pymongo, random

app = Flask(__name__)
app.secret_key = appsecret

@app.route('/')
def index():
	return redirect(url_for('classinfo'))

@app.route("/course_not_found")
def course_not_found():
	return render_template('notFound.html')

@app.route("/addtoTimetable", methods=['POST'])
def addtoTimetable():
	usesh = sessions.checksession()
	key = request.args.get("key")
	title = request.args.get("title")
	period = request.args.get("period")


	sessions.addCourse(key=key,title=title, period=period, doc=usesh)

	return "course added"


@app.route('/classinfo')
@app.route('/classinfo/<permalink>')
def classinfo(permalink=None):
	usesh = sessions.checksession()
	if permalink == None: permalink = randomKey()
	print ("about to query on permalink = ", permalink)
	course = courses.get_course_by_permalink(permalink)

	if course is None:
		return redirect(url_for("course_not_found"))

	# init comment form fields for additional comment
	# comment = {'name': "", 'body': "", 'email': ""}
	return render_template('classInfoPage.html', course=course)

@app.route('/courselist')
def courselist():
	courselist = courses.get_courses()
	return render_template("courseList.html", courses=courselist)

@app.route('/timetable')
def timetable():
	usesh = sessions.checksession()
	return render_template("timeTable.html", sesh=usesh)

@app.route('/about')
def about():
	return render_template('developers.html', creators = ["alexia","rebekah","jin"])

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html')

def randomKey():
	keys = [d["_id"] for d in courses.get_courses()]
	return random.choice(keys)

client = pymongo.MongoClient(secretkey)
db = client.sils
courses = coursesDAO.CoursesDAO(db)
crawler = crawlDAO.CrawlDAO(db)
sessions = sessionDAO.SessionDAO(db=db, app=app)