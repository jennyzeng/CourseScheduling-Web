from CourseScheduling.extensions import db
from datetime import datetime


class Course(db.Document):
    dept = db.StringField(max_length=10)
    cid = db.StringField(max_length=10)
    name = db.StringField(max_length=60)

    # guess it is better to change the prereq one later...
    # may change it to be a list of Courses not string.
    # so eventually we get a relational model = =...
    prereq = db.ListField(db.ListField(db.ReferenceField('Course', dbref=True)))
    units = db.FloatField()
    quarters = db.ListField(db.ReferenceField('Quarter', dbref=True))
    upperOnly = db.BooleanField(default=False)
    # for sample data in db right now, the pub_date is not correct
    # change the way we load data will fix this problem
    pub_date = db.DateTimeField(default=datetime.now)

    meta = {
        'indexes': [
            ('dept', 'cid') # compound idnex
        ]
    }

    def __unicode__(self):
        return self.dept +" "+ self.cid

class SubReq(db.EmbeddedDocument):
    # we need a more complicated model later such that we can
    # refer to the courses in the subreq!!!

    # req_list = db.ListField(db.StringField(max_length=20))
    req_list = db.ListField(db.ReferenceField(Course, dbref=True))
    req_num = db.IntField(min_value=0)

class Requirement(db.Document):
    name = db.StringField(max_length=60)
    sub_reqs = db.ListField(db.EmbeddedDocumentField(SubReq))

    meta = {
        'indexes': [
            'name' # compound idnex
        ]
    }
    def __unicode__(self):
        return self.name

class Major(db.Document):
    name = db.StringField(max_length=60, default="universal")
    requirements = db.ListField(db.ReferenceField(Requirement, dbref=True))
    
    meta = {
        'indexes': [
            'name'
        ]
    }
    def __unicode__(self):
        return self.name


class Quarter(db.Document):
    name = db.StringField(max_length=40)
    code = db.IntField(min_value=0)
    def __unicode__(self):
        return self.name