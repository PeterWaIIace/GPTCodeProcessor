# WIP

def hello_world():
   print("hello world")

test_inputs  = []
test_outputs = ["hello world"]

if __name__=="__main__":

    passed_tests = []

    for n,_ in enumerate(test_outputs):

        if(len(test_inputs) > n):
            output = hello_world(test_inputs[n])
            passed_tests.append(output == test_outputs[n])
        else:
            output = hello_world()
            passed_tests.append(output == test_outputs[n])

    print(not all(passed_tests)) # this statement will return result to stdout