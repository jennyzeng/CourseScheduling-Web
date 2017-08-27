from flask import Flask, url_for, render_template

from CourseScheduling.blueprints.page import page
from CourseScheduling.blueprints.schedule import schedule
from CourseScheduling.extensions import debug_toolbar, db, mongoInterface, admin
from CourseScheduling.blueprints.schedule.models import Course, Requirement, Major, Quarter
from CourseScheduling.blueprints.admin.views import (CourseView, RequirementView, QuarterView,
                                                     MajorView, UserView, RoleView)
from CourseScheduling.blueprints.admin.fileUpload import FileUploadView
from CourseScheduling.blueprints.user.models import User, Role
from flask_security import MongoEngineUserDatastore
from flask_admin import helpers as admin_helpers
from flask_security import Security
import flask_login as login
from CourseScheduling.blueprints.admin.views import HomeView


security = None


def create_app(settings_override=None):
    """
    Create a Flask application using the app factory pattern.

    :param settings_override: Override settings
    :return: Flask app
    """
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object('config.settings')
    app.config.from_pyfile('settings.py', silent=True)

    if settings_override:
        app.config.update(settings_override)
    error_templates(app)

    app.register_blueprint(page)
    app.register_blueprint(schedule)
    extensions(app)

    return app


def extensions(app):
    """
    Register 0 or more extensions (mutates the app passed in).

    :param app: Flask application instance
    :return: None
    """
    debug_toolbar.init_app(app)
    db.init_app(app)

    app.session_interface = mongoInterface
    # init login
    init_login(app)
    # Setup Flask-Security
    user_datastore = MongoEngineUserDatastore(db, User, Role)
    security = Security(app, user_datastore)
    # add admin view

    admin.init_app(app, index_view=HomeView())
    # admin.index_view =
    admin.add_view(CourseView(Course))
    admin.add_view(RequirementView(Requirement))
    admin.add_view(MajorView(Major))
    admin.add_view(QuarterView(Quarter))
    admin.add_view(UserView(User))
    admin.add_view(RoleView(Role))
    admin.add_view(FileUploadView(name='Course Upload', endpoint='upload'))
    # define a context processor for merging flask-admin's template context into the
    # flask-security views.
    @security.context_processor
    def security_context_processor():
        return dict(
            admin_base_template=admin.base_template,
            admin_view=admin.index_view,
            h=admin_helpers,
            get_url=url_for
        )

    # Create a user to test with
    @app.before_first_request
    def create_user():
        user_datastore.find_or_create_role(name='superuser', description='Administrator')
        user_datastore.find_or_create_role(name='user', description='User')
        if not user_datastore.get_user('admin'):
            user_datastore.create_user(email='admin', password='admin')
        user_datastore.add_role_to_user('admin', 'superuser')

    return None


def init_login(app):
    login_manager = login.LoginManager()
    login_manager.init_app(app)

    # Create user loader function
    @login_manager.user_loader
    def load_user(user_id):
        return User.objects(id=user_id).first()


def error_templates(app):
    """
    Register 0 or more custom error pages (mutates the app passed in).

    :param app: Flask application instance
    :return: None
    """

    def render_status(status):
        """
         Render a custom template for a specific status.
           Source: http://stackoverflow.com/a/30108946

         :param status: Status as a written name
         :type status: str
         :return: None
         """
        # Get the status code from the status, default to a 500 so that we
        # catch all types of errors and treat them as a 500.
        code = getattr(status, 'code', 500)
        return render_template('errors/{0}.html'.format(code)), code

    for error in [404, 429, 500]:
        app.errorhandler(error)(render_status)

    return None
