import requests, bs4, re
import pymongo
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client.sils
courses = db.courses

url = 'https://www.wsl.waseda.jp/syllabus/JAA104.php'
#TODO: submit to form https://www.wsl.waseda.jp/syllabus/JAA101.php?pLng=en
# res = requests.get(url)

searches = list()
for i in range(1,6):
	searches += [open(f'Syllabus Search － Syllabus Search Result{i}.htm').read()] #cheat for now


#TODO: parse links from response
pKeys = list()
soups = list()
for search in searches:
	soups += [bs4.BeautifulSoup(search,"html5lib").select('td > a')]
for soup in soups:
	pKeys += [i.get('onclick').split("\'")[-2] for i in soup]
# print(len(pKeys))

#TODO: parse html info for each class link and store it to DB

sample = "210CM20100012018210CM2010021"
for pKey in []:
	res  = requests.post(url+"?pLng=en&pKey="+pKey)
	res.raise_for_status()
	with open('sampleCourse.htm','w') as f:
		f.write(res.text)
	soup = bs4.BeautifulSoup(res.text, "html5lib").select("tbody > tr")

fields = [
'Year',
'School',
'Course Title',
'Instructor',
'Term/Day/Period',
'Category',
'Course Key\n',
'Main Language\n',
'Course Code\n',
'Level\n',
'Subtitle\n',
'Course Outline\n',
'Objectives\n',
'Course Schedule\n',
'Textbooks\n',
'Reference\n',
'Evaluation\n',
]

course = dict()
with open('sampleCourse.htm') as f:
	
	soup = bs4.BeautifulSoup(f.read(), "html5lib").select("tbody > tr")
	for elem in soup:
		for field in fields:
			if field in elem.getText():
				text = ' '.join(elem.getText().split('\n'))
				# print(f"{field.strip()}: {text}")#[len(field):]	
				course[field.strip()] = text[len(field):]
				fields.remove(field) #so that other words of same field name wont get caught

courses.insert_one(course)

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