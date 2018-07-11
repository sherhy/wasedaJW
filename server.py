from flask import Flask, render_template
import syllabusDAO
import pymongo


app = Flask(__name__)

@app.route('/')
def index(creators = ["alexia","rebekah","jin"]):
	#landing page
	return render_template('index.html', creators=creators)

#TODO: run syllabusCrawl.py twice a year
	#TODO: complete a syllabusCrawl that inputs into a DB format with the schema:

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client.sils
courses = coursesDAO.CoursesDAO(db)

courses.insert_entry("1234m123b", "course title", "other bs")