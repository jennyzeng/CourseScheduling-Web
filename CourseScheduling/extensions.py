from flask_debugtoolbar import DebugToolbarExtension
from flask_mongoengine import MongoEngine


debug_toolbar = DebugToolbarExtension()
db = MongoEngine()