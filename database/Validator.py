"""
a tool for validating the json files
"""

from jsonschema import validate, ValidationError
from database.schemas import CourseSchema
import json


class InvalidJsonError(Exception):
    """
    raised if course is not valid
    """
    pass

def CourseValidator(data, schema):
    """
    :param data: a dict of courses
    :return: where error happens
    """
    err_message = ''
    for key, val in data.items():
        try:
            validate(val, schema)
        except ValidationError as e:
            err_message += "validation error on key {k}, with validation error: \n{e}".format(k=key, e=e.message)
    if err_message:
        raise InvalidJsonError(err_message)

if __name__ == '__main__':

    test = {
        "COMPSCI 111": {
            "cid": "111",
            "dept": "COMPSCI",
            "name": "DIGITAL IMAGE PROC",
            "prereqs": [
                [
                    "I&C SCI 46",
                    "CSE 23",
                    "I&C SCI 23",
                    "CSE 46",
                    "I&C SCI H23"
                ],
                [
                    "I&C SCI 6D"
                ],
                [
                    "MATH 3A",
                    "MATH 6G",
                    "I&C SCI 6N"
                ]
            ],
            "quarters": [
                3
            ],
            "units": 4,
            "upperOnly": False
        },
        "COMPSCI 112": {
            "cid": "112",
            "dept": "COMPSCI",
            "name": "COMPUTER GRAPHICS",
            "prereqs": [
                [
                    "CSE 43",
                    "I&C SCI 22",
                    "I&C SCI 33",
                    "CSE 22",
                    "I&C SCI H22"
                ],
                [
                    "I&C SCI 45C",
                    "CSE 45C"
                ],
                [
                    "MATH 3A",
                    "MATH 6G",
                    "I&C SCI 6N"
                ]
            ],
            "quarters": [
                1,
                3
            ],
            "units": 4,
            "upperOnly": False
        },
    }
    CourseValidator(test,CourseSchema.SCHEMA)
    with open("courses/COMPSCI.json", 'r') as json_data:
        d = json.load(json_data)
        CourseValidator(d,CourseSchema.SCHEMA)
