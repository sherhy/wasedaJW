class CoursesDAO:
	def __init__(self, database):
		self.db = database
		self.courses = database.courses

	def insert_entry(self, title, post):
		#todo: make use of the crawlsyllabus.py file as a class object here
		pass
		# print "inserting blog entry", title, post

		# # fix up the permalink to not include whitespace

		# exp = re.compile('\W') # match anything not alphanumeric
		# whitespace = re.compile('\s')
		# temp_title = whitespace.sub("_",title)
		# permalink = exp.sub('', temp_title)

		# # Build a new post
		# post = {"title": title,
		# 		"author": author,
		# 		"body": post,
		# 		"permalink":permalink,
		# 		"tags": tags_array,
		# 		"comments": [],
		# 		"date": datetime.datetime.utcnow()}

		# # now insert the post
		# try:
		# 	print "Inserting the post"
		# 	self.posts.insert_one(post)
		# except:
		# 	print "Error inserting post"
		# 	print "Unexpected error:", sys.exc_info()[0]

		# return permalink

	def get_courses(self):
		cursor = self.courses.find({},{"_id":1, "title":1})
		l = []
		for course in cursor:
			l.append(course)
		return l

	def get_course_by_permalink(self, permalink):
		return self.courses.find_one({"_id":permalink})

	def get_one(self, idee="none"):
		return self.courses.find_one({"_id":idee})