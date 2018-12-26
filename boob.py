from sys import *

tokens = []
num_stack = []
OPs = ['+','-','*','/']
NUMs = ['0','1','2','3','4','5','6','7','8','9']

def openFile(filename):
    data = open(filename, 'r').read()
    data += '<EOF>'
    return data

def lex(filecontents):
    tok = ''
    state = 0
    string = ''
    expr = ''
    n = ''
    isexpr = 0
    # print(filecontents)
    filecontents = list(filecontents)
    # print(filecontents)
    for char in filecontents:
        tok += char
        if tok == ' ':
            if state == 0:
                tok = ''
            else:
                tok = ' '
        elif tok == '\n' or tok == '<EOF>':
            if expr != '' and isexpr == 1:
                tokens.append('EXPR:' + expr)
                expr = ''
                isexpr = 0
            elif expr != '' and isexpr == 0:
                tokens.append('NUM:' + expr)
                expr = ''
            tok = ''
        elif tok == 'PRINT' or tok == 'print':
            tokens.append('PRINT')
            tok = ''
        elif tok in NUMs:
            expr += tok
            tok = ''
        elif tok in OPs:
            isexpr = 1
            expr += tok
            tok = ''
        elif tok == '\"':
            if state == 0:
                state = 1
            elif state == 1:
                tokens.append('STRING:' + string + '\"')
                string = ''
                state = 0
                tok = ''
        elif state == 1:
            string += tok
            tok = ''
    # print(tokens)
    return(tokens)

def evalEXPR(expr):
    expr = ',' + expr # EOE
    i = len(expr) - 1
    num = ''
    while i >= 0:
        if expr[i] in OPs:
            num = num[::-1]
            num_stack.append(int(num))
            num_stack.append(expr[i])
            num = ''
        elif expr[i] == ',':
            num = num[::-1]
            num_stack.append(int(num))
            num = ''
        else:
            num += expr[i]
        i -= 1
    # print(num_stack)
    result = evalOOP(num_stack)
    return result

def evalOOP(stack):
    print(stack)
    found = 0
    for e in range(0,len(stack)):
        if len(stack) == 1:
            return stack[0] # exit
        elem = stack[e] if len(stack) != 1 else 0
        if '*' in stack or '/' in stack:
            if elem == '*':
                stack[e] = stack[e+1] * stack[e-1]
                found = 1
                print(stack)
            elif elem == '/':
                if stack[e -1] == 0:
                    return 'Can\'t divide by zero!'
                else:
                    stack[e] = stack[e+1] / stack[e-1]
                    found = 1
                    print(stack)
        else:
            if elem == '+':
                stack[e] = stack[e+1] + stack[e-1]
                found = 1
                print(stack)
            elif elem == '-':
                stack[e] = stack[e+1] - stack[e-1]
                found = 1
                print(stack)

        if found == 1:
            del stack[e+1]
            del stack[e-1]
            found = 0
            evalOOP(stack)
    return 0 # error exit

def doPRINT(toPRINT):
    if toPRINT[0:6] == 'STRING':
        toPRINT = toPRINT[8:-1]
    elif toPRINT[0:3] == 'NUM':
        toPRINT = toPRINT[4:]
    elif toPRINT[0:4] == 'EXPR':
        print(toPRINT[5:])
        toPRINT = evalEXPR(toPRINT[5:])
    print(toPRINT)

def parse(toks):
    i = 0
    while(i < len(toks)):
        if toks[i] == 'PRINT':
            doPRINT(toks[i+1])
            i += 2
        else:
            return 0

def run():
    data = openFile(argv[1])
    parse(lex(data))

run()
