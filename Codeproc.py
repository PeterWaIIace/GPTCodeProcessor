from revChatGPT.ChatGPT import Chatbot
import openai
import subprocess
import json
import time
import sys
import os

class ChatTuned():

    def __init__(self,init_message,API="revChatGPT"):
        self.ask_options  = {"revChatGPT":self.__ask__revChatGPT,"OpenAIAPI":self.__ask__OpenAIAPI}
        self.init_options = {"revChatGPT":self.__init__revChatGPT,"OpenAIAPI":self.__init__OpenAIAPI}

        self.stop_override = False
        self.init_message = init_message
        self.API = API

        with open("config.json") as f:
            config = json.load(f)

        self.init_options[self.API](config[self.API])

    def __init__OpenAIAPI(self,config):
        # print(config["organization"])
        openai.organization = config["organization"]
        openai.api_key = config["apiKey"]
        print(openai.api_key)

    def __init__revChatGPT(self, config):
        self.chatbot  = Chatbot(config, conversation_id=None, parent_id=None)
        self.conversation_id = self.chatbot.conversation_id


    def stop(self):
        self.stop_override = True

    def __ask__revChatGPT(self,message):
        success = False
        response = ""

        while not success and not self.stop_override:
            try:
                response = self.chatbot.ask(message, conversation_id=self.conversation_id)
                success = True
            except Exception as e:
                print(f"Exception: {e}")
                time.sleep(10)
                pass

        self.stop_override = False
        return response["message"]

    def __ask__OpenAIAPI(self,message):
        print(openai.api_key)

        ret_completion = openai.Completion.create(
            model="text-davinci-003",
            prompt=message,
            temperature=1,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        return ret_completion["choices"][0]["text"]

    def ask(self, message):
        return self.ask_options[self.API](message)

# Prompt builder
class PromptBuilder:

    def __init__(self,language,inputParameters,outputParameters,programDescription = ""):
        self.languagePlaceholder = "Python"

        self.programDescription = programDescription
        self.inputParameters  = inputParameters
        self.outputParameters = outputParameters

        self.program_description = f"Program: {programDescription}\n"+\
            f"Program Input:  {inputParameters}\n"+\
            f"Program Output: {outputParameters}\n"

        self.init_prompt = "I want you to write program in Python. You are allowed to respond only in JSON. No explanation. No English text.\n"+\
            self.program_description+\
            "Respond with JSON having field \"CODE\" with Python code and \"Inputs\" with list of possible inputs and \"Outputs\" with respective expected outputs."

        self.init_prompt.replace(self.languagePlaceholder,language)

    def get_initial_prompt(self):
        return self.init_prompt

    def get_debug_prompt(self,output):

        # with open(filename, "r") as f:
        #     file_content = f.read()

        debug_prompt = f"Code generated following output: ```{output}```\n"+\
                             "If output is result of bug, or unexpected exception, provide fixed code in new JSON.\n"+\
                            f"If output matches expected pattern: `{self.outputParameters}` then provide answer `CODE IS CORRECT`"

        return debug_prompt
class CodeGenerator():

    def __init__(self,prompt_file):
        self.init_message = ""
        self.API = "revChatGPT"
        with open(prompt_file,"r") as fjs:
            prompt_config     = json.load(fjs)
            self.input        = prompt_config["input"]
            self.output       = prompt_config["output"]
            self.API          = prompt_config["API"]

        self.builder = PromptBuilder("Python",self.input,self.output)

        self.chatbot = ChatTuned(self.builder.get_initial_prompt(),API=self.API)
        # https://github.com/acheong08/ChatGPT/wiki/Setup
        self.filename = "resources/dummy.py"

    def stop(self):
        self.chatbot.stop()

    def send_exception(self,e):
        return self.chatbot.ask("{\"Exception\":\""+ str(e) +"\"}. Fix JSON. No text beyond JSON.")

    def request_code(self,message):
        code = ""
        self.response = self.chatbot.ask(message)

        correct_format = False

        while not correct_format:
            try:
                print(self.response)
                first_pos   = self.response.find('{')
                second_pos  = len(self.response) - self.response[-1:].find('}')
                tmp_message = self.response[first_pos:second_pos]

                code  = json.loads(tmp_message)
                correct_format = True

            except Exception as e:
                print(f"exception: {e}")
                self.response = self.send_exception(e)

        print(f"code: {code}")
        return code

    def update_file(self,code):
        print("updating file:",code)
        with open(self.filename,"w") as f:
            f.write(code)

    def step(self,previous_result : str = None):
        code   = ""
        output = ""

        print(f"Another step {previous_result}",file=sys.stdout)
        if previous_result:
            new_prompt    = self.builder.get_debug_prompt(previous_result)
            print(f"new_prompt:{new_prompt}",file=sys.stdout)
            response_json = self.request_code(new_prompt)
        else:
            init_prompt = self.builder.get_initial_prompt()
            print(f"init_prompt: {init_prompt}",file=sys.stdout)
            response_json = self.request_code(init_prompt)

        if "CODE" in response_json:
            code = response_json["CODE"]
            self.update_file(code)

        output = self.run_file()
        print(f"output: {output}")

        return output

    def run(self):
        response = None

        while True:
            response = self.step(response)

    def run_file(self):
        os.environ['PYTHONUNBUFFERED'] = '1'
        process = subprocess.Popen(f"python3 {self.filename}", shell=False, stdout=subprocess.PIPE, env=os.environ) # Shell doesn't quite matter for this issue
        while True:
            output = process.stdout.readline()

            if process.poll() is not None:
                break

        rc = process.poll()
        return output

if __name__=="__main__":
# returns {'message':message, 'conversation_id':self.conversation_id, 'parent_id':self.parent_id}
    generator = CodeGenerator("Python","No input","Hello World","Program generates and prints output")
    generator.run()