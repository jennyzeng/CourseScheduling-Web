from CourseScheduling.blueprints.schedule.models import Course, Requirement, SubReq, Major, Quarter
import json

def load_quarters():
    qdict = ['fall 1', 'winter 1', 'spring 1', 'fall 2', 'winter 2', 'spring 2']
    for idx, value in enumerate(qdict):
        # clean old quarter
        Quarter.objects(name=value).update_one(code=idx,upsert=True)
        qdict[idx] = Quarter.objects(name=value).first()
    return qdict


def format_quarters(qlist, qdict):
    qlist = list(qlist)
    for i in range(len(qlist)):
        qlist[i] = qdict[qlist[i]]
    return qlist


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
            # ex. PHY SCI 122B 
            # assume the last segment is the cid, everything in front of cid is a dept
            dept, cid = ' '.join(a_tuple[:-1]), a_tuple[-1]
            course_obj = Course.objects(dept=dept, cid=cid).first()
            if course_obj:
                output[-1].append(course_obj)
        if not output[-1]: output.pop()
    return output


def load_course(filename="database/txt_files/fullcourses_new.txt"):
    """
    load course info to database from txt file
    :param filename: txt file path
    :param delete: delete all courses in db if True
    sample line:
        COMPSCI;161;DES&ANALYS OF ALGOR;
        [{'CSE46', 'I&CSCI23', 'CSE23', 'I&CSCI46', 'I&CSCIH23'},
        {'I&CSCI6B'}, {'I&CSCI6D'}, {'MATH2B'}];4;{0, 1, 2, 3, 4};False
    """
    qdict = load_quarters()
    try:
        with open(filename, 'r') as f:
            """
            # give up ijson because we are plannin to decrease the workload by separating courses by dept, 
            # so each file won't be too large. 

            # use ijson in case we will parse large course json file in future
            parser = parse(f)
            course = None
            for prefix, event, value in parser:
                # the begin of the first course in the file 
                if not course and prefix != '' and event == 'start_map':
                    course = Course(cid='', dept='', name='')
                # the rest of the conditional statements are supposed to be excuted line by line 
                elif prefix[-4:] == '.cid' and event == 'string':
                    course.cid= value
                elif prefix.endswith('.dept') and event == 'string':
                    course.dept = value
                elif prefix.endswith('.name') and event == 'string':
                    course.name = value
                elif prefix[-14:] == '.quarters.item' and event == 'number':
                    course.quarters.append(Quarter.objects(code=value).first())
                elif prefix.endswith('.units') and event == 'string':
                    course.units = int(value)
                elif prefix.endswith('.upperOnly') and event == 'boolean':
                    course.upperOnly = value
                # when the course is loaded and event end_map is happening
                elif course and prefix == course.dept+' '+course.cid and event == 'end_map':
                    course.save()
                    course = None;
            """
            
            for k, c in json.load(f).items():
                Course(name=c['name'], cid=c['cid'], units=int(c['units']), upperOnly=c['upperOnly'], dept=c['dept'],
                    quarters=[Quarter.objects(code=x).first() for x in c['quarters']]).save()

    except FileNotFoundError as e:
        print("txt loading ERROR: ", e)
    else:
        print("Successfully loaded txt file", filename)
        # to refer to the course object, we have to load courses without adding prereqs first,
        # and add the prereqs later
        with open(filename, 'r') as f:
            for k, c in json.load(f).items():
                Course.objects(cid=c['cid'], dept=c['dept']).update_one(prereq=format_prereqs(c['prereqs']))

        print ("updated prerequisites")

def load_requirement(name='universal', filename='database/txt_files/universal.txt'):
    """
    load requirement info to database from txt file
    this one does not consider the recommand!
    :param filename: txt file path
    """
    import re, os

    spec = False
    name = name.lower()
    Major.objects(name=name).upsert_one(requirements=[])
    major = Major.objects(name=name).first()
    with open(filename) as f:
        content = f.read().split(";")
        for block in content:
            block = block.strip().split("\n")
            if not block[0]: continue
            if block[0].lower() == 'spec':
                spec = True
                continue

            Requirement.objects(name=block[0]).update_one(sub_reqs=[], upsert=True)
            requirement = Requirement.objects(name=block[0]).first()
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
                        print("Error in ", dept, cid)
                        i += 1
                        continue
                    requirement.sub_reqs[-1].req_list.append(Course.objects(dept=dept, cid=cid).first())
                    i += 1
            print(requirement.name)
            if spec:
                major.specs.append(requirement)
            else:
                major.requirements.append(requirement)
            requirement.save()
        major.save()

