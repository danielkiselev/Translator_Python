import Token
import TreeNode as tN

num_functions = 0
num_variables = 0
num_statements = 0
root = tN.treeNode("program", False)

def program(currNode):
    global num_functions
    global num_variables
    global num_statements
    global root
    currTree = root
    data_decls_node = tN.treeNode("data_decl",False)
    func_list_node = tN.treeNode("func_list",False)
    currTree.addChild(data_decls_node)
    currTree.addChild(func_list_node)
    currNode = data_decls(currNode, data_decls_node)
    resNode = func_list(currNode,func_list_node)
    if(resNode.data.value != "end"):
        print("Error")
    return root







def data_decls(currNode, currTree):
    global num_variables
    type_name_node = tN.treeNode("type_name",False)
    id_list_node = tN.treeNode("id_list",False)
    data_decls_node = tN.treeNode("data_decl",False)
    resNode = currNode
    currTree.addChild(type_name_node)
    resNode = type_name(resNode, type_name_node)
    if(resNode is None):
        currTree.children = []
        return currNode
    currTree.addChild(id_list_node)
    resNode = id_list(resNode, id_list_node)
    if(resNode is None):
        currTree.children = []
        return currNode
    if(resNode.data.value == ";"):
        end_node = tN.treeNode(";",True)
        currTree.addChild(end_node)
        resNode = resNode.next
    else:
        num_variables -= 1
        currTree.children = []
        return currNode
    currTree.addChild(data_decls_node)
    currNode = data_decls(resNode, data_decls_node)
    return currNode




def func_list(currNode, currTree):#done
    resNode = currNode
    func_node = tN.treeNode("func",False)
    currTree.addChild(func_node)
    resNode = func(resNode, func_node)
    if(resNode is None):
        return currNode
    func_list_node = tN.treeNode("func_list",False)
    currTree.addChild(func_list_node)
    resNode = func_list(resNode, func_list_node)
    return resNode


def func(currNode, currTree):
    resNode = currNode
    func_decl_node = tN.treeNode("func_decl",False)
    currTree.addChild(func_decl_node)
    resNode = func_decl(resNode, func_decl_node)
    if resNode is None:
        currTree.data = "E"
        currTree.children = []
        return None
    n1 = tN.treeNode("func_prime",False)
    currTree.addChild(n1)
    return func_prime(resNode, n1)


def func_prime(currNode, currTree):
    resNode = currNode
    if (resNode.data.value == ";"):
        n1 = tN.treeNode(";", True)
        currTree.addChild(n1)
        resNode = resNode.next
        return resNode
    elif (resNode.data.value == "{"):
        n2 = tN.treeNode("{",True)
        currTree.addChild(n2)
        resNode = resNode.next
        n5 = tN.treeNode("data_decl",False)
        currTree.addChild(n5)
        resNode = data_decls(resNode,n5)
        n4 = tN.treeNode("statements",False)
        currTree.addChild(n4)
        resNode = statements(resNode, n4)
        if (resNode.data.value == "}"):
            n3 = tN.treeNode("}", True)
            currTree.addChild(n3)
            global num_functions
            global num_variables
            num_functions += 1
            resNode = resNode.next
            return resNode
        else:
            currTree.data = "E"
            currTree.children = []
            return None

    currTree.data = "E"
    currTree.children = []
    return None

def func_decl(currNode, currTree):
    n0 = tN.treeNode("type_name",False)
    currTree.addChild(n0)
    currNode = type_name(currNode,n0)
    if(currNode is None):
        currTree.data = "E"
        currTree.children = []
        return None
    n1 = tN.treeNode("identifier",False)
    currTree.addChild(n1)
    currNode = identifier(currNode,n1)
    if(currNode is None):
        currTree.data = "E"
        currTree.children = []
        return None
    if(currNode.data.value == "("):
        currNode = currNode.next
        n2 = tN.treeNode("(", True)
        currTree.addChild(n2)
    else:
        currTree.data = "E"
        currTree.children = []
        return None
    n3 = tN.treeNode("parameter_list", False)
    currTree.addChild(n3)
    currNode = parameter_list(currNode,n3)
    if(currNode is None):
        currTree.data = "E"
        currTree.children = []
        return None
    if(currNode.data.value == ")"):
        n4 = tN.treeNode(")", True)
        currTree.addChild(n4)
        currNode = currNode.next
    else:
        currTree.data = "E"
        currTree.children = []
        return None
    return currNode

