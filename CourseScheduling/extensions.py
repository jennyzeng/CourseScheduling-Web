from flask_debugtoolbar import DebugToolbarExtension
from flask_mongoengine import MongoEngine, MongoEngineSessionInterface
from flask_admin import Admin


debug_toolbar = DebugToolbarExtension()
db = MongoEngine()
mongoInterface = MongoEngineSessionInterface(db)
admin = Admin(name='Admin', base_template='admin/mymaster.html',url='/admin')
