functionDescriptionPlaceholder = "<functionDescription>"
inputParametersPlaceholder = "<inputParameters>"
outputParametersPlaceholder = "<outputParameters>"
languagePlaceholder = "<LANGUAGE>"

promptFileName = "prompt.txt"

class PromptBuilder:

    def __init__(self,language,inputParameters,outputParameters,functionDescription = ""):

        prompt = ""
        with open(promptFileName,"r") as f:
            prompt = f.read()

        prompt = prompt.replace(languagePlaceholder,language)
        prompt = prompt.replace(functionDescriptionPlaceholder,functionDescription)
        prompt = prompt.replace(inputParametersPlaceholder ,inputParameters)
        prompt = prompt.replace(outputParametersPlaceholder,outputParameters)

        print(prompt)
        self.init_prompt = prompt

    def get_initial_prompt(self):
        print(self.init_prompt)
        return self.init_prompt

    def get_debug_prompt(self,output):

        # with open(filename, "r") as f:
        #     file_content = f.read()

        debug_prompt = f"Code generated following output: ```{output}```\n"+\
                             "If output is result of bug, or unexpected exception, provide fixed code in new JSON.\n"+\
                            f"If output matches expected pattern: `{self.outputParameters}` then provide answer `CODE IS CORRECT`"

        return debug_prompt