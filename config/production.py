from config.default import *

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'leaps.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = "CcJQsNx%tf3Q79tNmuZ+#%BzAFx?pUB4s5QtcE55b9a2?v9v_x"
SECURITY_PASSWORD_SALT = "4gnah^gVP$aQEte_T6jXdXTfk98MA!9&#5XUj&T6HDs2vy6JU$"

MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USERNAME = 'leap1568@gmail.com'
MAIL_PASSWORD = 'gkawrrboakonwtvk'
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_DEFAULT_SENDER = 'CVIP'
MAIL_DEBUG = True