from bottle   import route, run
from Codeproc import CodeGenerator
import threading
import bottle
import json
import os

prompt_file = "initprompt.json"
generate = False
generator_thread = None

def codeGenThread():
    global generate
    generator = CodeGenerator(prompt_file)
    response = None

    while generate:
        generator.step(response)

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
    global generate, generator_thread

    print(bottle.request.json)
    with open(prompt_file,'w') as fjs:
        json.dump(bottle.request.json,fjs)

    generate = True
    generator_thread = threading.Thread(target=codeGenThread)
    generator_thread.run()


@bottle.post('/buttons/stop')
def buttonStart():
    global generate, generator_thread
    generate = False
    generator_thread.join()

run(host='localhost', port=8080, debug=True)