def type_name(currNode, currTree):

    if(currNode.data.value == "int"):
        t = tN.treeNode("int", True)
        currTree.addChild(t)
        return currNode.next
    if(currNode.data.value == "void"):
        t = tN.treeNode("void", True)
        currTree.addChild(t)
        return currNode.next
    return None

def parameter_list(currNode, currTree):
    t1 = tN.treeNode("non_empty_list", False)
    currTree.addChild(t1)
    resNode = non_empty_list(currNode,t1)
    if (resNode is not None):
        return resNode
    if(currNode.data.value == "void"):
        t = tN.treeNode("void", True)
        currTree.addChild(t)
        return currNode.next
    return currNode



def non_empty_list(currNode, currTree):
    resNode = currNode
    t = tN.treeNode("type_name", False)
    currTree.addChild(t)
    resNode = type_name(resNode,t)
    if (resNode is None):
        currTree.data = "E"
        currTree.children = []
        return None
    t1 = tN.treeNode("identifier", False)
    currTree.addChild(t1)
    resNode = identifier(resNode,t1)
    if (resNode is None):
        currTree.data = "E"
        currTree.children = []
        return None
    t2 = tN.treeNode("non_empty_list_prime", False)
    currTree.addChild(t2)
    resNode = non_empty_list_prime(resNode,t2)
    return resNode

def non_empty_list_prime(currNode, currTree):
    resNode = currNode
    if resNode.data.value == ",":
        t3 = tN.treeNode(",", True)
        currTree.addChild(t3)
        resNode = resNode.next
    else:
        
        return currNode
    t0 = tN.treeNode("type_name",False)
    currTree.addChild(t0)
    resNode = type_name(resNode,t0)
    if (resNode is None):
        
        return currNode
    t1 = tN.treeNode("identifier",False)
    currTree.addChild(t1)
    resNode = identifier(resNode, t1)
    if (resNode is None):
        
        return currNode
    return resNode

def id_list(currNode, currTree):
    resNode = currNode
    t1 = tN.treeNode("identifier",False)
    currTree.addChild(t1)
    resNode = identifier(resNode, t1)
    if (resNode is None):
        currTree.data = "E"
        currTree.children = []
        return None
    t2 = tN.treeNode("id_list_prime",False)
    currTree.addChild(t2)
    resNode = id_list_prime(resNode,t2)
    if (resNode is None):
        currTree.data = "E"
        currTree.children = []
        return None
    return resNode

def id_list_prime(currNode, currTree):
    global num_variables
    num_variables+=1
    resNode = currNode
    if resNode.data.value == ",":
        currTree.addChild(tN.treeNode(resNode.data.value, True))
        resNode = resNode.next
        if(resNode is None):
            return currNode
        t1 = tN.treeNode("identifier",False)
        currTree.addChild(t1)
        resNode = identifier(resNode, t1)
        if(resNode is None):
            return currNode
        t2 = tN.treeNode("id_list_prime",False)
        currTree.addChild(t2)
        currNode = id_list_prime(resNode,t2)
    return currNode


def identifier(currNode, currTree):
    if currNode.data.lex == "identifier":
        t0 = tN.treeNode(currNode.data.value, True)
        currTree.addChild(t0)
        currNode = currNode.next
    else:
        currTree.data = "E"
        currTree.children = []
        return None
    t1 = tN.treeNode("identifier_prime",False)
    currTree.addChild(t1)
    currNode = identifier_prime(currNode,t1)
    return currNode

