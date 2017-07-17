from flask_admin.form import rules
from flask_admin.contrib.mongoengine import ModelView
from CourseScheduling.extensions import admin
from CourseScheduling.blueprints.schedule.models import Course, Requirement


class CourseView(ModelView):
    column_filters = ['dept', 'cid']

class RequirementView(ModelView):
    form_subdocuments = {
        'sub_reqs': {
            'form_subdocuments': {
                None: {
                    # Add <hr> at the end of the form
                    'form_rules': ('req_num', 'req_list', rules.HTML('<hr>'))
                }
            }
        }
    }


admin.add_view(CourseView(Course))
admin.add_view(RequirementView(Requirement))