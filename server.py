from flask import Flask, render_template, flash, redirect, url_for, request, send_file
import coursesDAO, crawlDAO, sessionDAO, exportDAO
from db.secret import secretkey, appsecret
import pymongo, random, json

app = Flask(__name__)
app.secret_key = appsecret
app.url_map.strict_slashes=False

@app.route('/robots.txt')
def robots():
	return "User-agent: *\nDisallow: /"

@app.route('/')
@app.route('/index')
def index():
	return redirect(url_for('timetable'))

@app.route('/classinfo')
@app.route('/classinfo/<permalink>')
def classinfo(permalink=None):
	usesh = sessions.checkSession()
	if permalink == None: permalink = randomKey()
	# print ("about to query on permalink = ", permalink)
	course = courses.get_course_by_permalink(permalink)
	if course is None:
		return redirect(url_for("course_not_found"))
	return render_template('classInfoPage.html', course=course)

@app.route("/search/<query>")
def search(query=None):
	if query == None:
		return redirect(url_for('courselist'))
	else:
		courselist = courses.get_courses()
		return render_template('courseList.html',courses=courselist, q=query)
	

@app.route("/classinfo/addtoTimetable", methods=['POST'])
def addtoTimetable():
	usesh = sessions.checkSession()
	key = request.args.get("key")
	title = request.args.get("title")
	period = request.args.get("period")
	# print(f"got {title}")
	res = sessions.addCourse(key=key,title=title, period=period, doc=usesh)
	# print(res)
	return "course added"

@app.route('/timetable')
def timetable():
	usesh = sessions.checkSession()
	print(usesh)
	try:
		cl = courses.get_selectedCourses(usesh['timetable'])
	except:
		cl = []
	print(cl)
	return render_template("timeTable.html", courselist=cl)

# @app.route('/export', methods=['POST'])
# @app.route('/timetable/export', methods=['POST'])
# def exportReady():
# 	usesh = sessions.checkSession()
# 	uid = usesh["_id"]
# 	received = request.args.get("json")
# 	dumps = json.loads(received)
# 	export = exportDAO.Pprint(listofDict=dumps,uid=uid)
# 	exported = export.toTXT()
# 	if exported:
		
# 	else:
# 		print("not exported correctly")
# 		return "failed"

@app.route('/awesome_schedule')
def export():
	usesh = sessions.checkSession()
	try:
		cl = courses.get_selectedCourses(usesh['timetable'])
	except:
		cl = []
	exports = exportDAO.Pprint(listofDict=cl, uid=usesh["_id"])
	# exports.tempContent()
	exports.toTXT()
	try:
		return send_file('db/timetable.txt', attachment_filename="awesome_schedule.txt")
	except Exception as e:
		print(e)
		return str(e)
			
@app.route('/drop')
@app.route('/timetable/drop')
def drop():
	sessions.dropSession()
	return redirect(url_for('timetable'))

@app.route('/courselist')
@app.route('/courses')
def courselist():
	courselist = courses.get_courses()
	return render_template("courseList.html", courses=courselist)

@app.route('/about')
@app.route('/developer')
def about():
	return render_template('developers.html', creators = ["alexia","rebekah","jin"])

##error handling
@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html')

@app.route("/course_not_found")
def course_not_found():
	return render_template('notFound.html')



def randomKey():
	keys = [d["_id"] for d in courses.get_courses()]
	return random.choice(keys)

client = pymongo.MongoClient(secretkey)
db = client.sils
courses = coursesDAO.CoursesDAO(db)
crawler = crawlDAO.CrawlDAO(db)
sessions = sessionDAO.SessionDAO(db=db, app=app)