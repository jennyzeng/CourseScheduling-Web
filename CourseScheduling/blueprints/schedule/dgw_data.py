import requests, re
from bs4 import BeautifulSoup

# degreework data
class data:
	def __init__(self, cookies):
		self.url = 'https://www.reg.uci.edu/dgw/IRISLink.cgi'
		self.cookies = dict()
		self.name = None
		self.studentID = None
		self.major = list()
		self.minor = list()
		self.spec = list()
		self.applied_classes = list()
		self.degree = None
		self.level = None
		self.process_cookies(cookies)

	def getDict(self):
		return {'name':self.name, 'id':self.studentID, 'major':self.major, 'degree':self.degree,
			'level':self.level, 'spec':self.spec, 'minor':self.minor, 'taken': self.applied_classes}

	def process_cookies(self, cookies):
		for key_val in cookies.split(';'):
			key, val = key_val.split('=', 1)
			self.cookies[key] = val
	
	def fetch_student_id(self):
		if len(self.cookies) == 0:
			return self.studentID

		body = "SERVICE=SCRIPTER&SCRIPT=SD2STUCON"
		r = requests.post(self.url, cookies=self.cookies, data=body)
		
		with open('id.xml', 'w') as f:
			f.write(r.text)

		rl = re.findall('<input type="hidden" name="STUID" value="(\d+)">', r.text)
		if len(rl) == 1:
			self.studentID = rl[0]
		return self.studentID

	def fetch_student_detail(self):
		body = "SERVICE=SCRIPTER&SCRIPT=SD2STUGID&STUID={id}&DEBUG=OFF".format(id=self.studentID)
		r = requests.post(self.url, cookies=self.cookies, data=body)

		with open('details.xml', 'w') as f:
			f.write(r.text)

		soup = BeautifulSoup(r.text, 'lxml')
		stu_data = soup.find('studentdata')
		goaldtl = stu_data.goaldtl
		self.degree = goaldtl['degree']
		self.level = goaldtl['stulevel']
		
		name_pattern = 'sILStudentName = \"(.+)\";'
		rf = re.search(name_pattern, r.text)
		if rf:
			self.name = rf.group(1).strip()

		level_pattern = 'sLevelPicklist\[sLevelPicklist.length\] = new DataItem\(\".*%s.*\", \"(.+)\"\);' % (self.level)
		rf = re.search(level_pattern, r.text)
		if rf:
			self.level = rf.group(1).strip()
		else:
			self.level = None

	def fetch_xml(self):
		body = "SERVICE=SCRIPTER&REPORT=WEB31&SCRIPT=SD2GETAUD%%26ContentType%%3Dxml&ACTION=REVAUDIT&ContentType=xml&STUID=%s&DEBUG=OFF" % (self.studentID)
		r = requests.post(self.url, cookies=self.cookies, data=body)

		with open('courses.xml', 'w') as f:
			f.write(r.text)

		soup = BeautifulSoup(r.text, 'lxml')
		for goal in soup.find('deginfo').findAll('goal'):
			if goal['code'].lower() == 'major':
				self.major.append(goal['valuelit'])
			elif goal['code'].lower() == 'minor':
				self.minor.append(goal['valuelit'])
			elif goal['code'].lower() == 'spec':
				self.spec.append(goal['valuelit'])

		for applied_classes in soup.findAll('classesapplied'):
			for cla in applied_classes.findAll('class'):
				disc, num = '', ''
				if len(cla.get('disc', '')) > 0:
					disc = cla['disc']
				elif len(cla.get('discipline', '')) > 0:
					disc = cla['discipline']

				if len(cla.get('num', '')) > 0:
					num = cla['num']
				elif len(cla.get('number', '')) > 0:
					num = cla['number']

				if len(disc) > 0 and len(num) > 0:
					self.applied_classes.append(disc + ' ' + num)






		

