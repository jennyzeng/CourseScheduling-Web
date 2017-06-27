__author__ = 'Zhaohua Zeng'

"""
A manager that manage the Mongo Database for Course Scheduling Website

before running: do this in bash
 $ mkdir ./data/db
 $ mongod --dbpath ./data
"""

import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
import pprint


class MongoManager:
    def __init__(self, host, port, db):
        """
        Initialize the client and db
        example:
            host: 'localhost',
            port: 27017,
            db:  'CS-database'
        """
        self.client = MongoClient(host, port)
        self.db = self.client[db]
        self.courses = self.db.courses

    def insert_single_course(self, course):

        try:
            course_id = self.db.courses.insert_one(course).inserted_id
            print('Insert course successful, with course id: ', course_id)
        except Exception as e:
            print('Mongo insert course ERROR:', e)

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

    def insert_single_requirement(self, requirement):
        try:
            req_id = self.db.requirements.insert_one(requirement).inserted_id
            print('Insert requirement successful, wit req id: ', req_id)
        except Exception as e:
            print('Mongo insert course ERROR:', e)

    def load_requirement_from_txt(self, filename):
        """
        load requirement info to database from txt file
        :param filename: txt file path
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

    def get_all_docs(self, doc_type):
        """
        :param doc_type: document type, such as courses, or requirements
        :return: all documents in that doc type in the database
        ** may be super big, use wisely **
        """
        # TODO: add check if doc_type exist in db
        for doc in self.db[doc_type].find():
            pprint.pprint(doc)

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
    manager = MongoManager('localhost', 27017, 'CS-database')
    # manager.load_course_from_txt('fullcourses_new.txt')
    # manager.get_all_docs('requirements')
