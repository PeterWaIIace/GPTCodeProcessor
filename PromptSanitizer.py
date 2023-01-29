import json
import sys

class PromptSanitizer:

    def __init__(self):
        self.line_new             = ""
        self.flag_char            = False
        self.string_array         = []
        self.prev_char            = ''
        self.start_character      = '{' # required for recursive call
        self.end_character        = '}'
        self.permitted_characters = [',',':','{','}',"[","]"]

    def preprocessing(self,lines):
        lines = lines.replace('\n','\\n')
        lines = lines.replace(' ','\\s')
        return lines

    def postprocessing(self,line):
        line = line.replace('\\s',' ')
        return line

    def jsonSanitizer(self,lines):
        lines = self.preprocessing(lines)
        sanitized, _  = self.__stringToDict(lines)
        return sanitized

    def __isPayload(self,char):

        return self.flag_char

    def __stringToDict(self,lines):
        new_dict     = {}
        counter      = 0
        string_array = []

        for char in lines:

            # string_array.append(char)
            if char == "\"" and self.prev_char != '\\':
                self.flag_char = not self.flag_char
                string_array.append(char)

            if self.flag_char and not (char == "\"" and self.prev_char != '\\'):
                string_array.append(char)
                self.prev_char = char
            else:
                self.prev_char = ''
                if char in self.permitted_characters and counter > 0:
                    string_array.append(char)

            counter+=1

        postprocessed = self.postprocessing('{'+''.join(string_array))
        return postprocessed,counter

if __name__=="__main__":
    lines = ""
    print(lines)
    with open("tmp.txt", "r") as fJson:
        lines = fJson.read()

    ps = PromptSanitizer()
    new_dict = ps.dictSanitizer(lines)

    print(new_dict)
    with open("tmp.json", "w") as fJson:
        json.dump(new_dict,fJson)