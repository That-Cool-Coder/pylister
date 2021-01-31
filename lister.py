import simpleFileManager as files

def countFunctions(fileName=None, code=None):
    code = chooseFileOrCode(fileName, code)

    return code.count('def ')

def countLines(fileName=None, code=None):
    code = chooseFileOrCode(fileName, code)

    return code.count('\n')

def chooseFileOrCode(fileName, code):
    if code is not None:
        return code
    elif fileName is not None:
        return files.read(fileName)
    else:
        raise BaseException