def identifier_prime(currNode, currTree):
    resNode = currNode
    if resNode.data.value == "[":
        currTree.addChild(tN.treeNode(resNode.data.value, True))
        resNode = resNode.next
        t1 = tN.treeNode("expression",False)
        currTree.addChild(t1)
        resNode = expression(resNode,t1)
        if(resNode is None):
            return currNode
        if resNode.data.value == "]":
            currTree.addChild(tN.treeNode(resNode.data.value, True))
            resNode = resNode.next
            return resNode
    return currNode


def block_statements(currNode, currTree):
    resNode = currNode
    if resNode.data.value == "{":
        t5 = tN.treeNode("{", True)
        currTree.addChild(t5)
        resNode = resNode.next
    else:
        currTree.data = "E"
        currTree.children = []
        return None
    t1 = tN.treeNode("statements",False)
    currTree.addChild(t1)
    resNode = statements(resNode,t1)
    if (resNode is None):
        currTree.data = "E"
        currTree.children = []
        return None
    if resNode.data.value == "}":
        t5 = tN.treeNode("}", True)
        currTree.addChild(t5)
        resNode = resNode.next
    else:
        currTree.data = "E"
        currTree.children = []
        return None
    return resNode

def statements(currNode, currTree):
    resNode = currNode
    t1 = tN.treeNode("statement",False)
    currTree.addChild(t1)
    resNode = statement(resNode,t1)
    if resNode is None:
        return currNode
    t2 = tN.treeNode("statements",False)
    currTree.addChild(t2)
    return statements(resNode,t2)

def statement(currNode, currTree):
    global num_statements
    t1 = tN.treeNode("statement_ident",False)
    resNode = statement_ident(currNode,t1)
    if resNode is not None:
        currTree.addChild(t1)
        num_statements+=1
        return resNode
    t2 = tN.treeNode("printf_func_call",False)
    resNode = printf_func_call(currNode,t2)
    if resNode is not None:
        currTree.addChild(t2)
        num_statements += 1
        return resNode
    t3 = tN.treeNode("scanf_func_call",False)
    resNode = scanf_func_call(currNode,t3)
    if resNode is not None:
        currTree.addChild(t3)
        num_statements += 1
        return resNode
    t4 = tN.treeNode("if_statement",False)
    resNode = if_statement(currNode,t4)
    if resNode is not None:
        currTree.addChild(t4)
        num_statements += 1
        return resNode
    t5 = tN.treeNode("while_statement",False)
    resNode = while_statement(currNode,t5)
    if resNode is not None:
        currTree.addChild(t5)
        num_statements += 1
        return resNode
    t6 = tN.treeNode("return_statement",False)
    resNode = return_statement(currNode,t6)
    if resNode is not None:
        currTree.addChild(t6)
        num_statements += 1
        return resNode
    t7 = tN.treeNode("break_statement",False)
    resNode = break_statement(currNode,t7)
    if resNode is not None:
        currTree.addChild(t7)
        num_statements += 1
        return resNode
    t8 = tN.treeNode("continue_statement",False)
    resNode = continue_statement(currNode,t8)
    if resNode is not None:
        currTree.addChild(t8)
        num_statements += 1
        return resNode
    currTree.data = "E"
    currTree.children = []
    return None


def statement_ident(currNode, currTree):
    resNode = currNode
    t1 = tN.treeNode("identifier",False)
    currTree.addChild(t1)
    resNode = identifier(resNode, t1)
    if resNode is None:
        currTree.data = "E"
        currTree.children = []
        return None
    t2 = tN.treeNode("statement_ident_prime",False)
    currTree.addChild(t2)
    return statement_ident_prime(resNode,t2)

def statement_ident_prime(currNode, currTree):
    resNode = currNode
    if(resNode.data.value == "="):
        t1 = tN.treeNode("assignment",False)
        currTree.addChild(t1)
        resNode = assignment(resNode,t1)
    elif(resNode.data.value == "("):
        t2 = tN.treeNode("general_func_call",False)
        currTree.addChild(t2)
        resNode = general_func_call(resNode,t2)
    return resNode



