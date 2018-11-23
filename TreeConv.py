import TreeNode


globData = {}
index = 0
lines = []
line = []
funclines = []
labelCounter = 0



class Stack(object):

   def __init__(self):
      self.items = []

   def push(self, item):
      self.items.append(item)

   def pop(self):
       return self.items.pop()

   def peek(self):
       return self.items[-1]

   def isEmpty(self):
       return len(self.items) == 0

loopStack = Stack()
conStack = Stack()

def test(root):
    global lines
    global index
    #print("arrived")
    getGlobals(root.children[0])
    if(index>0):
        lines.append("int global[" + str(index) + "];")
    funcDec(root.children[1])
    #printTree(root, 0,0)
    for l in lines:
        print(l)
    return lines
    #getLocals(root.children[1])


def funcDec(node):
    if node.data == "func_decl":
        appender(node)
        return
    if node.data == "func_prime":
        controller = node.children[0]
        if(controller.data == ";"):
            line.append(";")
            pushToMaster()
            return
        elif(controller.data == "{"):
            line.append("{")
            pushToMaster()
            locData = []
            locData = funcAssign(node.children[1],locData)
            global index
            index = len(locData)
            locDict = listToDict(locData)
            changeVar(node.children[2], locDict)
            statements(node.children[2])
            pushFunc()
    for c in node.children:
        funcDec(c)


def changeVar(node, dict):
    if node.data in dict:
        key = dict.get(node.data)
        node.data = key
    elif(node.data in globData):
        key = globData.get(node.data)
        node.data = key
    for c in node.children:
        changeVar(c, dict)

def statements(node):
    global labelCounter
    global funclines
    global loopStack
    global conStack
    for child in node.children:
        if(child.data == "statement"):
            if child.children[0].data == "break_statement":
                funclines.append("goto "+loopStack.peek()+";")
                return
            if child.children[0].data == "continue_statement":
                funclines.append("goto "+conStack.peek()+";")
                return
            if child.children[0].data == "if_statement":
                procLab = ""
                altLab = ""
                nIf = child.children[0]
                stringbuilder = "if("
                for z in nIf.children:
                    if z.data == "condition_expression":
                        stringbuilder+=(statementIdent(z))
                        procLab = "L_"+str(labelCounter)
                        stringbuilder+=")goto "+procLab+";"
                        funclines.append(stringbuilder)
                        labelCounter+=1
                        altLab = "L_"+str(labelCounter)
                        funclines.append("goto "+altLab+";")
                        labelCounter+=1
                    if z.data == "block_statements":
                        funclines.append(procLab+":;")
                        for s in z.children:
                            if s.data == "statements":
                                statements(s)
                    if z.data == "if_statement_prime":
                        funclines.append(altLab + ":;")
                        for s in z.children:
                            if s.data == "block_statements":
                                eLab = "L_" + str(labelCounter)
                                labelCounter += 1
                                funclines.append("goto "+eLab+";")
                                for k in s.children:
                                    if k.data == "statements":
                                        statements(k)
                                funclines.append(eLab+":;")


            elif child.children[0].data == "while_statement":
                tLab = "L_" + str(labelCounter)
                labelCounter += 1
                wLab = "L_" + str(labelCounter)
                labelCounter += 1
                bLab = "L_" + str(labelCounter)
                labelCounter += 1
                loopStack.push(bLab)
                conStack.push(tLab)
                nIf = child.children[0]
                stringbuilder = "if("
                size = len(nIf.children)
                for z in reversed(nIf.children):
                    if z.data == "condition_expression":
                        stringbuilder += (statementIdent(z))
                        stringbuilder += ")goto " + wLab + ";"
                        funclines.append(stringbuilder)


                    if z.data == "block_statements":
                        funclines.append("goto " + tLab + ";")
                        funclines.append(wLab + ":;")
                        for k in z.children:
                            if k.data == "statements":
                                statements(k)
                        funclines.append(tLab+":;")
                funclines.append(bLab+":;")
                loopStack.pop()
                conStack.pop()

            else:
                funclines.append(statementIdent(child.children[0]))
                #print(funclines)
        if(child.data == "statements"):
            statements(child)

def statementIdent(node):
    global funclines
    if(node.data == "factor" or  node.data == "term" or node.data == "term_prime"):
        lineBuilder = []
        for child in node.children:
            lineBuilder.append(statementIdent(child))
        global index
        factor = str("local["+str(index)+"]")
        stringbuilder = factor+"="
        for l in lineBuilder:
            stringbuilder+=l
        stringbuilder+=";"
        funclines.append(stringbuilder)
        index+=1
        return factor
    elif(node.code):
        if node.data == "return":
            node.data = node.data+" "
        return node.data
    else:
        resline = ""
        for child in node.children:
            if(child.data == "identifier"):
                for x in child.children:
                    if (x.data == "read"):
                        return stateRead(node)
            resline+=statementIdent(child)
        return resline




def stateRead(node):
    stringbuilder = ""
    if (node.code):
        stringbuilder+=node.data
    for child in node.children:
        stringbuilder+=stateRead(child)
    return stringbuilder

def listToDict(locData):
    cnt = 0
    locDict = {}
    for i in locData:
        locDict[i] = "local["+str(cnt)+"]"
        cnt+=1
    return locDict


def funcAssign(node, locData):
    if node.data == "data_decl":
        locData = funcIdent(node, locData)
        #print(locData)
    return locData

def funcIdent(node, locData):
    if(node.data == "identifier"):
        locData.append(node.children[0].data)
    for c in node.children:
        locData = funcIdent(c, locData)
    return locData




def appender(node):
    global line
    if(node.code):
        line.append(node.data)
    for c in node.children:
        appender(c)

def pushToMaster():
    global line
    global lines
    stringBuilder = ""
    for i in line:
        stringBuilder += str(i)+" "
    lines.append(stringBuilder)
    line = []

def pushFunc():
    global index
    global funclines
    global lines
    if index>0:
        lines.append("  int local[" + str(index) + "];")
    for i in funclines:
        lines.append("  "+str(i))
    last = funclines[len(funclines)-1]
    lines.append("}")
    index = 0
    funclines = []


def getGlobals(curr):
    global index
    if curr.data == "func_list":
        return
    else:
        if curr.data == "identifier":
            #print(curr.children[0].data)
            if(curr.children[0].data in globData):
                key = globData.get(curr.children[0].data)
                curr.children[0].data = key
            else:
                globData[curr.children[0].data] = "global["+str(index)+"]"
                curr.children[0].data = "global["+str(index)+"]"
                index+=1
    for child in curr.children:
        getGlobals(child)





def printTree(n, level, size):
    print(' '*size +'      '*(level-1) + '+-----'*(level > 0) + n.data)
    size += len(n.data)
    for child in n.children:
        printTree(child, level+1, size)
