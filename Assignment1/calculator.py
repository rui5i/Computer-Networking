def operation(op, b, a):
    if op == '+':
        return a + b
    elif op == '-':
        return a - b
    elif op == '*':
        return a * b
    elif op == '/':
        return a / b
    else:
        return 0

def precedence(op1, op2):
    if op2 == '(' or op2 == ')':
        return False
    elif (op1 == '*' or op1 == '/') and (op2 == '+' or op2 == '-'):
        return False
    else:
        return True

def calculate(s):
    if len(s) == 0:
        return 0
    # number stack
    num_stack = []
    # operator stack
    ops_stack = []
    index = 0
    while index < len(s):
        elem = s[index]
        if elem.isdigit():
            num = int(elem)
            # construct complete number
            while (index < len(s) - 1) and (s[index + 1].isdigit()):
                num = num * 10 + int(s[index + 1])
                index += 1
            num_stack.append(num)
        elif elem == '(':
            ops_stack.append(elem)
        elif elem == ')':
            # do calculation when meeting ')'
            while len(ops_stack) != 0 and ops_stack[-1] != '(':
                num_stack.append(int(operation(ops_stack.pop(), num_stack.pop(), num_stack.pop())))
            # get rid of '(' associated
            if len(ops_stack) != 0: ops_stack.pop()
        elif elem == '-' and (index == 0 or not s[index - 1].isdigit()):
            # if elem is an along negative number, make '-5' to '0-5'
            num_stack.append(0)
            ops_stack.append('-')
        elif elem == '+' or elem == '-' or elem == '*' or elem == '/':
            while len(ops_stack) != 0 and precedence(elem, ops_stack[-1]):
                num_stack.append(int(operation(ops_stack.pop(), num_stack.pop(), num_stack.pop())))
            ops_stack.append(elem)
        index += 1
    while len(ops_stack) != 0:
        num_stack.append(int(operation(ops_stack.pop(), num_stack.pop(), num_stack.pop())))
    return num_stack.pop()