def assignment(currNode, currTree):
    resNode = currNode
    if resNode.data.value == "=":
        currTree.addChild(tN.treeNode(resNode.data.value,True))
        resNode = resNode.next
    else:
        currTree.data = "E"
        currTree.children = []
        return None
    t2 = tN.treeNode("expression",False)
    currTree.addChild(t2)
    resNode = expression(resNode,t2)
    if resNode is None:
        currTree.data = "E"
        currTree.children = []
        return None
    if resNode.data.value == ";":
        currTree.addChild(tN.treeNode(resNode.data.value,True))
        resNode = resNode.next
    else:
        currTree.data = "E"
        currTree.children = []
        return None
    return resNode




def general_func_call(currNode, currTree):

    resNode = currNode
    if resNode.data.value == "(":
        currTree.addChild(tN.treeNode(resNode.data.value, True))
        resNode = resNode.next
    else:
        currTree.data = "E"
        currTree.children = []
        return None
    t2 = tN.treeNode("expr_list",False)
    currTree.addChild(t2)
    resNode = expr_list(resNode,t2)
    if resNode is None:
        currTree.data = "E"
        currTree.children = []
        return None
    if resNode.data.value == ")":
        currTree.addChild(tN.treeNode(resNode.data.value,True))
        resNode = resNode.next
    else:
        currTree.data = "E"
        currTree.children = []
        return None
    if resNode.data.value == ";":
        currTree.addChild(tN.treeNode(resNode.data.value, True))
        resNode = resNode.next
    else:
        currTree.data = "E"
        currTree.children = []
        return None
    return resNode

def printf_func_call(currNode, currTree):

    resNode = currNode
    if resNode.data.value == "printf":
        currTree.addChild(tN.treeNode(resNode.data.value, True))
        resNode = resNode.next
    else:
        currTree.data = "E"
        currTree.children = []
        return None
    if resNode.data.value == "(":
        currTree.addChild(tN.treeNode(resNode.data.value, True))
        resNode = resNode.next
    else:
        currTree.data = "E"
        currTree.children = []
        return None
    if resNode.data.lex == "string":
        currTree.addChild(tN.treeNode(resNode.data.value, True))
        resNode = resNode.next
    else:
        currTree.data = "E"
        currTree.children = []
        return None
    t2 = tN.treeNode("printf_func_call_prime", False)
    currTree.addChild(t2)
    return printf_func_call_prime(resNode,t2)



def printf_func_call_prime(currNode, currTree):
    resNode = currNode
    if resNode.data.value == ",":
        currTree.addChild(tN.treeNode(resNode.data.value, True))
        resNode = resNode.next
        t2 = tN.treeNode("expression", False)
        currTree.addChild(t2)
        resNode = expression(resNode,t2)
        if resNode is None:
            currTree.data = "E"
            currTree.children = []
            return None
    if resNode.data.value == ")":
        currTree.addChild(tN.treeNode(resNode.data.value, True))
        resNode = resNode.next
    else:
        currTree.data = "E"
        currTree.children = []
        return None
    if resNode.data.value == ";":
        currTree.addChild(tN.treeNode(resNode.data.value, True))
        resNode = resNode.next
    else:
        currTree.data = "E"
        currTree.children = []
        return None
    return resNode


