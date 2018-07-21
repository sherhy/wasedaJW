from flask import Flask, render_template, flash, redirect, url_for, request
import coursesDAO, crawlDAO, sessionDAO
from db.secret import secretkey, appsecret
import pymongo, random

app = Flask(__name__)
app.secret_key = appsecret

@app.route('/')
@app.route('/index')
def index():
	return redirect(url_for('classinfo',permalink=None))

@app.route("/course_not_found")
def course_not_found():
	return render_template('notFound.html')

@app.route("/classinfo/addtoTimetable", methods=['POST'])
@app.route("/addtoTimetable", methods=['POST'])
def addtoTimetable():
	usesh = sessions.checkSession()
	key = request.args.get("key")
	title = request.args.get("title")
	period = request.args.get("period")

	print(f"got {title}")

	sessions.addCourse(key=key,title=title, period=period, doc=usesh)

	return "course added"

@app.route('/drop')
@app.route('/timetable/drop')
def drop():
	sessions.dropSession()
	return redirect(url_for('timetable'))

@app.route('/classinfo')
@app.route('/classinfo/<permalink>')
def classinfo(permalink=None):
	usesh = sessions.checkSession()
	if permalink == None: permalink = randomKey()
	print ("about to query on permalink = ", permalink)
	course = courses.get_course_by_permalink(permalink)
	if course is None:
		return redirect(url_for("course_not_found"))
	return render_template('classInfoPage.html', course=course)


@app.route('/courselist')
@app.route('/courses')
def courselist():
	courselist = courses.get_courses()
	return render_template("courseList.html", courses=courselist)

@app.route('/timetable')
def timetable():
	usesh = sessions.checkSession()
	return render_template("timeTable.html", sesh=usesh)

@app.route('/about')
@app.route('/developer')
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