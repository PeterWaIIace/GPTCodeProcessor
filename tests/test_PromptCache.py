import time
import sys
import os
sys.path.append(os.path.abspath('..'))
from PromptCache import promptCache, promptCacheClearEntry

testString = "hello mr test, it is time to print this value"
@promptCache
def some_utility(prompt):
    time.sleep(1)
    return testString + f" {prompt}"

def test_promptCache():

    testingPromtps = ["FirstPrompt","SecondPrompt","ThirdPrompt"]

    # not cached yet
    for prompt in testingPromtps:
        start = time.perf_counter()
        some_utility(prompt)
        elapsedTime = time.perf_counter() - start
        assert(0.01 < elapsedTime)

    # cached
    for prompt in testingPromtps:
        start = time.perf_counter()
        some_utility(prompt)
        elapsedTime = time.perf_counter() - start
        assert(0.01 > elapsedTime)

def test_promptCacheClearEntry():

    testingPromtps = ["FirstPrompt_ToClear","SecondPrompt_ToClear","ThirdPrompt_ToClear"]

    # not cached yet
    for prompt in testingPromtps:
        start = time.perf_counter()
        some_utility(prompt)
        elapsedTime = time.perf_counter() - start
        assert(0.01 < elapsedTime)

    # cached
    for prompt in testingPromtps:
        start = time.perf_counter()
        some_utility(prompt)
        elapsedTime = time.perf_counter() - start
        assert(0.01 > elapsedTime)

    for prompt in testingPromtps:
        promptCacheClearEntry(prompt)
        start = time.perf_counter()
        some_utility(prompt)
        elapsedTime = time.perf_counter() - start
        assert(0.01 < elapsedTime)