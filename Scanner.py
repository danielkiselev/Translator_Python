import sys
import os
import Token as token
import Node
import GrammarAnalyzer
import TreeNode
import TreeConv

'''
Takes in the parameter opens the file. We store then iterate through each line in the data set passing them into
the lineParser function and store the results in lineData1. We then make a new file with the same name as the original
in "c_out" folder. We then iterate through lineData1 and write each line into the new file.
'''
def scan(filePath):
    filePath = str(filePath)
    fileName = os.path.basename(filePath)
    f = None
    try:
        original = filePath
        f = open(original, 'r+')
    except IOError:
        print("Error: File does not appear to exist.")
        sys.exit(0)
    lineData0 = []#original
    lineData1 = []#result
    resData = []
    for line in f:
        lineData0.append(line)
        outLine = lineParser(line)
        lineData1.append(outLine)
    f.close()
    root = None
    curr = None
    counter = 1
    for line in lineData1:
        counter+=1
        for t in line:
            if(t.lex != "meta_statement" ):
                n = Node.node(t, None)
                if(root == None):
                    root = n
                    curr = root
                else:
                    curr.next = n
                    curr = n
            else:
                resData.append(t.value)
    t = token.Token("end","end")
    n = Node.node(t, None)
    curr.next = n
    curr = root
    while(curr.next != None):
        curr = curr.next
    root = GrammarAnalyzer.program(root)
    #printTree(root, 0, 0)
    premerge = TreeConv.test(root)
    for l in premerge:
        resData.append(l+'\n')
    #print("------------Result------------")
    f.close()

    clone = fileName
    out = open(clone, 'w')
    out.writelines(resData)
    out.close()

def printTree(n, level, size):
    print(' '*size +'      '*(level-1) + '+-----'*(level > 0) + n.data)
    size += len(n.data)
    for child in n.children:
        printTree(child, level+1, size)

'''
Iterates through the passed in line and puts the result into String lineBuilder as we go along. This is done by
tokenizing each individual character string and if it is a digit or letter we add it to a string called stringbuilder.
Once we get something that tells us that it's a new token such as a space or symbol we classify the stringbuilder using
classifystring function. Then we add the resulting token's value into linebuilder and clear the contents of 
stringbuilder. I obviously coded in some cases for comments, meta statements, and other wacky edge cases.
'''
def lineParser(line):
    lineBuilder = ""
    StringBuilder = ""
    TokenTracker = []
    stringStatus = False
    stringStatusBuilder = ""
    metaStatement = False
    meta = False
    lineTokens = []
    for i in line:
        curr = str(i)
        if metaStatement:
            StringBuilder+=curr
            continue
        if curr == '"':
            if stringStatus:
                stringStatusBuilder += curr
                locT = token.Token(stringStatusBuilder, "string")
                lineTokens.append(locT)
                stringStatusBuilder = ""
                stringStatus = False
            else:
                if (len(StringBuilder) > 0):
                    classifiedToken = classifyString(StringBuilder, TokenTracker)
                    lineBuilder += classifiedToken.value
                    StringBuilder = ""
                    TokenTracker = []
                stringStatusBuilder += curr
                stringStatus = True
            lineBuilder+=curr
            continue
        if stringStatus:
            stringStatusBuilder += curr
            lineBuilder+=curr
            continue
        if(curr == "/"):
            if len(lineBuilder)>0:
                if (lineBuilder[len(lineBuilder) - 1] == "/" and len(StringBuilder)==0):
                    lineTokens.pop()
                    StringBuilder=""
                    StringBuilder+="//"
                    metaStatement = True
                    continue
        if(curr == "#"):
            StringBuilder = ""
            StringBuilder += "#"
            metaStatement = True
            continue
        t = token.Token(curr, None)
        if(curr != " " and t.lex == "letter" or t.lex == "digit"):
            StringBuilder+=t.value
            TokenTracker.append(t.lex)
        elif(t.lex == "symbol" or curr == " "):
            if (len(StringBuilder)>0):
                if(meta):
                    if(lineBuilder[len(lineBuilder)-1] == "#"):
                        if(StringBuilder == "include"):
                            lineBuilder += StringBuilder
                            lineBuilder += curr
                            StringBuilder = ""
                            metaStatement = True
                            meta = False
                        else:
                            lineBuilder += StringBuilder
                            lineBuilder += curr
                            StringBuilder = ""
                            meta = False

                else:
                    classifiedToken = classifyString(StringBuilder, TokenTracker)
                    lineTokens.append(classifiedToken)
                    lineBuilder+=classifiedToken.value
                    StringBuilder = ""
                    TokenTracker = []
                    lineBuilder+=curr
                    if(t.lex != None):
                        lineTokens.append(t)
            else:
                StringBuilder = ""
                TokenTracker = []
                lineBuilder += curr
                if (t.lex != None):
                    lineTokens.append(t)
        else:
            lineBuilder+=curr
    if(metaStatement):
        t = token.Token(StringBuilder,"meta_statement")
        lineTokens.append(t)
    else:
        if(len(StringBuilder) > 0):
            classifiedToken = classifyString(StringBuilder, TokenTracker)
            lineTokens.append(classifiedToken)
            lineBuilder += classifiedToken.value
            StringBuilder = ""
            TokenTracker = []
            lineBuilder += curr
            if (t.lex != None):
                lineTokens.append(t)

    return lineTokens


'''
takes in a String called StringBuilder and TokenTracker which is an array of each character's token classification.
We use it to classify the collection of individual character as an identifier and a number. We also watch out for
illegal token and throw an error
'''
def classifyString(StringBuilder, TokenTracker):
    temp = token.Token(StringBuilder, None)
    lexClassifier = None
    if(temp.lex != "reserved word"):
        for t in TokenTracker:
            if(lexClassifier is None):
                if t == "letter":
                    lexClassifier = "identifier"
                elif t == "digit":
                    lexClassifier = "number"
            else:
                if t == "letter":
                    if(lexClassifier == "number"):
                        print("Abort scanning and report illegal token "+'"'+StringBuilder+'".')
                        sys.exit(0)
    else:
        lexClassifier =  "reserved word"
    if(lexClassifier == "identifier"):
        pass
    resToken = token.Token(StringBuilder, lexClassifier)
    return resToken

