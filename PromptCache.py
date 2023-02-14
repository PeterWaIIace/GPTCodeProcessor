import sys

cachedVars = {}

def promptCache(func):

    def promptWrapper(self=None,prompt=""):
        if prompt in cachedVars:
            return cachedVars[prompt]
        else:
            ret_val = None
            if self == None:
                ret_val = func(prompt)
            else:
                ret_val = func(self,prompt)
            cachePrompt(prompt,ret_val)
            return ret_val

    return promptWrapper

def promptCacheClearEntry(prompt):
    cachedVars.pop(prompt,cachedVars[prompt])

def cachePrompt(prompt,retVal):
    cachedVars[prompt] = retVal