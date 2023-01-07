from revChatGPT.ChatGPT import Chatbot
import subprocess
import os
import json

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
                pass

        return response


class CodeGenerator():

    def __init__(self,language,program_input_description,program_output_description,
                program_description=""):

        self.init_message = "I want you to treat me as API which can take only JSON files containing fields CODE, FILENAME. "+\
                            "You will write requested code into CODE field, filename into FILENAME."+\
                            "I will send you code result in "+\
                            "following format {'Result':'Hello World'}. You will investigate code and if required you will send update, "+\
                            "code will ran successfully you will respond with empty field CODE."+\
                            "example:"+\
                            "\nWrite Python program outputting bye world:"+\
                            "\nAI:{\"CODE\":\"print(\"bye world\")\",\"FILENAME\":\"byeworld.py\"}"+\
                            "\nUSER:{\"Result\":\"bye world\"}"+\
                            f"\n\nI want you to write following in {language}. "+\
                            f"\nProgram: {program_description}"+\
                            f"\nProgram Input: {program_input_description}"+\
                            f"\nProgram Output: {program_output_description}"+\
                            f"\nRemember I am API. You are only allowed to respond with {language} syntax inside Json. Json should be in one line. Do not add any english comment or explanation inside JSON. Do not add any english comment or explanation outside JSON."

        self.chatbot = ChatTuned(self.init_message)
        # https://github.com/acheong08/ChatGPT/wiki/Setup
        self.message  = ""
        self.filename = "dummy.txt"
        pass


    def request_code(self,message):
        print("Message: \n",message)
        self.response = self.chatbot.ask(message)

        print("Response: \n",self.response)

        correct_format = False
        while not correct_format:
            try:
                first_pos   = self.response["message"].find('{')
                second_pos  = len(self.response["message"]) - self.response["message"][-1:].find('}')
                tmp_message = self.response["message"][first_pos:second_pos]

                self.message  = json.loads(tmp_message)
                correct_format = True
            except Exception as e:
                print("Exception: \n",e)

                self.response = self.chatbot.ask("{\"Result\":\""+ str(e) +"\"}")
                print("Response: \n",self.response)

        if "FILENAME" in self.message.keys():
            self.filename = self.message["FILENAME"]

        correct_format = True

    def update_file(self):
        if self.message["CODE"] != "":
            with open(self.filename,"w") as f:
                f.write(self.message["CODE"])

    def run(self):
        self.request_code(self.init_message)
        self.update_file()
        while(self.message["CODE"] != ""):
            self.run_proxy()

    def run_proxy(self):
        os.environ['PYTHONUNBUFFERED'] = '1'
        process = subprocess.Popen(f"python3 {self.filename}", shell=False, stdout=subprocess.PIPE, env=os.environ) # Shell doesn't quite matter for this issue
        while True:
            output = process.stdout.readline()
            if process.poll() is not None:
                break
            if output:
                self.request_code("{\"Result\":\""+output.decode("utf-8")+"\"}")
                self.update_file()
        rc = process.poll()
        return rc

# returns {'message':message, 'conversation_id':self.conversation_id, 'parent_id':self.parent_id}
generator = CodeGenerator("Python","No input","Hello World","Program generates random tree and performs dfs algorithm")
generator.run()