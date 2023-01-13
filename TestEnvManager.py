# WIP
import subprocess
import os

class EnvironmentManager:

    def __init__(self,envFilePath="resources",envFileName="python_test_env.py"):
        self.ptrFuncBody       = "<TESTED_FUNCTION_BODY>"
        self.ptrFuncInvocation = "<TESTED_FUNCTION_CALL>"
        self.ptrInputs         = "<TEST_INPUTS>"
        self.ptrOutputs        = "<TEST_OUTPUTS>"

        self.envFilePath = envFilePath
        self.envFileName = envFileName
        self.envBaseFileName = "environmentBase.py"

        self.fullPathToBase = self.envFilePath + "/" + self.envBaseFileName
        self.fullPathToTest = self.envFilePath + "/" + self.envFileName

    def generateTest(self,funcName="",funcBody="",inputs=[],outputs=[]):

        fileContent = ""

        with open(self.fullPathToBase, "r") as f:
            fileContent = f.read()

        fileContent = fileContent.replace(self.ptrFuncBody,funcBody)
        fileContent = fileContent.replace(self.ptrFuncInvocation,funcName)
        fileContent = fileContent.replace(self.ptrInputs,f"{inputs}")
        fileContent = fileContent.replace(self.ptrOutputs,f"{outputs}")

        with open(self.fullPathToTest, "w") as f:
            f.write(fileContent)

    def runTest(self):
        os.environ['PYTHONUNBUFFERED'] = '1'
        process = subprocess.Popen(f"python3 {self.fullPathToTest}", shell=False, stdout=subprocess.PIPE, env=os.environ) # Shell doesn't quite matter for this issue
        while True:
            tmp_output = process.stdout.readline()
            if tmp_output:
                output = process.stdout.readline()

            if process.poll() is not None:
                break

        rc = process.poll()
        result = (b'True' in output)
        return result


evnM = EnvironmentManager()
evnM.generateTest("hello_world","def hello_world():\n   print(\"hello world\")","[]","[\"hello world\"]");

print(evnM.runTest())