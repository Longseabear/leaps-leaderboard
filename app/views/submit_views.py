from flask import Blueprint, request, render_template, flash,redirect, url_for, g, session, jsonify
from datetime import datetime
import os
import io
from app.module.logics import LossProcessor, PreProcessor
from app.forms import UserLoginForm, ModelSubmitForm
from app import db
import config.default as config
import json
from app.models import User, SubmitModel, Losses
from app.views.auth_views import login_required
bp = Blueprint('submit', __name__, url_prefix='/submit')

@bp.route('/task_finish', methods=['POST'])
@login_required
def task_finish():
    form = ModelSubmitForm()
    client_data = json.loads(request.form['datas'])
    session_data = session.get('model')

    if not session_data:
        return ajax_response(False, {'status': 'Fail: Session error. please retry.'})

    if session_data['count'] != client_data['count'] or not session_data['finish']:
        session_data.clear()
        return ajax_response(False, {'status': 'Fail: Server-client consistency check failed. Please approach it in the normal way.'})

    try:
        submit_model = SubmitModel(task=session_data['task'],
                                   teamname=form.teamname.data,
                                   user=g.user,
                                   method=form.method.data,
                                   code=form.code.data,
                                   submitted_on=datetime.now())
        db.session.add(submit_model)
        for loss_name in session_data['losses'].keys():
            db.session.add(Losses(name=loss_name,
                                  val=session_data['losses'][loss_name],
                                  model=submit_model))
        db.session.commit()
    except Exception as e:
        session_data.clear()
        return ajax_response(False, {
            'status': 'Database error occurred: {}'.format(e)
        })
    session_data.clear()
    return ajax_response(True, {})

@bp.route('/task_init', methods=['POST'])
@login_required
def task_init():
    if not config.MODEL_SUBMIT_POSSIBLE:
        return ajax_response(False, {'status': '[CLOSE] Submission is closed.'})

    session_data = session.get('model')
    form = ModelSubmitForm()
    if session_data:
        session_data.clear()

    if not form.validate_on_submit():
        return ajax_response(False, {'status': '[ERROR] please check input form. content: {}'.format(form.errors)})

    task = form.task.data
    if task not in config.TASK_MODELS.keys():
        return ajax_response(False, {'status': '[ERROR] Task {} is not implemented.'.format(task)})

    model = config.TASK_MODELS[task]
    session_data = {
        'count': 0,
        'task': task,
        'losses': {},
    }
    for loss in model.losses:
        session_data['losses'][loss] = 0.0
    session['model'] = session_data

    client_data = {
        'count': 0,
        'total': model.total,
        'next_required': model.file_list[0]
    }
    return ajax_response(True, client_data)

@bp.route('/task_processing', methods=['POST'])
@login_required
def task_processing():
    form = ModelSubmitForm()
    session_data = session.get('model')
    if not session_data:
        return ajax_response(False, {'status': 'Fail: Only one processing is possible per session.'})
    task = session_data['task']

    current_count = session_data['count']
    session_data['count'] += 1
    client_data = json.loads(request.form['datas'])
    raw = json.loads(request.form['file'])

    if current_count != int(client_data['count']):
        session_data.clear()
        return ajax_response(False, {'status': 'Fail: The order of data is broken. Only one processing per session is possible.'})

    # processing
    current_model = config.TASK_MODELS[task]
    gt_path = os.path.join(current_model.label_path, current_model.file_list[current_count])
    pred, label = PreProcessor.factory(current_model.input_type).preprocess(raw, gt_path)
    losses = LossProcessor(task).calculate(pred, label)

    if current_model.total == current_count+1:
        session_data['finish'] = True
    else:
        client_data['next_required'] = current_model.file_list[current_count + 1]

    for loss_name in losses.keys():
        session_data['losses'][loss_name] = session_data['losses'][loss_name] * (current_count / (current_count+1)) + losses[loss_name] / (current_count+1)

    #commit
    session['model'] = session_data

    client_data['server_message'] = ' '.join(['{}: {}'.format(loss, session_data['losses'][loss]) for loss in losses.keys()])
    return ajax_response(True, client_data)

def ajax_response(status, datas, error_number=500):
    status_code = 200 if status else error_number
    return jsonify(dict(
        **datas
    )), status_code

