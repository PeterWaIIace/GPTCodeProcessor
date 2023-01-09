from revChatGPT.ChatGPT import Chatbot
import subprocess
import json
import time
import os

class ChatTuned():

    def __init__(self,init_message):
        self.init_message = init_message

        with open("config.json") as f:
            config = json.load(f)

        self.chatbot  = Chatbot(config, conversation_id=None, parent_id=None)
        self.conversation_id = self.chatbot.conversation_id

        self.response = self.ask(self.init_message)

    def ask(self, message):
        success = False
        response = ""

        while not success:
            try:
                response = self.chatbot.ask(message, conversation_id=self.conversation_id)
                success = True
            except Exception as e:
                print(f"Exception: {e}")
                time.sleep(10)
                pass

        return response["message"]


class CodeGenerator():

    def __init__(self,prompt_file):
        self.init_message = ""
        with open(prompt_file,"r") as fjs:
            self.init_message = json.load(fjs)["prompt"]

        print(self.init_message)

        self.chatbot = ChatTuned(self.init_message)
        # https://github.com/acheong08/ChatGPT/wiki/Setup
        self.filename = "resources/dummy.py"

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

# if __name__=="__main__":
# returns {'message':message, 'conversation_id':self.conversation_id, 'parent_id':self.parent_id}
    # generator = CodeGenerator("Python","No input","Hello World","Program generates and prints output")
    # generator.run()