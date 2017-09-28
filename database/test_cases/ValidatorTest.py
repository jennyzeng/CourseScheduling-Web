from database.schemas import CourseSchema, RequirementsSchema
from database.Validator import CourseValidator, RequirementValidator
import json

def testReqs():
    ReqJson = {
        "major": "COMPUTER SCIENCE",
        "requirements": [
            {
                "name": "CS-Lower-division",
                "sub_reqs": [
                    {
                        "req_num": 16,
                        "req_list": [
                            "I&C SCI 31",
                            "I&C SCI 32",
                            "I&C SCI 33",
                            "I&C SCI 45C",
                            "I&C SCI 46",
                            "I&C SCI 51",
                            "I&C SCI 53+53L",
                            "I&C SCI 90",
                            "IN4MATX 43",
                            "MATH 2A",
                            "MATH 2B",
                            "I&C SCI 6B",
                            "I&C SCI 6D",
                            "STATS 67",
                            "GEII -1",
                            "GEII -2"
                        ]
                    },
                    {
                        "req_num": 1,
                        "req_list": [
                            "I&C SCI 6N",
                            "MATH 3A"
                        ]
                    }
                ]
            }],
        "specs": [
            {
                "name": "CS:Algorithms",
                "sub_reqs": [
                    {
                        "req_num": 2,
                        "req_list": [
                            "COMPSCI 178",
                            "COMPSCI 171"
                        ]
                    },
                    {
                        "req_num": 4,
                        "req_list": [
                            "COMPSCI 162",
                            "COMPSCI 163",
                            "COMPSCI 164",
                            "COMPSCI 165",
                            "COMPSCI 167",
                            "COMPSCI 169",
                            "COMPSCI 168",
                            "COMPSCI 177",
                            "COMPSCI 179"
                        ]
                    }
                ]
            }]
    }
    RequirementValidator(ReqJson, RequirementsSchema.SCHEMA)

def testReqsJson():
    with open("../requirements/UNIVERSAL.json", 'r') as json_data:
        d = json.load(json_data)
        RequirementValidator(d, RequirementsSchema.SCHEMA)

def testCourse():
    CourseTest = {
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
    CourseValidator(CourseTest, CourseSchema.SCHEMA)


if __name__ == '__main__':
    testReqs()
    testReqsJson()
    testCourse()
