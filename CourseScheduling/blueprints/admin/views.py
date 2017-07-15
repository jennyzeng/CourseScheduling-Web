# https://github.com/flask-admin/flask-admin/blob/master/examples/mongoengine/app.py
# route for admin is localhost:8000/admin/
# no auth for now

from flask_admin.contrib.mongoengine import ModelView
from CourseScheduling.extensions import admin
from CourseScheduling.blueprints.schedule.models import Course, Requirement


class CourseView(ModelView):
    column_filters = ['dept', 'cid']

    column_searchable_list = ('name', 'dept', 'cid')



class RequirementView(ModelView):
    column_filters = ['name']

    column_searchable_list = ('name')

    # form_ajax_refs = {
    #     '': {
    #         'fields': ('name',)
    #     }
    # }

admin.add_view(CourseView(Course))

# TODO: fix the Invalid search field Exception
# admin.add_view(RequirementView(Requirement))
