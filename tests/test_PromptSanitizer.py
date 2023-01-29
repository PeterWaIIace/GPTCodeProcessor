import json
import sys
import os
sys.path.append(os.path.abspath('..'))

from PromptSanitizer import PromptSanitizer

def test_broken_prompt_1():
    lines = ""
    correctDict = {}

    with open("BrokenPrompt1.txt", "r") as fJson:
        lines = fJson.read()

    with open("CorrectPrompt1.json", "r") as fJson:
        correctDict = json.load(fJson)

    ps = PromptSanitizer()
    sanitezedJsonString = ps.jsonSanitizer(lines)
    sanitazedJson= json.loads(sanitezedJsonString)

    with open("tmp.json","w") as fJson:
        json.dump(sanitezedJsonString,fJson)

    assert(sanitazedJson == correctDict)

def test_broken_prompt_2():
    lines = ""
    correctDict = {}

    with open("BrokenPrompt2.txt", "r") as fJson:
        lines = fJson.read()

    with open("CorrectPrompt2.json", "r") as fJson:
        correctDict = json.load(fJson)

    ps = PromptSanitizer()
    sanitezedJsonString = ps.jsonSanitizer(lines)
    sanitazedJson= json.loads(sanitezedJsonString)

    with open("tmp.json","w") as fJson:
        json.dump(sanitezedJsonString,fJson)

    assert(sanitazedJson == correctDict)

def test_broken_prompt_3():
    lines = ""
    correctDict = {}

    with open("BrokenPrompt3.txt", "r") as fJson:
        lines = fJson.read()

    with open("CorrectPrompt3.json", "r") as fJson:
        correctDict = json.load(fJson)

    ps = PromptSanitizer()
    sanitezedJsonString = ps.jsonSanitizer(lines)
    sanitazedJson= json.loads(sanitezedJsonString)

    with open("tmp.json","w") as fJson:
        json.dump(sanitezedJsonString,fJson)

    assert(sanitazedJson == correctDict)