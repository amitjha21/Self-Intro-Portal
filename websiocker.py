from gevent import monkey
monkey.patch_all()
from flask import Flask, render_template, request, url_for, jsonify
from flask_socketio import SocketIO ,send, emit
import time, sys, eventlet
# import gevent
from io import StringIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
try:
    socketio = SocketIO(app, async_mode="eventlet")
except:
    print("conn issue")

def ack():
    print ('Ack: message was received!')

def print_exec(code):
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    exec(code)
    sys.stdout = old_stdout
    return redirected_output.getvalue()

@app.route("/", methods=['GET'])
def home():
    return "<h4>App is running</h4>"

@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)
    a= print_exec(message)
    # print(a)
    emit('python',a, json=True)

@socketio.on('json')
def handle_json(json):
    print('received jsonfrom client: ' + str(json))
    send(json, json=True)

@socketio.on('my event')
def handle_my_custom_event(arg1, arg2, arg3):
    print('received args: ' + arg1 + arg2 + arg3)
    emit('my response', (arg1, arg2,arg3), callback=ack)

# Broadcasting
@socketio.on('board')
def handle_broad(data):
    emit('my broadcasted response', data, broadcast=True)

if __name__ == '__main__':

    # context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    # context.load_cert_chain('cert.pem','key.pem')
    # socketio.run(app, ssl_context=context, debug=True )
    #eventlet.wsgi.server(eventlet.wrap_ssl(eventlet.listen(('0.0.0.0', 5000)), certfile='cert.pem', keyfile='key.pem',server_side=True), app)
    socketio.run(app, host='0.0.0.0', port=50001, debug=True, keyfile='key.pem', certfile='cert.pem')
