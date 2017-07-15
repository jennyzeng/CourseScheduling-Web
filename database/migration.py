from CourseScheduling.blueprints.schedule.models import Course, Requirement, SubReq
from CourseScheduling.app import create_app
from CourseScheduling.extensions import db
import os
import sys

"""
use 
$ docker-compose exec website python database/migration.py
to load data
"""
app = create_app()
sys.path.append(os.getcwd())
app.config['MONGODB_SETTINGS'] = {
    'MONGODB_HOST': 'mongodb',
    'MONGODB_PORT': 27017,
    'MONGODB_DB': 'CS-database'
}


def load_course_from_txt(filename):
    """
    load course info to database from txt file
    :param filename: txt file path
    sample line:
        COMPSCI;161;DES&ANALYS OF ALGOR;
        [{'CSE46', 'I&CSCI23', 'CSE23', 'I&CSCI46', 'I&CSCIH23'},
        {'I&CSCI6B'}, {'I&CSCI6D'}, {'MATH2B'}];4;{0, 1, 2, 3, 4};False
    """
    def format_prereqs( prereqs):
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
            output.append(list(or_set))

        return output
    try:
        with open(filename, 'r') as f:
            line = f.readline()
            while line:
                line = line.strip().split(";")
                course = Course(
                    dept=line[0], cid=line[1],
                    name=line[2],
                    prereq=format_prereqs(eval(line[3])),
                    units=float(line[4]),
                    quarters=list(eval(line[5])),
                    upperOnly=eval(line[6])
                )
                course.save()
                line = f.readline()
    except Exception as e:
        print("txt loading ERROR: ", e)
    else:
        print("Successfully loaded txt file", filename)




def load_requirement_from_txt(filename):
    """
    load requirement info to database from txt file
    this one does not consider the recommand!
    :param filename: txt file path
    """
    import re
    with open(filename) as f:
        content = f.read().split(";")
        for block in content:
            block = block.strip().split('\n')
            requirement = Requirement(name=block[0], sub_reqs=[])
            i = 1

            while i < len(block):
                if re.match("^([1-9][0-9]*)$", block[i]):
                    subreq = SubReq(req_list=[], req_num=eval(block[i]))
                    requirement["sub_reqs"].append(subreq)
                    i += 2  # skip {
                elif re.match("(\}|\{)", block[i]):
                    i += 1
                else:
                    requirement.sub_reqs[-1]['req_list'].append(block[i].replace(" ", ""))
                    i += 1
            print(requirement.name)
            requirement.save()

if __name__ == '__main__':
    load_course_from_txt('database/txt_files/fullCourses_new.txt')
    # load_requirement_from_txt('database/txt_files/specializations.txt')