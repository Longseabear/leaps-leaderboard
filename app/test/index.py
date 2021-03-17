
import time
from flask import Blueprint, request, render_template, flash, redirect, url_for, Response
from flask import current_app as current_app

from app.module import dbModule

test = Blueprint('test', __name__, url_prefix='/test')

@test.route('/', methods=['GET'])
def index():
    return render_template('/test/test.html',
                           result=None,
                           resultData=None,
                           resultUPDATE=None)


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