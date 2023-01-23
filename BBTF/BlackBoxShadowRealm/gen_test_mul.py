import sys

def mul(x,y):
   return x*y

test_inputs  = [[1, 1], [2, 2], [3, 3]]
test_outputs = [1, 4, 9]

if __name__=="__main__":

    passed_tests = []

    output=mul(test_inputs[0][0],test_inputs[0][1])
    passed_tests.append(output == test_outputs[0])
    output=mul(test_inputs[1][0],test_inputs[1][1])
    passed_tests.append(output == test_outputs[1])
    output=mul(test_inputs[2][0],test_inputs[2][1])
    passed_tests.append(output == test_outputs[2])
    

    sys.stdout.buffer.write(bytes(passed_tests))