from flask_script import Command, Manager, Option
from CourseScheduling.app import create_app
from CourseScheduling.blueprints.schedule.models import Course, Requirement, SubReq, Major

manager = Manager(create_app)

def format_prereqs(prereqs):
	"""
	convert OR sets to OR lists in order to load them into the db
	:param prereqs:
        in format [{'CSE46', 'I&CSCI23', 'CSE23', 'I&CSCI46', 'I&CSCIH23'},
                             {'I&CSCI6B'}, {'I&CSCI6D'}, {'MATH2B'}]
    :return:
        prereqs in format:
        [['CSE46', 'I&CSCI23', 'CSE23', 'I&CSCI46', 'I&CSCIH23'],
                             ['I&CSCI6B'], ['I&CSCI6D'], ['MATH2B']]
        """



	output = []
	for or_set in prereqs:
		output.append([])
		for course in or_set:
			a_tuple = course.strip().split(' ')
			dept, cid = a_tuple
			course_obj = Course.objects(dept=dept, cid=cid).first()
			if course_obj:
				output[-1].append(course_obj)
		if not output[-1]: output.pop()
	return output


@manager.command
def load_course(filename="database/txt_files/fullcourses_new.txt"):
	"""
    load course info to database from txt file
    :param filename: txt file path
    sample line:
        COMPSCI;161;DES&ANALYS OF ALGOR;
        [{'CSE46', 'I&CSCI23', 'CSE23', 'I&CSCI46', 'I&CSCIH23'},
        {'I&CSCI6B'}, {'I&CSCI6D'}, {'MATH2B'}];4;{0, 1, 2, 3, 4};False
	"""
	try:
		with open(filename, 'r') as f:
			line = f.readline()
			while line:
				line = line.strip().split(";")
				course = Course(
					dept=line[0], cid=line[1],
					name=line[2],
					units=float(line[4]), quarters=list(eval(line[5])),
					upperOnly=eval(line[6])
				)
				course.save()
				line = f.readline()
	except FileNotFoundError as e:
		print("txt loading ERROR: ", e)
	else:
		print("Successfully loaded txt file", filename)
		# to refer to the course object, we have to load courses without adding prereqs first,
		# and add the prereqs later
		with open(filename, 'r') as f:
			line = f.readline()
			while line:
				line = line.strip().split(";")
				course_obj = Course.objects(dept=line[0], cid=line[1]).first()
				if course_obj:
					course_obj.prereq = format_prereqs(eval(line[3]))
					course_obj.save()
				line = f.readline()
@manager.command
def load_requirement(name='universal', filename='database/txt_files/universal.txt'):
	"""
    load requirement info to database from txt file
    this one does not consider the recommand!
    :param filename: txt file path
	"""
	import re, os 
	major = Major(name=name, requirements=[])
	with open(filename) as f:
		content = f.read().split(";")
		for block in content:
			block = block.strip().split('\n')
			requirement = Requirement(name=block[0], sub_reqs=[])
			i = 1

			while (i < len(block)):
				if re.match("^([1-9][0-9]*)$", block[i]):
					subreq = SubReq(req_list=[], req_num=eval(block[i]))
					requirement["sub_reqs"].append(subreq)
					i += 2  # skip {
				elif re.match("(\}|\{)", block[i]):
					i += 1
				else:
					dept, cid = block[i].strip().split()
					if not Course.objects(dept=dept, cid=cid).first():
						print ("Error in ", dept, cid)
						i += 1
						continue
					requirement.sub_reqs[-1].req_list.append(Course.objects(dept=dept, cid=cid).first())
					i += 1
			print (requirement.name)
			major.requirements.append(requirement)
			requirement.save()
		major.save()



@manager.command
def hello(name='Yitong Wu'):
    print ("hello", name)

if __name__ == "__main__":
    manager.run()
