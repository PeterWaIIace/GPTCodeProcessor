# WIP
import subprocess
import os
class EnvironmentManager:

    def __init__(self,envFilePath="resources",envFileName="python_test_env.py"):
        self.ptrFuncBody       = "<TESTED_FUNCTION_BODY>"
        self.ptrFuncInvocation = "<TESTED_FUNCTION_CALLS>"
        self.ptrInputs         = "<TEST_INPUTS>"
        self.ptrOutputs        = "<TEST_OUTPUTS>"

        self.envFilePath = envFilePath
        self.envFileName = envFileName
        self.envBaseFileName = "environmentBase.py"

        self.fullPathToBase = self.envFilePath + "/" + self.envBaseFileName
        self.fullPathToTest = self.envFilePath + "/" + self.envFileName

    def __inputListToStr(self,inputs=[],n=0):
        allInputs = ""
        # get list of inputs
        if(hasattr(inputs[n], '__iter__')): # will fail for string what is good
            for i,_ in enumerate(inputs[n]):
                if i:
                    allInputs += f",test_inputs[{n}][{i}]"
                else:
                    allInputs += f"test_inputs[{n}][{i}]"
        else:
            allInputs += f"test_inputs[{n}]"

        return allInputs

    def generateTest(self,funcName="",funcBody="",inputs=[],outputs=[]):

        fileContent = ""

        with open(self.fullPathToBase, "r") as f:
            fileContent = f.read()

        fileContent = fileContent.replace(self.ptrFuncBody,funcBody)

        for n,_ in enumerate(outputs):
            if len(inputs) > n:
                functionCall = f"output={funcName}({self.__inputListToStr(inputs,n)})\n"+\
                               f"    passed_tests.append(output == test_outputs[{n}])\n"+\
                               f"    {self.ptrFuncInvocation}"
                fileContent = fileContent.replace(self.ptrFuncInvocation,functionCall)

            else:
                functionCall = f"output={funcName}()\n"+\
                               f"    passed_tests.append(output == test_outputs[{n}])\n"+\
                               f"    {self.ptrFuncInvocation}"
                fileContent = fileContent.replace(self.ptrFuncInvocation,functionCall)

        fileContent = fileContent.replace(self.ptrFuncInvocation,"") # clean last call
        fileContent = fileContent.replace(self.ptrInputs,f"{inputs}")
        fileContent = fileContent.replace(self.ptrOutputs,f"{outputs}")

        with open(self.fullPathToTest, "w") as f:
            f.write(fileContent)

    def runTest(self):
        os.environ['PYTHONUNBUFFERED'] = '1'
        process = subprocess.Popen(f"python3 {self.fullPathToTest}", shell=False, stdout=subprocess.PIPE, env=os.environ) # Shell doesn't quite matter for this issue
        output = b''

        while True:
            tmp_output = process.stdout.readline()
            if tmp_output != b'':
                output = tmp_output

            if process.poll() is not None:
                break

        rc = process.poll()
        result = (b'True' in output)
        return result


evnM = EnvironmentManager(envFileName="gen_test_hello_world.py")
evnM.generateTest("hello_world","def hello_world():\n   return \"hello world\"",[],["hello world"]);

print(evnM.runTest())

evnM = EnvironmentManager(envFileName="gen_test_mul.py")
evnM.generateTest("mul","def mul(x,y):\n   return x*y",[[1,1],[2,2],[3,3]],[1,4,9])

print(evnM.runTest())
