import json
import sys
import os
sys.path.append(os.path.abspath('..'))

from PromptSanitizer import dictSanitizer

def test_broken_prompt_1():
    lines = ""
    correctDict = {}

    with open("BrokenPrompt1.txt", "r") as fJson:
        lines = fJson.read()

    with open("CorrectPrompt1.json", "r") as fJson:
        correctDict = json.load(fJson)

    new_dict = dictSanitizer(lines)
    assert(new_dict == correctDict)

def test_broken_prompt_2():
    lines = ""
    correctDict = {}

    with open("BrokenPrompt2.txt", "r") as fJson:
        lines = fJson.read()

    with open("CorrectPrompt2.json", "r") as fJson:
        correctDict = json.load(fJson)

    new_dict = dictSanitizer(lines)
    with open("tmp.json","w") as fJson:
        json.dump(new_dict,fJson)
    assert(new_dict == correctDict)

def test_broken_prompt_3():
    lines = ""
    correctDict = {}

    with open("BrokenPrompt3.txt", "r") as fJson:
        lines = fJson.read()

    with open("CorrectPrompt3.json", "r") as fJson:
        correctDict = json.load(fJson)

    new_dict = dictSanitizer(lines)
    assert(new_dict == correctDict)