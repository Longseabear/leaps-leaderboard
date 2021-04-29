from app import socketIO
import time

@socketIO.on('task')
# required (g -> submit model)
def handle_my_custom_event(json, methods=['GET','POST']):
    print('received event: ' + str(json))
    for i in range(10):
        time.sleep(1)
        socketIO.emit('{}'.format(i))