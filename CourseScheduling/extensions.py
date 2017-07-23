from flask_debugtoolbar import DebugToolbarExtension
from flask_mongoengine import MongoEngine, MongoEngineSessionInterface
from CourseScheduling.blueprints.admin.views import HomeView
from flask_admin import Admin



debug_toolbar = DebugToolbarExtension()
db = MongoEngine()
mongoInterface = MongoEngineSessionInterface(db)
admin = Admin(name='MongoAdmin', index_view=HomeView())
