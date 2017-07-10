from pymongo import MongoClient

"""
A manager that manage the Mongo Database for Course Scheduling Website

before running: do this in bash
 $ mkdir ./data/db
 $ mongod --dbpath ./data
"""
__author__ = 'Zhaohua Zeng'


class MongoManager:
    def __init__(self, host, port):
        """
        Initialize the client and db
        example:
            host: 'localhost',
            port: 27017,
            db:  'CS-database'
        """
        self.client = MongoClient(host, port)
        self.db = self.client['CS-database']

    def get_single_course(self, dept, cid):
        """
        get a course based on the dept and cid
        :param dept: course dept
        :param cid: course cid
        :return: a course dict
        """
        return self.db.course.find_one({'dept': dept, 'cid': cid})

    def insert_single_course(self, course):
        """
        insert single course document into the Course
        :param course: a course dict
        :return: ObjectId Object. a inserted_id of the course
        """
        return self.db.course.insert_one(course).inserted_id

    def update_single_course(self, course):
        """
        update course based on the course dept and cid, if none found, create one
        :param course: a course dict
        :return True is a course is updated
        """
        return self.db.course.update_one({'dept': course['dept'], 'cid': course['cid']},
                                          {'$set': course}, upsert=True).modified_count == 1

    def delete_single_course(self, dept, cid):
        """
        delete a course based on the dept and cid
        if not exists, do nothing
        :param dept: course dept
        :param cid: course cid
        :return True if a course is deleted
        """
        return self.db.course.delete_one({'dept': dept, 'cid': cid}).deleted_count == 1

    def get_single_requirement(self, name):
        """
        get a requirement by name
        :param name: requirement name
        :return: a requirement dict
        """
        return self.db.requirement.find_one({'name': name})

    def insert_single_requirement(self, requirement):
        """
        :param requirement: a requirement dict
        :return: ObjectId Object. a inserted_id of the course
        """
        return self.db.requirement.insert_one(requirement).inserted_id

    def update_single_requirement(self, requirement):
        """
        update the requirement with the same name, if not found, create one
        :param requirement: requirement dict
        :return: True if found one and updated.
        """
        return self.db.requirement.update_one(
            {'name': requirement['name']},
            {'$set': requirement},
            upsert=True).modified_count == 1

    def delete_single_requirement(self, name):
        return self.db.requirement.delete_one({'name': name}).deleted_count == 1

    def get_all_docs(self, doc_type):
        """
        :param doc_type: document type, such as Course, or requirements
        :return: all documents in that doc type in the database
        ** may be super big, use wisely **
        """
        import pprint
        for doc in self.db[doc_type].find():
            pprint.pprint(doc)

    def load_course_from_txt(self, filename):
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
                    course = {
                        'dept': line[0], 'cid': line[1],
                        'name': line[2],
                        'prereq': self._format_prereqs(eval(line[3])),
                        'units': float(line[4]),
                        'quarters': list(eval(line[5])),
                        'upperOnly': eval(line[6])
                    }
                    self.insert_single_course(course)
                    line = f.readline()
        except Exception as e:
            print("txt loading ERROR: ", e)
        else:
            print("Successfully loaded txt file", filename)

    def load_requirement_from_txt(self, filename):
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
                requirement = {"name": block[0], "sub_reqs": []}
                i = 1

                while i < len(block):
                    if re.match("^([1-9][0-9]*)$", block[i]):
                        requirement["sub_reqs"].append(
                            {"req_list": [], "req_num": eval(block[i])})
                        i += 2  # skip {
                    elif re.match("(\}|\{)", block[i]):
                        i += 1
                    else:
                        requirement["sub_reqs"][-1]['req_list'].append(block[i].replace(" ", ""))
                        i += 1
                self.insert_single_requirement(requirement)

    def drop_database(self):
        self.client.drop_database('CS-database')

    def _format_prereqs(self, prereqs):
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


if __name__ == '__main__':
    manager = MongoManager('localhost', 27017)
    manager.load_course_from_txt('database/txt_files/fullCourses_new.txt')
    manager.load_requirement_from_txt('database/txt_files/specializations.txt')
    # # manager.get_all_docs('Course')

    # course = {'cid': '162', 'upperOnly': False, 'units': 0.0, 'quarters': [1, 4], 'dept': 'COMPSCI',
    #           'name': 'FORMAL LANG & AUTM',
    #           'prereq': [['CSE23', 'I&CSCI46', 'I&CSCIH23', 'I&CSCI23', 'CSE46'], ['MATH2A'], ['MATH2B'], ['I&CSCI6B'],
    #                      ['I&CSCI6D']]}
    # print(manager.update_single_course(course))
    # print(manager.get_single_course('COMPSCI', '162'))
    # print (manager.delete_single_course('COMPSCI', '161'))
    # manager.get_all_docs('requirements')
