# https://github.com/flask-admin/flask-admin/blob/master/examples/mongoengine/app.py
# route for admin is localhost:8000/admin/
# no auth for now

from flask_admin.contrib.mongoengine import ModelView
from CourseScheduling.extensions import admin
from CourseScheduling.blueprints.schedule.models import Course, Requirement
from flask_admin.form import rules

class CourseView(ModelView):
    column_filters = ['dept', 'cid']

    column_searchable_list = ('name', 'dept', 'cid')

    # form_ajax_refs = {
    #     '': {
    #         'fields': ('name',)
    #     }
    # }


class RequirementView(ModelView):
    column_filters = ['name']

    column_searchable_list = ['name']

    # form_subdocuments = {
    #     'sub_reqs': {
    #         'form_subdocuments': {
    #             None: {
    #                 'form_columns': ('req_list', 'req_num')
    #             }
    #         }
    #     }
    # }


admin.add_view(CourseView(Course))

admin.add_view(RequirementView(Requirement))
