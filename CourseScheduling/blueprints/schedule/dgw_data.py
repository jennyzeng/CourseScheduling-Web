import requests, re
from bs4 import BeautifulSoup, element

disallowed_per_complete = ['Not Needed', 'Not Used'] 
allowed_rule_type = ['Course', 'Group']
ge_filter = '^(M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3}))\..+$'

# degreework data
class data:
	def __init__(self, cookies):
		self.url = 'https://www.reg.uci.edu/dgw/IRISLink.cgi'
		self.cookies = dict()
		self.name = None
		self.studentID = None
		self.major = ['UNIVERSAL']
		self.minor = list()
		# spec now only support for CS major
		self.spec = list()
		self.classes = set()
		self.degree = None
		self.level = None
		self.units_applied = 0
		self.ge_table = dict()
		self.process_cookies(cookies)

	def getDict(self):
		return {'name':self.name, 'id':self.studentID, 'major':self.major, 'degree':self.degree,
			'level':self.level, 'spec':self.spec, 'minor':self.minor, 'taken': self.classes, 
			'units':self.units_applied}

	def process_cookies(self, cookies):
		for key_val in cookies.split(';'):
			key, val = key_val.split('=', 1)
			self.cookies[key] = val
	
	def fetch_xml(self):
		# fetch student id needed to fetch courses page, which is the key element
		self._fetch_student_id()
		# fetch student information (name, degree, level)
		# maybe we can get rid of this later so that we don't have to parse 3 xml files
		self._fetch_student_detail()
		# key component : fetch course applied, spec, units and etc
		self._fetch_courses()

	def _fetch_student_id(self):
		if len(self.cookies) == 0:
			return self.studentID

		body = "SERVICE=SCRIPTER&SCRIPT=SD2STUCON"
		r = requests.post(self.url, cookies=self.cookies, data=body)

		rl = re.findall('<input type="hidden" name="STUID" value="(\d+)">', r.text)
		if len(rl) == 1:
			self.studentID = rl[0]
		return self.studentID

	def _fetch_student_detail(self):
		body = "SERVICE=SCRIPTER&SCRIPT=SD2STUGID&STUID={id}&DEBUG=OFF".format(id=self.studentID)
		r = requests.post(self.url, cookies=self.cookies, data=body)

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

	def _fetch_courses(self):
		body = "SERVICE=SCRIPTER&REPORT=WEB31&SCRIPT=SD2GETAUD%%26ContentType%%3Dxml&ACTION=REVAUDIT&ContentType=xml&STUID=%s&DEBUG=OFF" % (self.studentID)
		r = requests.post(self.url, cookies=self.cookies, data=body)

		soup = BeautifulSoup(r.text, 'lxml')

		block = soup.find('block')
		self.units_applied = float(block['credits_applied'])

		for goal in soup.find('deginfo').findAll('goal'):
			if goal['code'].lower() == 'major':
				self.major.append(goal['valuelit'])
			elif goal['code'].lower() == 'minor':
				self.minor.append(goal['valuelit'])
			elif goal['code'].lower() == 'spec':
				self.spec.append(goal['valuelit'])

		classes = soup.find("clsinfo")
		for cls in classes.findAll("class"):
			disc, num = '', ''
			if len(cls.get('disc', '')) > 0:
				disc = cls['disc']
			elif len(cls.get('discipline', '')) > 0:
				disc = cls['discipline']

			if len(cls.get('num', '')) > 0:
				num = cls['num']
			elif len(cls.get('number', '')) > 0:
				num = cls['number']

			if len(disc) > 0 and len(num) > 0:
	 			self.classes.add(disc + ' ' + num)

	 	# check for each requirement 
		for rule in soup.find_all('rule', attrs={'indentlevel':'1'}):
			if rule and type(rule) == element.Tag \
			and rule['ruletype'] in allowed_rule_type and rule['per_complete'] not in disallowed_per_complete:
				ge = re.match(ge_filter, rule.get('label', ''))
				if not ge:
					continue
				self.ge_table['GE'+ge.group(1)] = self.checkRequirement(rule)
				# for development purpose, print out how many classes are missing for each requirement
				print ('@@@', 'GE'+ge.group(1), 'missing', self.ge_table['GE'+ge.group(1)], 'courses')

	# return total missing courses for this rule
	def checkRequirement(self, rule):
		# unusable rules 
		if not rule or type(rule) != element.Tag or rule['ruletype'] not in allowed_rule_type or rule['per_complete'] in disallowed_per_complete:
			return 10000  # return a impossible number

		if rule.requirement and rule.requirement.has_attr('numgroups'):
			n = int(rule.requirement['numgroups'])
			shortlist = list()
			for child_rule in rule.find_all('rule'):
				# in case there are multiple subrules
				if child_rule.has_attr('per_complete') and child_rule.get('per_complete') not in disallowed_per_complete \
				and child_rule['ruletype'] in allowed_rule_type:
					shortlist.append(self.checkRequirement(child_rule))
			# sort the list and choose the first n (smallest) subrules
			return sum(sorted(shortlist)[:n])
		else:
			return int(rule.requirement['classes_begin']) - int(rule.classes_applied.text)

		

