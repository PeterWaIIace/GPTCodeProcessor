# WIP

<TESTED_FUNCTION_BODY>

test_inputs  = <TEST_INPUTS>
test_outputs = <TEST_OUTPUTS>

if __name__=="__main__":

    passed_tests = []

    for n,_ in enumerate(test_outputs):

        if(len(test_inputs) > n):
            output = <TESTED_FUNCTION_CALL>(test_inputs[n])
            passed_tests.append(output == test_outputs[n])
        else:
            output = <TESTED_FUNCTION_CALL>()
            passed_tests.append(output == test_outputs[n])

    print(not all(passed_tests)) # this statement will return result to stdout