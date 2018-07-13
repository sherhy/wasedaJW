#export function to export the saved courses as a text file

import pprint

class Pprint:
    def __init__(self,listofDict):
        self.dicts=listofDict

    def toTXT(self):
        with open(r'timetable', 'w') as f:
            f.write('Saved Courses\n\n')
            for i in range(len(self.dicts)):
                f.write('Course Title: %s\n' %self.dicts[i]['title'])
                f.write('Course Code: %s\n' %self.dicts[i]['id'])
                f.write('Period: %s\n\n' %self.dicts[i]['period'])
            f.write('www.wasedajw.com') 




saved=[
    {'id': 123123, 'title': 'math', 'period':'Mon.3'},
    {'id': 345345, 'title': 'bio', 'period':'Mon.5,Tue.4'},
    {'id': 456456, 'title': 'phy', 'period':'Wed.4'},
    {'id': 789789, 'title': 'chem', 'period':'Thu.1,Fri,1'},
    ]

timetable=Pprint(saved)
Pprint.toTXT(timetable)
