DEBUG = True

SERVER_NAME = "localhost:8000"

SECRET_KEY = 'insecurekeyfordev'

# MONGODB_SETTINGS = {
#     'db':'CS-database',
#     'host': 'mongodb://localhost/CS-database'#,
#     # 'port': 27017
# }
MONGODB_HOST = 'mongodb'
MONGODB_PORT = 27017
MONGODB_DB = 'CS-database'


DEBUG_TB_PANELS = (
    'flask_debugtoolbar.panels.versions.VersionDebugPanel',
    'flask_debugtoolbar.panels.timer.TimerDebugPanel',
    'flask_debugtoolbar.panels.headers.HeaderDebugPanel',
    'flask_debugtoolbar.panels.request_vars.RequestVarsDebugPanel',
    'flask_debugtoolbar.panels.template.TemplateDebugPanel',
    'flask_debugtoolbar.panels.logger.LoggingPanel',
    # 'flask_mongoengine.panels.MongoDebugPanel'
)