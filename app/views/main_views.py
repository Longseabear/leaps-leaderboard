from flask import Blueprint, request, render_template, flash,redirect, url_for
from flask import current_app as app

main = Blueprint('main', __name__, url_prefix='/')

@main.route('/', methods=['GET'])
def index():
    return redirect(main)

@main.route('/main', methods=['GET'])
def main_tab():
    # database에서 얻어오고 ~ 
    return render_template('/main/main.html')

@main.route('/colorization', methods=['GET'])
def colorization_tab():
    return render_template('/main/colorization.html')


