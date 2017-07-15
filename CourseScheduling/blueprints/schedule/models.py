from CourseScheduling.extensions import db
from datetime import datetime


class Course(db.Document):
    dept = db.StringField(max_length=10)
    cid = db.StringField(max_length=10)
    name = db.StringField(max_length=60)

    # guess it is better to change the prereq one later...
    # may change it to be a list of Courses not string.
    # so eventually we get a relational model = =...
    prereq = db.ListField(db.ListField(db.StringField()))
    units = db.FloatField()
    quarters = db.ListField(db.IntField(min_value=0))
    upperOnly = db.BooleanField(default=False)
    # for sample data in db right now, the pub_date is not correct
    # change the way we load data will fix this problem
    pub_date = db.DateTimeField(default=datetime.now)

    def __unicode__(self):
        return self.name

# no idea why this one is not working

class SubReq(db.EmbeddedDocument):
    # we need a more complicated model later such that we can
    # refer to the courses in the subreq!!!

    # req_list = db.ListField(db.StringField(max_length=20))
    req_list = db.ListField(db.ReferenceField(Course))
    req_num = db.IntField(min_value=0)

class Requirement(db.Document):
    name = db.StringField(max_length=20)
    # TODO: comment out 的是新model，暂时无法使用
    # sub_reqs = db.ListField(db.EmbeddedDocumentField(SubReq))

    sub_reqs = db.ListField(db.DictField())