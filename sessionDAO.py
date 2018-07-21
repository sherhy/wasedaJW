from flask import request, session
import random, string
class SessionDAO():
	def __init__(self, db, app):
		self.db = db
		self.sessions = db.sessions
		self.app = app

	def checksession(self):
		sid = request.cookies.get(self.app.session_cookie_name)
		if "_id" in session:
			usesh = self.find_session(sid)
		else:
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