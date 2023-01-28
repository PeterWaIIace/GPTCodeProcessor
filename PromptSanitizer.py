import json

def dictSanitizer(lines):
    lines = lines.replace('\n','\\n')
    lines = lines.replace(' ','\\s')

    line_new = ""
    flag_char = False
    string_array = []
    prev_char = ''
    divider = ','
    keyValueGrouper = ':'
    permitted_characters = ["{","}","[","]"]

    new_dict = {}

    counter = 0
    for char in lines:
        if char == "\"" and prev_char != '\\':
            flag_char = not flag_char
            # string_array.append(char)
        else:
            if flag_char:
                string_array.append(char)
                prev_char = char
            else:
                prev_char = ''
                if char in permitted_characters and counter > 0:
                    string_array.append(char)

                if char in divider:
                    value = ''.join(string_array)
                    key = key.replace('\\s',' ')
                    key = key.replace('\\n','\n')
                    value = value.replace('\\s',' ')
                    value = value.replace('\\n','\n')
                    value = value.replace('\\\"','\"')

                    new_dict[key] = value
                    string_array = []

                if char in keyValueGrouper:
                    key = ''.join(string_array)
                    string_array = []

        counter+=1

    return new_dict

if __name__=="__main__":
    lines = ""
    print(lines)
    with open("tmp.txt", "r") as fJson:
        lines = fJson.read()

    new_dict = dictSanitizer(lines)

    print(new_dict)
    with open("tmp.json", "w") as fJson:
        json.dump(new_dict,fJson)