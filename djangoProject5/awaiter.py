from flask import Flask, request
from werkzeug.serving import make_server
from threading import Thread
from time import sleep

server = None
app = Flask('awaiter')

def stop():
    global server
    sleep(0.1)
    server.shutdown()

@app.route('/end')
def end():
    t = Thread(target=stop)
    t.start()
    return ''

server = make_server('0.0.0.0', 5000, app)
app.app_context().push()
server.serve_forever()
