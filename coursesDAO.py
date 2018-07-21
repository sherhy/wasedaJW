class CoursesDAO:
	def __init__(self, database):
		self.db = database
		self.courses = database.courses

	def insert_entry(self, title, post):
		#todo: make use of the crawlsyllabus.py file as a class object here
		pass

	def get_courses(self):
		cursor = self.courses.find({},{"_id":1, "title":1})
		l = []
		for course in cursor:
			l.append(course)
		return l

	def get_selectedCourses(self, idlist):
		cl = []
		for doc in idlist:
			course = self.courses.find_one({"_id":doc["key"]},{
				"title": 1,
				"courseCode":1,
				"period": 1
			})
			cl.append(course)
		return cl

	def get_course_by_permalink(self, permalink):
		return self.courses.find_one({"_id":permalink})

	def get_one(self, idee="none"):
		return self.courses.find_one({"_id":idee})