from bottle   import route, run
from Codeproc import CodeGenerator
import threading
import bottle
import json
import time
import os

prompt_file = "initprompt.json"
generator = None
generate = False
generator_thread = None
latest_response = ""
generatorEngine = CodeGenerator(prompt_file)

def codeGenThread():
    global generate,latest_response,generator
    response = None

    while generate:
        response,passed = generatorEngine.step(response)
        latest_response = response
        print(passed)
        time.sleep(10)
        if(passed):
            generate = False

    print("Generator Stopped")

@bottle.route('/')
def index():
    root = os.path.join(os.path.dirname(__file__), 'bottle_frontend')
    return bottle.static_file('index.html', root=root)

@bottle.route('/<filename>')
def interfaces(filename="interface.js"):
    root = os.path.join(os.path.dirname(__file__), 'bottle_frontend')
    return bottle.static_file(filename, root=root)

@bottle.route('/GPTresponse')
def getLatestResponse():
    global latest_response
    return latest_response

@bottle.route('/read/<filename>')
def readFiles(filename="dummy.py"):
    root = os.path.join(os.path.dirname(__file__), 'resources')

    response = bottle.static_file(filename, root=root)
    response.set_header("Cache-Control", "public, max-age=1")
    return response

@bottle.post('/buttons/start')
def buttonStart():
    global generate, generator_thread

    print(bottle.request.json)
    with open(prompt_file,'w') as fjs:
        json.dump(bottle.request.json,fjs)

    generate = True
    generatorEngine.configure(prompt_file)
    generator_thread = threading.Thread(target=codeGenThread)
    generator_thread.start()


@bottle.post('/buttons/stop')
def buttonStart():
    global generate, generator_thread
    print("STOPPING")
    generate = False

    if generator != None:
        generator.stop()
    generator_thread.join()

run(host='localhost', port=8080, debug=None, quiet=True)