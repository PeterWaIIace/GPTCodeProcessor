from bottle import route, run
import bottle
import os

@bottle.route('/')
def index():
    root = os.path.join(os.path.dirname(__file__), 'bottle_frontend')
    return bottle.static_file('index.html', root=root)

@bottle.route('/<filename>')
def interfaces(filename="interface.js"):
    root = os.path.join(os.path.dirname(__file__), 'bottle_frontend')
    return bottle.static_file(filename, root=root)

@bottle.route('/read/<filename>')
def readFiles(filename="dummy.py"):
    root = os.path.join(os.path.dirname(__file__), 'resources')
    return bottle.static_file(filename, root=root)

@bottle.post('/buttons/start')
def buttonStart():
    print(bottle.request.json)



run(host='localhost', port=8080, debug=True)