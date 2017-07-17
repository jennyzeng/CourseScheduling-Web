from flask_debugtoolbar import DebugToolbarExtension
from flask_mongoengine import MongoEngine, MongoEngineSessionInterface

import flask_admin as admin


debug_toolbar = DebugToolbarExtension()
db = MongoEngine()
mongoInterface = MongoEngineSessionInterface(db)
admin = admin.Admin(name='MongoAdmin')