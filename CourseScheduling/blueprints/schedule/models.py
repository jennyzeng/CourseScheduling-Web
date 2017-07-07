from CourseScheduling.extensions import db
from datetime import datetime


class Course(db.Document):
    dept = db.StringField(max_length=10)
    cid = db.StringField(max_length=10)
    name = db.StringField(max_length=60)
    prereq = db.ListField(db.ListField(db.StringField()))
    units = db.FloatField()
    quarters = db.ListField(db.IntField(min_value=0))
    upperOnly = db.BooleanField(default=False)
    pub_date = db.DateTimeField(default=datetime.now)


class SubReq(db.Document):
    req_list = db.ListField(db.StringField(max_length=20))
    req_num = db.IntField(min_value=0)

class Requirement(db.Document):
    name = db.StringField(max_length=20)
    sub_reqs = db.ListField(SubReq)

