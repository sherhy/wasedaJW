import re
import coursesDAO
import pymongo

#mongoDB driver
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client.sils
courses = coursesDAO.CoursesDAO(db)

