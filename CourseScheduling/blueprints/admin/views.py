# https://github.com/flask-admin/flask-admin/blob/master/examples/mongoengine/app.py
# route for admin is localhost:8000/admin/
# no auth for now

from flask_admin.contrib.mongoengine import ModelView
from flask_admin.form import rules
from flask_security import current_user
from flask import redirect, request, abort, url_for, render_template
from flask_admin import AdminIndexView, expose

class HomeView(AdminIndexView):

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))


class CourseView(ModelView):
    can_create = True
    can_edit = True
    column_filters = ['dept', 'cid']

    column_searchable_list = ('name', 'dept', 'cid')

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('superuser'):
            return True

        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))


class RequirementView(ModelView):
    can_create = True
    can_edit = True
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

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('superuser'):
            return True

        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))


class MajorView(ModelView):
    column_filters = ['name']
    column_searchable_list = ['name']
    can_create = True
    can_edit = True

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('superuser'):
            return True

        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))


class UserView(ModelView):
    column_filters = ['email', 'confirmed_at', 'active']
    column_searchable_list = ['email']
    can_create = True
    can_edit = True

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('superuser'):
            return True

        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))


class RoleView(ModelView):
    column_filters = ['name']
    column_searchable_list = ['name']
    can_create = True
    can_edit = True

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('superuser'):
            return True

        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))

