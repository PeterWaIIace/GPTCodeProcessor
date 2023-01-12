from revChatGPT.ChatGPT import Chatbot
import openai
import subprocess
import json
import time
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
        # print(openai.Model.list())

    def __init__revChatGPT(self, config):
        self.chatbot  = Chatbot(config, conversation_id=None, parent_id=None)
        self.conversation_id = self.chatbot.conversation_id

        self.response = self.ask(self.init_message)


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


class CodeGenerator():

    def __init__(self,prompt_file):
        self.init_message = ""
        self.API = "revChatGPT"
        with open(prompt_file,"r") as fjs:
            prompt_config     = json.load(fjs)
            self.init_message = prompt_config["prompt"]
            self.API          = prompt_config["API"]

        print(self.init_message)

        self.chatbot = ChatTuned(self.init_message,API=self.API)
        # https://github.com/acheong08/ChatGPT/wiki/Setup
        self.filename = "resources/dummy.py"

    def stop(self):
        self.chatbot.stop()

    def send_exception(self,e):
        return self.chatbot.ask("{\"Exception\":\""+ str(e) +"\"}. Fix JSON. No text beyond JSON.")

    def send_program_output(self,e):
        return self.chatbot.ask("{\"Output\":\""+ str(e) +"\"}")

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

    def step(self,previous_result=None):
        code   = ""
        output = ""

        if previous_result:
            response_json = self.request_code(self.init_message)
        else:
            response_json = self.request_code(self.init_message)

        if "CODE" in response_json:
            print("response_json: ",response_json)
            code = response_json["CODE"]
            output = self.update_file(code)

        return output


    def run(self):
        response = None

        while True:
            self.step(response)

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