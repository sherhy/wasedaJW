import subprocess
import requests, bs4, re, pymongo
from db.secret import secretkey

client = pymongo.MongoClient(secretkey)
db = client.sils
courses = db.courses

class CrawlDAO:
	def __init__(self):
		self.values = {
			'url':'url',
			'Evaluation Criteria':'evaluation',
			'Reference':'reference',
			'Textbooks':'textbooks',
			'Course Schedule':'schedule',
			'Objectives':'objectives',
			'Course Outline':'outline',	
			'Subtitle':'subtitle',
			'Types of lesson':'typeOfLesson',
			'Level':'level',
			'Course Code':'courseCode',
			'Main Language':'language',
			'Course Class Code':'classCode',
			'Course Key':'courseKey',
			'Campus':'campus',
			'Classroom':'clasroom',
			'Credits':'credits',
			'Eligible Year':'eligibleYear',
			'Category':'category',
			'Term/Day/Period':'tdp',#parse again
			'Instructor':'instructor',
			'Course Title':'title',
			'School':'school',
			'Year':'year',
			'First Academic disciplines': 'fad',
		}

		# self.keys = [
		# 	'210CM20100012018210CM2010021',
		# 	'210CM40200012018210CM4020021',
		# 	'210CO10200012018210CO1020021',
		# ]

		with open("db/keys.csv") as d:
			self.keys = list(filter(lambda k: k.strip()!="", d.read().split(',')))

		self.url = 'https://www.wsl.waseda.jp/syllabus/JAA104.php'
		self.tdpPattern = re.compile(r"(\w{3,4}\.\d)")

	def phantomJS(self):

		res = subprocess.run('ls')
		print(res.stdout)

		pass

	def perlParse(self):
		pass

	def add2Mongo(self):
		def tdpReplace(course):
			try:
				token = course['tdp'].replace(u'\xa0', u' ').split(" ")
				course['semester']=token[0]
				course['period'] = re.findall(self.tdpPattern, token[-1])
			except:
				pass
			
		for pKey in self.keys:
			course = dict()
			res  = requests.post(self.url+"?pLng=en&pKey="+pKey.strip())
			res.raise_for_status()
			soup = bs4.BeautifulSoup(res.text, "html5lib").select("tbody > tr")
			fields = list(self.values)
			category = None
			for elem in soup:
				text = elem.getText().strip().split('\n')
				for line in text:
					if line == "": continue
					if line in fields:
						category = self.values[line]
						continue
					if category in course:
						course[category] += line.strip()	
					else: 
						course[category] = line.strip()
			course["_id"]=pKey.strip()
			course["url"]=self.url+"?pLng=en&pKey="+pKey
			tdpReplace(course)
			try:
				courses.insert_one(course)
			except:
				courses.replace_one({"_id":pKey.strip()}, course, upsert=True)

if __name__=="__main__":
	a = CrawlDAO()
	a.add2Mongo()