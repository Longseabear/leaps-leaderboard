from itsdangerous import URLSafeTimedSerializer
from flask import current_app as app

def generate_confirmation_token(email):
    serial = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serial.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])

def confirm_token(token, expiration=3600):
    serial = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serial.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except Exception as e:
        return None
    return email
