#export function to export the saved courses as a text file

import pprint, tempfile

class Pprint:
	def __init__(self,listofDict,uid):
		self.dicts=listofDict
		self.uid = uid
		# self.tempMake()

	def toTXT(self):
		print(self.dicts)
		try:
			with open(f"db/timetable.txt", 'w') as f:
				f.write('Saved Courses\n\n')
				for doc in self.dicts:
					f.write(f"Course Title: {doc['title']}\n")
					f.write(f"Course Code: {doc['courseCode']}\n")
					f.write(f"Period: {' '.join(doc['period'])}\n\n")
				f.write('www.wasedajw.herokuapp.com') 
			return True
		except:
			return False

	def tempMake(self):
		self.temp = tempfile.TemporaryFile()

	def tempContent(self):
		try:
			self.temp.write('Saved Courses\n\n')
			for i in range(len(self.dicts)):
				self.temp.write(f"Course Title: {self.dicts[i]['title']}\n")
				self.temp.write(f"Course Code: {self.dicts[i]['code']}\n")
				self.temp.write(f"Period: {' '.join(self.dicts[i]['period'])}\n\n")
			self.temp.write('www.wasedajw.herokuapp.com') 
			return True
		except:
			return False