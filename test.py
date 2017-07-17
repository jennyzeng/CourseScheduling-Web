from datetime import datetime

from flask import Flask

import flask_admin as admin
from flask_mongoengine import MongoEngine
from flask_admin.form import rules
from flask_admin.contrib.mongoengine import ModelView

# Create application
app = Flask(__name__)

# Create dummy secrey key so we can use sessions
app.config['SECRET_KEY'] = '123456790'
app.config['MONGODB_SETTINGS'] = {'DB': 'CS-database', 'host': 'localhost'}
# Create models
db = MongoEngine()
db.init_app(app)



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

    meta = {
        'indexes': [
            ('dept', 'cid') # compound idnex
        ]
    }

    def __unicode__(self):
        return self.name


class SubReq(db.EmbeddedDocument):
    # we need a more complicated model later such that we can
    # refer to the courses in the subreq!!!

    # req_list = db.ListField(db.StringField(max_length=20))
    req_list = db.ListField(db.ReferenceField(Course, dbref=True))
    req_num = db.IntField(min_value=0)

class Requirement(db.Document):
    name = db.StringField(max_length=60)
    major = db.StringField(max_length=60, default="universal")
    sub_reqs = db.ListField(db.EmbeddedDocumentField(SubReq))

    meta = {
        'indexes': [
            ('name', 'major') # compound idnex
        ]
    }


class Major(db.Document):
    name = db.StringField(max_length=30)
    requirements = db.ListField(db.StringField(max_length=30))

    def __unicode__(self):
        return self.name


class CourseView(ModelView):
    column_filters = ['dept', 'cid']

    column_searchable_list = ('name', 'dept', 'cid')


class RequirementView(ModelView):
    column_filters = ['name']

    column_searchable_list = ['name']

    form_subdocuments = {
        'sub_reqs': {
            'form_subdocuments': {
                None: {
                    # Add <hr> at the end of the form
                    'form_rules': ('req_list', 'req_num', rules.HTML('<hr>'))
                }
            }
        }
    }

class MajorView(ModelView):
    column_filters = ['name']
    column_searchable_list = ['name']

    #form = MajorForm

    # def create_form(self):
    #     form = super(MajorView, self).create_form()
    #     return form


# Flask views
@app.route('/')
def index():
    return '<a href="/admin/">Click me to get to Admin!</a>'


if __name__ == '__main__':
    # Create admin
    admin = admin.Admin(app, 'Example: MongoEngine')

    # Add views

    admin.add_view(CourseView(Course))
    admin.add_view(RequirementView(Requirement))
    admin.add_view(MajorView(Major))

    # Start app
    app.run(debug=True)