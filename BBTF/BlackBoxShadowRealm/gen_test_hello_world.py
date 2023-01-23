import sys

def hello_world():
   return "hello world"

test_inputs  = []
test_outputs = ['hello world']

if __name__=="__main__":

    passed_tests = []

    output=hello_world()
    passed_tests.append(output == test_outputs[0])
    

    sys.stdout.buffer.write(bytes(passed_tests))