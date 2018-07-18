import random, string
class SessionDAO():
	def __init__(self, db):
		self.db = db
		self.sessions = db.sessions

	def create_session(self):
		random_string = ""
		for _ in range(51):
			random_string += random.choice(string.ascii_letters)
		try:
			self.sessions.insert_one({"_id": random_string})
		except:
			pass
		return random_string