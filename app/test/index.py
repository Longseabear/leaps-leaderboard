
import time
import json
from flask import Blueprint, request, render_template, flash, redirect, url_for, Response, session, jsonify
from flask import current_app as current_app
import config
from app.module import dbModule
import copy
from app.forms import ModelSubmitForm

test = Blueprint('test', __name__, url_prefix='/test')

@test.route('/', methods=['GET'])
def index():
    return render_template('/main/auth/register_user.html',form = {'email':'a', 'password':'b'}, errors=None)

from PIL import Image
import io
import numpy as np

@test.route('/zip_test', methods=['POST'])
def zip_test():
    datas = request.json
    filename = datas['filename']
    bytedata = datas['bytes']
    print(type(bytedata))
    import matplotlib.pyplot as plt
    img = np.array(Image.open(io.BytesIO(bytearray(bytedata))))
    img = img[:, :, :3] / 255.
    plt.imshow(img)
    plt.show()
    return ajax_response(True, {})

@test.route('/task_finish', methods=['POST'])
def task_finish():
    print('finish')
    model = session.get('model')
    if not model:
        return ajax_response(False, request.json)

    datas = request.json
    if model['count'] != datas['count'] or not model['finish']:
        model.clear()
        return ajax_response(False, request.json)

    # db 등록하고 / 성공메세지 보낸다.

    model.clear()
    return ajax_response(True, request.json)

@test.route('/task_test', methods=['POST'])
def task_test():
    print('start')
    model = session.get('model')
    if not model:
        print(model)
        return ajax_response(False, request.json)

    current_count = model['count']
    model['count'] += 1

    datas = request.json
    if current_count != datas['count']:
        print(current_count, datas['count'])
        model.clear()
        return ajax_response(False, request.json)

    print('processing: {}'.format(current_count))
    time.sleep(1)
    print('finish. next to {}'.format(model['count']))

    if model['total'] == current_count+1:
        model['finish'] = True
    session['model'] = model
    return ajax_response(True, request.json)

@test.route('/task_init', methods=['POST'])
def task_init():
    model = session.get('model')
    form = ModelSubmitForm()
    if model:
        model.clear()

    if not form.validate_on_submit():
        return ajax_response(False, {'status': '[ERROR] please check validate'})

    task = form.task
    if task not in config.TASK_MODELS.keys():
        pass
    models = copy.deepcopy(config.TASK_MODELS)

#    session['model']
    return ajax_response(False, {'msg':'[ERROR] '})

def ajax_response(status, datas, error_number=500):
    status_code = 200 if status else error_number
    return jsonify(dict(
        **datas
    )), status_code


# INSERT 함수 예제
@test.route('/insert', methods=['GET'])
def insert():
    def generate():
        x = 0
        while x <= 100:
            yield "data:" + str(x) + "\n\n"
            x = x + 10
            time.sleep(0.5)

    return Response(generate(), mimetype='text/event-stream')

    # db = dbModule.DB()
    #
    # query = "INSERT INTO testDB.testTable(test) \
    #             VALUES('%s')" % ('testData')
    #
    # cur.executemany(query, purchases)
    # con.commit()
    #
    # db_class.execute(sql)
    # db_class.commit()
    # return render_template('/test/test.html',
    #                        result='insert is done!',
    #                        resultData=None,
    #                        resultUPDATE=None)
#
#
# # SELECT 함수 예제
# @test.route('/select', methods=['GET'])
# def select():
#     db_class = dbModule.Database()
#
#     sql = "SELECT idx, test \
#                 FROM testDB.testTable"
#     row = db_class.executeAll(sql)
#
#     print(row)
#
#     return render_template('/test/test.html',
#                            result=None,
#                            resultData=row[0],
#                            resultUPDATE=None)
#
#
# # UPDATE 함수 예제
# @test.route('/update', methods=['GET'])
# def update():
#     db_class = dbModule.Database()
#
#     sql = "UPDATE testDB.testTable \
#                 SET test='%s' \
#                 WHERE test='testData'" % ('update_Data')
#     db_class.execute(sql)
#     db_class.commit()
#
#     sql = "SELECT idx, test \
#                 FROM testDB.testTable"
#     row = db_class.executeAll(sql)
#
#     return render_template('/test/test.html',
#                            result=None,
#                            resultData=None,
#                            resultUPDATE=row[0])