def scanf_func_call(currNode, currTree):

    resNode = currNode
    if resNode.data.value == "scanf":
        currTree.addChild(tN.treeNode(resNode.data.value, True))
        resNode = resNode.next
    else:
        currTree.data = "E"
        currTree.children = []
        return None
    if resNode.data.value == "(":
        currTree.addChild(tN.treeNode(resNode.data.value, True))
        resNode = resNode.next
    else:
        currTree.data = "E"
        currTree.children = []
        return None
    if resNode.data.lex == "string":
        currTree.addChild(tN.treeNode(resNode.data.value, True))
        resNode = resNode.next
    else:
        currTree.data = "E"
        currTree.children = []
        return None
    if resNode.data.value == ",":
        currTree.addChild(tN.treeNode(resNode.data.value, True))
        resNode = resNode.next
    else:
        currTree.data = "E"
        currTree.children = []
        return None
    if resNode.data.value == "&":
        currTree.addChild(tN.treeNode(resNode.data.value, True))
        resNode = resNode.next
    else:
        currTree.data = "E"
        currTree.children = []
        return None
    t2 = tN.treeNode("expression", False)
    currTree.addChild(t2)
    resNode = expression(resNode,t2)
    if resNode is None:
        currTree.data = "E"
        currTree.children = []
        return None
    if resNode.data.value == ")":
        currTree.addChild(tN.treeNode(resNode.data.value, True))
        resNode = resNode.next
    else:
        currTree.data = "E"
        currTree.children = []
        return None
    if resNode.data.value == ";":
        currTree.addChild(tN.treeNode(resNode.data.value, True))
        resNode = resNode.next
    else:
        currTree.data = "E"
        currTree.children = []
        return None
    return resNode

def expr_list(currNode, currTree):

    resNode = currNode
    t2 = tN.treeNode("non_empty_expr_list", False)
    currTree.addChild(t2)
    resNode = non_empty_expr_list(resNode,t2)
    if resNode is None:
        return currNode
    return resNode

def non_empty_expr_list(currNode, currTree):

    resNode = currNode
    t2 = tN.treeNode("expression", False)
    currTree.addChild(t2)
    resNode = expression(resNode,t2)
    if resNode is None:
        currTree.data = "E"
        currTree.children = []
        return None
    t0 = tN.treeNode("non_empty_expr_list_prime", False)
    currTree.addChild(t0)
    return non_empty_expr_list_prime(resNode, t0)

def non_empty_expr_list_prime(currNode, currTree):

    resNode = currNode
    if resNode.data.value == ",":
        currTree.addChild(tN.treeNode(resNode.data.value, True))
        resNode = resNode.next
    else:
        return currNode
    t2 = tN.treeNode("expression", False)
    currTree.addChild(t2)
    resNode = expression(resNode,t2)
    if resNode is None:
        return currNode
    t0 = tN.treeNode("non_empty_expr_list_prime", False)
    currTree.addChild(t0)
    return non_empty_expr_list_prime(resNode,t0)

def if_statement(currNode, currTree):

    resNode = currNode
    if resNode.data.value == "if":
        currTree.addChild(tN.treeNode(resNode.data.value, True))
        resNode = resNode.next
    else:
        currTree.data = "E"
        currTree.children = []
        return None
    if resNode.data.value == "(":
        currTree.addChild(tN.treeNode(resNode.data.value, True))
        resNode = resNode.next
    else:
        currTree.data = "E"
        currTree.children = []
        return None
    t2 = tN.treeNode("condition_expression", False)
    currTree.addChild(t2)
    resNode = condition_expression(resNode,t2)
    if resNode is None:
        currTree.data = "E"
        currTree.children = []
        return None
    if resNode.data.value == ")":
        currTree.addChild(tN.treeNode(resNode.data.value, True))
        resNode = resNode.next
    else:
        currTree.data = "E"
        currTree.children = []
        return None
    t0 = tN.treeNode("block_statements", False)
    currTree.addChild(t0)
    resNode = block_statements(resNode,t0)
    if resNode is None:
        return None
    t3 = tN.treeNode("if_statement_prime", False)
    currTree.addChild(t3)
    resNode = if_statement_prime(resNode,t3)
    return resNode


def if_statement_prime(currNode, currTree):

    resNode = currNode
    if resNode.data.value == "else":
        currTree.addChild(tN.treeNode(resNode.data.value, True))
        resNode = resNode.next
    else:
        return currNode
    t0 = tN.treeNode("block_statements", False)
    currTree.addChild(t0)
    resNode = block_statements(resNode,t0)
    if resNode is None:
        return currNode
    return resNode

