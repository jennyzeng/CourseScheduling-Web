from flask_debugtoolbar import DebugToolbarExtension
from flask_mongoengine import MongoEngine, MongoEngineSessionInterface


debug_toolbar = DebugToolbarExtension()
db = MongoEngine()
mongoInterface = MongoEngineSessionInterface(db)
