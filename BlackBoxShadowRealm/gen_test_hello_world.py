import sys

def hello_world():
              print("Hello world")

test_inputs  = []
test_outputs = ['Hello world']

if __name__=="__main__":

    passed_tests = []

    output=hello_world()
    passed_tests.append(output == test_outputs[0])
    

    sys.stdout.buffer.write(bytes(passed_tests))