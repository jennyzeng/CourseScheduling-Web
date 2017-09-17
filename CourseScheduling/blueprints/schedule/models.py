from CourseScheduling.extensions import db
from datetime import datetime
import lib.CourseSchedulingAlgorithm as cs

def convert_prereq(prereq):
    output = []
    for or_set in prereq:
        output.append([])
        for course in or_set:
            output[-1].append(course.dept + " " + course.cid)
    return output


def convert_quarters(quarters):
    for idx, q in enumerate(quarters):
        quarters[idx] = q.code
    return quarters


class Course(db.Document):
    # dept name might contain spaces
    dept = db.StringField(max_length=10)
    # cid in format ^[0-9]+[A-Z]*$
    cid = db.StringField(max_length=10)
    # name is a brief introduction to the course
    name = db.StringField(max_length=60)

    # a list of lists
    # each nested list contains a reference to a Course object
    prereq = db.ListField(db.ListField(db.ReferenceField('Course', dbref=True)), default=[])
    units = db.FloatField(default=4)
    quarters = db.ListField(db.ReferenceField('Quarter', dbref=True), default=[])
    upperOnly = db.BooleanField(default=False)
    # for sample data in db right now, the pub_date is not correct
    # change the way we load data will fix this problem
    pub_date = db.DateTimeField(default=datetime.now)
    priority = db.IntField(default=0, min_value=0, max_value=5)
    meta = {
        'indexes': [
            ('dept', 'cid') # compound index
        ]
    }

    def __unicode__(self):
        return self.dept +" "+ self.cid

class SubReq(db.EmbeddedDocument):
    # now each requirement refers to the Course object
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
    name = db.StringField(max_length=60, default="UNIVERSAL")
    requirements = db.ListField(db.ReferenceField(Requirement, dbref=True))
    # used to be DictField for better performance,
    # but admin doesn't work well with complex structure. 
    specs = db.ListField(field=db.ReferenceField(Requirement, dbref=True))
    meta = {
        'indexes': [
            'name'
        ]
    }

    def prepareScheduling(self, spec=[], ge_filter={}):
        G, R, R_detail = dict(), dict(), dict()
        req = list(self.requirements)
        if len(spec):
            spec_req = [x for x in self.specs if x in spec]
            req.extend(spec_req)
            print ('spec', spec_req)
        print ('req', req)

        for r in req:
            R[r.name] = list()
            R_detail[r.name] = list()

            for subr in r.sub_reqs:
                c_set = set()

                # for ge requirement, simply apply the missing courses number as requirement number
                if r.name in ge_filter:
                    R[r.name].append(ge_filter[r.name])
                # otherwise, apply it as it is
                else:
                    R[r.name].append(subr.req_num)

                for c in subr.req_list:
                    c_name = c.dept + " " + c.cid
                    c_set.add(c_name)
                    G[c_name] = cs.Course(name=c.name, units=c.units,
                                      quarter_codes=convert_quarters(c.quarters),
                                      prereq=convert_prereq(c.prereq), is_upper_only=c.upperOnly)
                R_detail[r.name].append(c_set)
        return G, R, R_detail

    def __unicode__(self):
        return self.name


class Quarter(db.Document):
    name = db.StringField(max_length=40)
    code = db.IntField(min_value=0)
    def __unicode__(self):
        return self.name
