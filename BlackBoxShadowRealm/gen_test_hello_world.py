import sys

def hello_world():
  return 'Hello World63'

test_inputs  = []
test_outputs = Hello World63

if __name__=="__main__":

    passed_tests = []

    output=hello_world()
    passed_tests.append(output == test_outputs[0])
    output=hello_world()
    passed_tests.append(output == test_outputs[1])
    output=hello_world()
    passed_tests.append(output == test_outputs[2])
    output=hello_world()
    passed_tests.append(output == test_outputs[3])
    output=hello_world()
    passed_tests.append(output == test_outputs[4])
    output=hello_world()
    passed_tests.append(output == test_outputs[5])
    output=hello_world()
    passed_tests.append(output == test_outputs[6])
    output=hello_world()
    passed_tests.append(output == test_outputs[7])
    output=hello_world()
    passed_tests.append(output == test_outputs[8])
    output=hello_world()
    passed_tests.append(output == test_outputs[9])
    output=hello_world()
    passed_tests.append(output == test_outputs[10])
    output=hello_world()
    passed_tests.append(output == test_outputs[11])
    output=hello_world()
    passed_tests.append(output == test_outputs[12])
    

    sys.stdout.buffer.write(bytes(passed_tests))