def condition_expression(currNode, currTree):

    resNode = currNode
    t0 = tN.treeNode("condition", False)
    currTree.addChild(t0)
    resNode = condition(resNode,t0)
    if resNode is None:
        currTree.data = "E"
        currTree.children = []
        return None
    t1 = tN.treeNode("condition_expression_prime", False)
    currTree.addChild(t1)
    resNode = condition_expression_prime(resNode,t1)
    return resNode

def condition_expression_prime(currNode, currTree):

    resNode = currNode
    t0 = tN.treeNode("condition_op", False)
    currTree.addChild(t0)
    resNode = condition_op(resNode, t0)
    if resNode is None:
        return currNode
    t1 = tN.treeNode("condition", False)
    currTree.addChild(t1)
    resNode = condition(resNode, t1)
    if resNode is None:
        return currNode
    return resNode


def condition_op(currNode, currTree):

    resNode = currNode
    if resNode.data.value == "&":
        currTree.addChild(tN.treeNode(resNode.data.value, True))
        resNode = resNode.next
        if resNode.data.value == "&":
            currTree.addChild(tN.treeNode(resNode.data.value, True))
            resNode = resNode.next
            return resNode
        else:
            currTree.data = "E"
            currTree.children = []
            return None
    elif resNode.data.value == "|":
        currTree.addChild(tN.treeNode(resNode.data.value, True))
        resNode = resNode.next
        if resNode.data.value == "|":
            currTree.addChild(tN.treeNode(resNode.data.value, True))
            resNode = resNode.next
            return resNode
        else:
            currTree.data = "E"
            currTree.children = []
            return None
    else:
        currTree.data = "E"
        currTree.children = []
        return None

def condition(currNode, currTree):

    resNode = currNode
    t0 = tN.treeNode("expression", False)
    currTree.addChild(t0)
    resNode = expression(resNode,t0)
    if resNode is None:
        currTree.data = "E"
        currTree.children = []
        return None
    t2 = tN.treeNode("comparison_op", False)
    currTree.addChild(t2)
    resNode = comparison_op(resNode,t2)
    if resNode is None:
        currTree.data = "E"
        currTree.children = []
        return None
    t1 = tN.treeNode("expression", False)
    currTree.addChild(t1)
    resNode = expression(resNode,t1)
    if resNode is None:
        currTree.data = "E"
        currTree.children = []
        return None
    return resNode

def comparison_op(currNode, currTree):

    resNode = currNode
    if resNode.data.value == "=":
        currTree.addChild(tN.treeNode(resNode.data.value, True))
        resNode = resNode.next
        if resNode.data.value == "=":
            currTree.addChild(tN.treeNode(resNode.data.value, True))
            resNode = resNode.next
            return resNode
    elif resNode.data.value == "!":
        currTree.addChild(tN.treeNode(resNode.data.value, True))
        resNode = resNode.next
        if resNode.data.value == "=":
            currTree.addChild(tN.treeNode(resNode.data.value, True))
            resNode = resNode.next
            return resNode
    elif resNode.data.value == ">":
        currTree.addChild(tN.treeNode(resNode.data.value, True))
        resNode = resNode.next
        if resNode.data.value == "=":
            currTree.addChild(tN.treeNode(resNode.data.value, True))
            resNode = resNode.next
            return resNode
        return resNode
    elif resNode.data.value == "<":
        currTree.addChild(tN.treeNode(resNode.data.value, True))
        resNode = resNode.next
        if resNode.data.value == "=":
            currTree.addChild(tN.treeNode(resNode.data.value, True))
            resNode = resNode.next
            return resNode
        return resNode
    currTree.data = "E"
    currTree.children = []
    return None


