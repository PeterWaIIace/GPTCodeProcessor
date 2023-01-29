from revChatGPT.ChatGPT import Chatbot
from PromptBuilder import PromptBuilder
from PromptSanitizer import PromptSanitizer
from BlackBoxManager import BBTest
from functools import cache
import logging
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

    def __init__revChatGPT(self, config):
        # https://github.com/acheong08/ChatGPT/wiki/Setup
        self.chatbot  = Chatbot(config, conversation_id=None, parent_id=None)
        self.conversation_id = self.chatbot.conversation_id


    def stop(self):
        self.stop_override = True

    def __ask__revChatGPT(self,message):
        print("__ask__revChatGPT")

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
        print("__ask__OpenAIAPI")

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

## TMP Save JSON to file and then read it again to get proper json formatting
def response2JSON(response):
    first_pos   = response.find('{')
    second_pos  = len(response) - response[-1:].find('}')
    tmp_message = response[first_pos:second_pos]

    ps = PromptSanitizer()
    return json.loads(ps.jsonSanitizer(tmp_message))


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
        self.filename = "resources/dummy.py"

    def configure(self,prompt_file):
        with open(prompt_file,"r") as fjs:
            prompt_config     = json.load(fjs)
            self.input        = prompt_config["input"]
            self.output       = prompt_config["output"]
            self.API          = prompt_config["API"]

        self.builder = PromptBuilder("Python",self.input,self.output)

        self.chatbot = ChatTuned(self.builder.get_initial_prompt(),API=self.API)
        self.filename = "resources/dummy.py"

    def stop(self):
        self.chatbot.stop()

    def send_exception(self,e):
        return self.chatbot.ask("{\"Exception\":\""+ str(e) +"\"}. Fix JSON. No text beyond JSON.")

    def request_code(self,message):
        response = self.chatbot.ask(message)

        correct_format = False

        while not correct_format:
            try:
                response = response2JSON(response)
                correct_format = True

            except Exception as e:
                print(f"exception: {e}")
                response = self.send_exception(e)

        return response

    def update_file(self,code):
        print("updating file:",code)
        with open(self.filename,"w") as f:
            f.write(code)

    def runTest(self,code,inputs,outputs):
        nameStart = code.find("def ") + len("def ")
        nameEnd   = code.find("()")

        funcName = code[nameStart:nameEnd]

        bbTest = BBTest()
        bbTest.generateTest(funcName,code,inputs,outputs)
        return all(bbTest.runTest()) ## This will fail as wrong test report is not processed correctly

    def step(self,previous_result : str = None):
        code   = ""
        output = ""

        start=time.perf_counter()
        if previous_result:
            new_prompt    = self.builder.get_debug_prompt(previous_result)
            responseJSON  = self.request_code(new_prompt)
        else:
            init_prompt  = self.builder.get_initial_prompt()
            responseJSON = self.request_code(init_prompt)

        elapsed=time.perf_counter() - start
        print(f"Done in = f{elapsed:.2f}")

        if "CODE" in responseJSON:
            code = responseJSON["CODE"]
            self.update_file(code)

        output     = self.run_file()
        passed     = self.runTest(code,responseJSON["Inputs"],responseJSON["Outputs"])

        return output,passed

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