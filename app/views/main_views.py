from flask import Blueprint, request, render_template, flash,redirect, url_for
from flask import current_app as app
from app.module.leader_borad import LeaderBoardTable
from uuid import uuid4
import zipfile
from app.forms import UserLoginForm, ModelSubmitForm
from app import db
from app.models import User
from app.views.auth_views import login_required
bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/', methods=['GET'])
def index():
    return redirect(url_for('main.main_tab'))

@bp.route('/main', methods=['GET'])
def main_tab():
    return render_template('/main/main.html')

@bp.route('/leaderboard/<task>', methods=['GET'])
def leaderboard_table(task):
    table = LeaderBoardTable(task)
    table.fetch_all()
    table.calculate_rank()
    return render_template('/main/task/{}.html'.format(task),
                           table_item=table.make_table_template())

@bp.route('/submit', methods=['GET', 'POST'])
@login_required
def submit_tab():
    form = ModelSubmitForm()
    if form.validate_on_submit() and request.method == 'POST':
        return render_template('/main/submit/submit_{}.html'.format(form.task.data), form=form)
    return render_template('/main/submit.html', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login_tab():
    return redirect('/auth/login')

@bp.route('/register', methods=['GET'])
def register_tab():
    return redirect('/auth/email_register')

