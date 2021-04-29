from app import db

class SubmitModel(db.Model):
    id = db.Column(db.Integer, primary_key=True) # submit number
    task = db.Column(db.String(120), nullable=False)
    teamname = db.Column(db.String(20), nullable=False)

    submitter = db.Column(db.String(120), db.ForeignKey('user.email'))
    user = db.relationship('User', backref=db.backref('submit_model_set'))

    method = db.Column(db.String(20), nullable=False)
    code = db.Column(db.String(120), nullable=False)

    submitted_on = db.Column(db.DateTime, nullable=False)

class Losses(db.Model):
    id = db.Column(db.Integer, primary_key=True) # submit number
    name = db.Column(db.String(30), nullable=False)
    val = db.Column(db.Float, nullable=False)

    model_id = db.Column(db.Integer, db.ForeignKey('submit_model.id', ondelete='CASCADE'))
    model = db.relationship('SubmitModel', backref=db.backref('losses_set'))

class User(db.Model):
    email = db.Column(db.String(120), unique=True, nullable=False, primary_key=True)
    password = db.Column(db.String(200), nullable=False)

    nickname = db.Column(db.String(150), unique=True, nullable=False)

    student_name = db.Column(db.String(10), nullable=False)
    student_number = db.Column(db.Integer)

    #authority
    authority = db.Column(db.Boolean, nullable=False, default=False)
    authority_type = db.Column(db.Integer, nullable=False, default=0) # User
    registered_on = db.Column(db.DateTime, nullable=False)

# class LeaderBoard(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     team_name =