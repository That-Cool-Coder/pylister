import simpleFileManager as files

def countLines(fileName=None, code=None):
    code = chooseFileOrCode(fileName, code)

    return code.count('\n')

def countCodeLines(fileName=None, code=None):
    code = chooseFileOrCode(fileName, code)

    return countLines(code=code) - countCommentLines(code=code) - countBlankLines(code=code)

def countCommentLines(fileName=None, code=None):
    code = chooseFileOrCode(fileName, code)

    lines = code.split('\n')
    commentLines = 0
    for line in lines:
        line = line.strip()
        if len(line) > 0:
            if line[0] == '#':
                commentLines += 1
    
    return commentLines

def countBlankLines(fileName=None, code=None):
    code = chooseFileOrCode(fileName, code)

    lines = code.split('\n')
    blankLines = 0
    for line in lines:
        line = line.strip()
        if len(line) == 0:
            blankLines += 1
    
    return blankLines

def countClasses(fileName=None, code=None):
    code = chooseFileOrCode(fileName, code)

    return code.count('class ')

def countFunctions(fileName=None, code=None):
    code = chooseFileOrCode(fileName, code)

    return code.count('def ')

def countBranches(fileName=None, code=None):
    code = chooseFileOrCode(fileName, code)

    branchKeywords = ['if', 'elif', 'else']

    tokens = code.split(' ')
    tokens = [t.strip() for t in tokens]

    branches = 0
    for keyword in branchKeywords:
        branches += tokens.count(keyword)
    
    return branches

def countLoops(fileName=None, code=None):
    code = chooseFileOrCode(fileName, code)
    
    loopKeywords = ['for', 'while']

    tokens = code.split(' ')
    tokens = [t.strip() for t in tokens]

    loops = 0
    for keyword in loopKeywords:
        loops += tokens.count(keyword)
    
    return loops

def countTryExcepts(fileName=None, code=None):
    code = chooseFileOrCode(fileName, code)

    return code.count('try:')

def chooseFileOrCode(fileName, code):
    if code is not None:
        return code
    elif fileName is not None:
        return files.read(fileName)
    else:
        raise BaseException