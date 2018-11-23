'''
for symbol, digit, letter, and reserve we create a hashset since they are all pre-defined values. This allows us to
identify and classify tokens with ease.
'''
symbol = {"(",")","{","}","[","]",",",";","+","-","*","/", "==","!" ,"!=","<", "<=",">", ">=","=","&&","||","&","|"}
digit = {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9"}
letter = {"a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v","w", "x", "y", "z","A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S",
"T", "U", "V", "W", "X", "Y", "Z", "_"}
reserve = {
"int", "void", "if","else","while", "return", "continue", "break", "scanf", "printf"
}

class Token:
    def __init__(self, value, lex):
        self.value = value #The token's string
        self.lex = lex #the classification of the token
        if reserve.__contains__(self.value):
            self.lex = "reserved word"
        elif self.lex is None:
            self.lex = setLex(self)

'''
if no token classification is passed in then we use setLex to check if the value is in one of the hashsets. Otherwise
we return None and set that as the classification
'''
def setLex(s):
    if symbol.__contains__(s.value):
        return "symbol"
    if digit.__contains__(s.value):
        return "digit"
    if letter.__contains__(s.value):
        return "letter"
    if reserve.__contains__(s.value):
        return "reserved word"
    return None
