from flask import request, session, flash
import random, string, uuid

class SessionDAO():
	def __init__(self, db, app):
		self.db = db
		self.sessions = db.sessions
		self.app = app

	def addCourse(self, key, period, title, doc):
		#TODO: just get the key and pull data from the courses collection using "_id"
		self.sessions.update_one(
			{"_id":doc["_id"]
		},{
			'$addToSet':{'timetable': {
				'title':title,
				'key':key,
				'period':period
			}
		}})
	
	def dropSession(self):
		usesh = self.checkSession()
		self.sessions.delete_one({"_id": usesh["_id"]})
		return None

	def checkSession(self):
		sid = request.cookies.get(self.app.session_cookie_name)
		if sid:
			if "_id" in session:
				sid = session["_id"]
				usesh = self.find_session(sid)
				if usesh: 
					return usesh
				else:
					flash("Search and add courses to your timetable!")
					usesh = self.create_session(sid)
			else:
				flash("Search and add courses to your timetable!")
				session["_id"] = sid
				usesh = self.create_session(sid)
		else:
			flash("Search and add courses to your timetable!")
			sid = str(uuid.uuid4())
			session["_id"] = sid
			usesh = self.create_session(sid)
		return usesh

	def find_session(self, uid):
		try:
			sesh = self.sessions.find_one({"_id":uid})
			return sesh
		except:
			print('mongodb find_session error')

	def create_session(self, uid):
		try:
			sesh = {"_id": uid}
			self.sessions.insert_one(sesh)
			return sesh
		except:
			print("mongodb create_session error session already in db")