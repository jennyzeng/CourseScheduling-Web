
DEBUG = True

SERVER_NAME = "localhost:8000"

SECRET_KEY = 'insecurekeyfordev'
SECURITY_PASSWORD_HASH = "sha512_crypt"
SECURITY_PASSWORD_SALT = "5gz"
SECURITY_POST_LOGIN_VIEW = 'admin/'
SECURITY_POST_LOGOUT_VIEW = 'admin/'

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
DEBUG_TB_INTERCEPT_REDIRECTS = False

# file upload in admin
UPLOAD_FOLDER = '/CourseScheduling/database/txt_files/'

