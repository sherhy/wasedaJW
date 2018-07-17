import requests, bs4, re
import pymongo
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client.sils
courses = db.courses

#TODO: import the whole keys.txt as list
keys = [
	'210CM20100012018210CM2010021',
	'210CM40200012018210CM4020021',
	'210CO10200012018210CO1020021',
]
values = {
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
url = 'https://www.wsl.waseda.jp/syllabus/JAA104.php'


for pKey in keys:
	course = dict()
	res  = requests.post(url+"?pLng=en&pKey="+pKey)
	res.raise_for_status()
	soup = bs4.BeautifulSoup(res.text, "html5lib").select("tbody > tr")
	fields = list(values)
	doPrint = False
	category = None
	desc = ""
	for elem in soup:
		text = elem.getText().strip().split('\n')
		for line in text:
			if line == "": continue
			if line in fields:
				category = values[line]
				continue
			if category in course:
				course[category] += line.strip()	
			else: 
				course[category] = line.strip()
		course["_id"]=pKey
		course["url"]=url+"?pLng=en&pKey="+pKey
		# tdp = course["tdp"].split(' ')
		# print (tdp)
	try:
		courses.insert_one(course)
	except:
		courses.replace_one({"_id":pKey}, course, upsert=True)

'''
current issues:
1."YEAR" 
	to inset values of each key with a smarter approach, 
	and to cut down white space before and after the keyvalue

2. "Term_Day_Period" 
	to be parsed even more, since this is critical in feeding the time information

3. "COURSE_CODE" & "COURSE_KEY"
	make appropriate changes

4. "OVERVIEW"
	there exists subcategories to parse

5. "Evaluation"
	make use of the percentages given
'''