def while_statement(currNode, currTree):

    resNode = currNode
    if resNode.data.value == "while":
        currTree.addChild(tN.treeNode(resNode.data.value, True))
        resNode = resNode.next
    else:
        currTree.data = "E"
        currTree.children = []
        return None
    if resNode.data.value == "(":
        currTree.addChild(tN.treeNode(resNode.data.value, True))
        resNode = resNode.next
    else:
        currTree.data = "E"
        currTree.children = []
        return None
    t0 = tN.treeNode("condition_expression", False)
    currTree.addChild(t0)
    resNode = condition_expression(resNode, t0)
    if resNode is None:
        currTree.data = "E"
        currTree.children = []
        return None
    if resNode.data.value == ")":
        currTree.addChild(tN.treeNode(resNode.data.value, True))
        resNode = resNode.next
    else:
        currTree.data = "E"
        currTree.children = []
        return None
    t1 = tN.treeNode("block_statements", False)
    currTree.addChild(t1)
    resNode = block_statements(resNode,t1)
    if resNode is None:
        currTree.data = "E"
        currTree.children = []
        return None
    return resNode

def return_statement(currNode, currTree):

    resNode = currNode
    if resNode.data.value == "return":
        currTree.addChild(tN.treeNode(resNode.data.value, True))
        resNode = resNode.next
    else:
        currTree.data = "E"
        currTree.children = []
        return None
    t0 = tN.treeNode("return_statement_prime", False)
    currTree.addChild(t0)
    resNode = return_statement_prime(resNode,t0)
    return resNode

def return_statement_prime(currNode, currTree):

    resNode = currNode
    t0 = tN.treeNode("expression", False)
    currTree.addChild(t0)
    resNode = expression(resNode,t0)
    if resNode is None:
        resNode = currNode
    if resNode.data.value == ";":
        currTree.addChild(tN.treeNode(resNode.data.value, True))
        resNode = resNode.next
    else:
        currTree.data = "E"
        currTree.children = []
        return None
    return resNode

def break_statement(currNode, currTree):

    resNode = currNode
    if resNode.data.value == "break":
        currTree.addChild(tN.treeNode(resNode.data.value, True))
        resNode = resNode.next
    else:
        currTree.data = "E"
        currTree.children = []
        return None
    if resNode.data.value == ";":
        currTree.addChild(tN.treeNode(resNode.data.value, True))
        resNode = resNode.next
    else:
        currTree.data = "E"
        currTree.children = []
        return None
    return resNode

def continue_statement(currNode, currTree):
    resNode = currNode
    if resNode.data.value == "continue":
        currTree.addChild(tN.treeNode(resNode.data.value, True))
        resNode = resNode.next
    else:
        currTree.data = "E"
        currTree.children = []
        return None
    if resNode.data.value == ";":
        currTree.addChild(tN.treeNode(resNode.data.value, True))
        resNode = resNode.next
    else:
        currTree.data = "E"
        currTree.children = []
        return None
    return resNode

def expression(currNode, currTree):
    resNode = currNode
    t1 = tN.treeNode("term", False)
    currTree.addChild(t1)
    resNode = term(resNode, t1)
    if resNode is None:
        currTree.data = "E"
        currTree.children = []
        return None
    t0 = tN.treeNode("expression_prime", False)
    currTree.addChild(t0)
    return expression_prime(resNode,t0)

def expression_prime(currNode, currTree):
    resNode = currNode
    t0 = tN.treeNode("addop", False)
    currTree.addChild(t0)
    resNode = addop(resNode, t0)
    if resNode is None:
        return currNode
    t1 = tN.treeNode("term", False)
    currTree.addChild(t1)
    resNode = term(resNode,t1)
    if resNode is None:
        return currNode
    t2= tN.treeNode("expression_prime", False)
    currTree.addChild(t2)
    return expression_prime(resNode, t2)

def addop(currNode, currTree):
    if(currNode.data.value == "+"):
        currTree.addChild(tN.treeNode(currNode.data.value, True))
        return currNode.next
    if(currNode.data.value == "-"):
        currTree.addChild(tN.treeNode(currNode.data.value, True))
        return currNode.next
    currTree.data = "E"
    currTree.children = []
    return None

