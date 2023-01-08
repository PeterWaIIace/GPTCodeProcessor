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

    def __init__(self,language,program_input_description,program_output_description,
                program_description=""):

        self.init_message = f"I want you to write program in {language}. You are allowed to respond only in JSON. No explanation. No English text."+\
                            f"\nProgram: {program_description}"+\
                            f"\nProgram Input: {program_input_description}"+\
                            f"\nProgram Output: {program_output_description}"+\
                            f"\nRespond with JSON having one field \"CODE\" with {language} code."

        print(self.init_message)
        self.chatbot = ChatTuned(self.init_message)
        # https://github.com/acheong08/ChatGPT/wiki/Setup
        self.filename = "dummy.py"
        pass


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
        if "CODE" in code:
            with open(self.filename,"w") as f:
                f.write(code["CODE"])

    def run(self):
        code = self.request_code(self.init_message)
        self.update_file(code)

        while("CODE" in code):

            output = self.run_file()

            if output:
                code = self.request_code("{\"Result\":\""+output.decode("utf-8")+"\"}")
                self.update_file(code)


    def run_file(self):
        os.environ['PYTHONUNBUFFERED'] = '1'
        process = subprocess.Popen(f"python3 {self.filename}", shell=False, stdout=subprocess.PIPE, env=os.environ) # Shell doesn't quite matter for this issue
        while True:
            output = process.stdout.readline()

            if process.poll() is not None:
                break

        rc = process.poll()
        return output

# returns {'message':message, 'conversation_id':self.conversation_id, 'parent_id':self.parent_id}
generator = CodeGenerator("Python","No input","Hello World","Program generates and prints output")
generator.run()