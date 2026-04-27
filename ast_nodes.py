class ProgramNode:
    def __init__(self, statements):
        self.statements = statements


class NumberNode:
    def __init__(self, value):
        self.value = int(value)


class VarNode:
    def __init__(self, name):
        self.name = name


class BinOpNode:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right


class AssignNode:
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr


class PrintNode:
    def __init__(self, expr):
        self.expr = expr


class InputNode:
    pass


class IfNode:
    def __init__(self, condition, body, else_body=None):
        self.condition = condition
        self.body = body
        self.else_body = else_body


class WhileNode:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body


class ForNode:
    def __init__(self, var_name, start, end, body):
        self.var_name = var_name
        self.start = start
        self.end = end
        self.body = body


class FuncNode:
    def __init__(self, name, body):
        self.name = name
        self.body = body


class CallNode:
    def __init__(self, name):
        self.name = name