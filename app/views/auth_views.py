import datetime
import functools

from flask import Blueprint, url_for, render_template, flash, request, current_app, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect
from app import db, mail

from app.forms import UserCreateForm, EmailForm, UserLoginForm
from app.models import User
from app.token import generate_confirmation_token, confirm_token
from app.mail import send_email

bp = Blueprint('auth', __name__, url_prefix='/auth')

# decorator
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            flash('required login.', 'danger')
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

# routing
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            error = "There are no matching emails."
        elif not check_password_hash(user.password, form.password.data):
            error = "incorrect password."

        if error is None:
            session.clear()
            session['user_id'] = user.email
            if user.authority_type == 1:
                session['admin_mode'] = True
            return redirect('/')
        flash(error, 'danger')
    return render_template('main/auth/login.html', form=form)

@bp.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect('/')

@bp.route('/email_register', methods=('GET', 'POST'))
def email_register():
    form = EmailForm()
    if request.method == 'POST':
        form.email.data = form.email_name.data + current_app.config['REGISTRATION_EMAIL_DOMAIN']
        if form.validate_on_submit():
            email = User.query.filter_by(email=form.email.data).first()
            if not email:
                token = generate_confirmation_token(form.email.data)
                flash('{}으로 이메일이 전송되었습니다. 전송된 URL을 통하여 회원가입을 진행해주십시오.'.format(form.email.data), 'info')
                confirm_url = url_for('auth.confirm_email', token=token, _external=True)
                contents = render_template('/constant/email.html', confirm_url=confirm_url)
                send_email(form.email.data, '[CVIP] email verification', contents)
                return redirect('/')
            else:
                flash('email already exist.', 'danger')
    return render_template('/main/auth/register.html', form=form)

@bp.route('/confirm/<token>', methods=('GET', 'POST'))
def confirm_email(token):
    email = None
    try:
        email = confirm_token(token)
    finally:
        if email is None:
            flash('The confirmation link is invalid or has expired.', 'danger')
            return redirect('/')

    form = UserCreateForm()
    form.email.data = email
    if request.method == 'POST' and form.validate_on_submit():
        email = User.query.filter_by(email=form.email.data).first()
        nickname = User.query.filter_by(email=form.nickname.data).first()

        if not email and not nickname:
            user = User(email=form.email.data,
                        password=generate_password_hash(form.password1.data),
                        student_name=form.student_name.data,
                        student_number=form.student_number.data,
                        nickname=form.nickname.data,
                        authority=True,
                        authority_type=0,  # User
                        registered_on=datetime.datetime.now())
            db.session.add(user)
            db.session.commit()
            flash('Registration finished. Please login.', category='info')
            return redirect('/')
        else:
            if email: flash('The email already exists.', category='danger')
            if nickname: flash('The nickname already exists.', category='danger')
            return redirect('/')

    return render_template('/main/auth/register_user.html', form=form)