def term(currNode, currTree):
    resNode = currNode
    t0 = tN.treeNode("factor", False)
    currTree.addChild(t0)
    resNode = factor(resNode,t0)
    if resNode is None:
        currTree.data = "E"
        currTree.children = []
        return None
    currNode = resNode
    t1 = tN.treeNode("mulop", False)
    currTree.addChild(t1)
    resNode = mulop(resNode,t1)
    if resNode is None:
        return currNode
    t2 = tN.treeNode("term_prime", False)
    currTree.addChild(t2)
    return term_prime(resNode,t2)


def term_prime(currNode, currTree):
    resNode = currNode
    t0 = tN.treeNode("factor", False)
    currTree.addChild(t0)
    resNode = factor(resNode, t0)
    if resNode is None:
        return currNode
    currNode = resNode
    t1 = tN.treeNode("mulop", False)
    currTree.addChild(t1)
    resNode = mulop(resNode,t1)
    if resNode is None:
        return currNode
    t2 = tN.treeNode("term_prime", False)
    currTree.addChild(t2)
    return term_prime(resNode,t2)

def mulop(currNode, currTree):
    if(currNode.data.value == "*"):
        currTree.addChild(tN.treeNode(currNode.data.value, True))
        return currNode.next
    if(currNode.data.value == "/"):
        currTree.addChild(tN.treeNode(currNode.data.value, True))
        return currNode.next
    currTree.data = "E"
    currTree.children = []
    return None

def factor(currNode, currTree):
    resNode = currNode
    if resNode.data.value == "-":
        currTree.addChild(tN.treeNode(resNode.data.value, True))
        resNode = resNode.next
        if resNode.data.lex == "number":
            currTree.addChild(tN.treeNode(resNode.data.value, True))
            resNode = resNode.next
            return resNode
        else:
            currTree.data = "E"
            currTree.children = []
            return None
    resNode = currNode
    if resNode.data.lex == "number":
        currTree.addChild(tN.treeNode(resNode.data.value, True))
        resNode = resNode.next
        return resNode
    if resNode.data.value == "(":
        currTree.addChild(tN.treeNode(resNode.data.value, True))
        resNode = resNode.next
        t0 = tN.treeNode("expression", False)
        currTree.addChild(t0)
        resNode = expression(resNode, t0)
        if resNode is None:
            currTree.data = "E"
            currTree.children = []
            return None
        if resNode.data.value == ")":
            currTree.addChild(tN.treeNode(resNode.data.value, True))
            resNode = resNode.next
            return resNode
        else:
            currTree.data = "E"
            currTree.children = []
            return None
    t1 = tN.treeNode("identifier", False)
    currTree.addChild(t1)
    resNode = identifier(resNode, t1)
    if resNode is None:
        currTree.data = "E"
        currTree.children = []
        return None
    t2 = tN.treeNode("factor_prime", False)
    currTree.addChild(t2)
    return factor_prime(resNode,t2)

def factor_prime(currNode, currTree):
    resNode = currNode
    if resNode.data.value == "(":
        currTree.addChild(tN.treeNode(resNode.data.value, True))
        resNode = resNode.next
        t0 = tN.treeNode("expr_list", False)
        currTree.addChild(t0)
        resNode = expr_list(resNode,t0)
        if resNode is None:
            currTree.data = "E"
            currTree.children = []
            return None
        if resNode.data.value == ")":
            currTree.addChild(tN.treeNode(resNode.data.value, True))
            resNode = resNode.next
            return resNode
        else:
            currTree.data = "E"
            currTree.children = []
            return None
    if resNode.data.value == "[":
        currTree.addChild(tN.treeNode(resNode.data.value, True))
        resNode = resNode.next
        t1 = tN.treeNode("expr_list", False)
        currTree.addChild(t1)
        resNode = expr_list(resNode,t1)
        if resNode is None:
            currTree.data = "E"
            currTree.children = []
            return None
        if resNode.data.value == "]":
            currTree.addChild(tN.treeNode(resNode.data.value, True))
            resNode = resNode.next
            return resNode
        else:
            currTree.data = "E"
            currTree.children = []
            return None
    return currNode