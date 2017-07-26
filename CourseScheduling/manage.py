from flask_script import Command, Manager, Option
from CourseScheduling.app import create_app
from CourseScheduling.blueprints.schedule.models import Course, Requirement, SubReq, Major, Quarter

manager = Manager(create_app)


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
            dept, cid = a_tuple
            course_obj = Course.objects(dept=dept, cid=cid).first()
            if course_obj:
                output[-1].append(course_obj)
        if not output[-1]: output.pop()
    return output


@manager.command
def load_course(filename="database/txt_files/fullcourses_new.txt", delete=False):
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
            if delete: Course.objects().delete()
            line = f.readline()
            while line:
                line = line.strip().split(";")
                course = Course.objects(
                    dept=line[0], cid=line[1]).update_one(
                    name=line[2],
                    units=float(line[4]), quarters=format_quarters(eval(line[5]), qdict),
                    upperOnly=eval(line[6]), upsert=True
                )
                # course.save()
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
        print("updated prerequisites")

@manager.command
def load_requirement(name='universal', filename='database/txt_files/universal.txt'):
    """
    load requirement info to database from txt file
    this one does not consider the recommand!
    :param filename: txt file path
    """
    import re, os
    # clean old major
    Major.objects(name=name).upsert_one(requirements=[])
    major = Major.objects(name=name).first()
    with open(filename) as f:

        content = f.read().split(";")
        for block in content:
            block = block.strip().split('\n')
            if not block[0]: continue
            # clean old requirement
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
            major.requirements.append(requirement)
            requirement.save()
        major.save()


@manager.command
def hello(name='Yitong Wu'):
    print("hello", name)


if __name__ == "__main__":
    manager.run()
