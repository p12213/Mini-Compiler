from ast_nodes import *

class Interpreter:

    def __init__(self):
        self.variables = {}

    def execute(self, node):

        if isinstance(node, ProgramNode):
            for stmt in node.statements:
                self.execute(stmt)

        elif isinstance(node, AssignNode):
            value = self.eval_expr(node.expr)
            self.variables[node.name] = value

        elif isinstance(node, PrintNode):
            value = self.eval_expr(node.expr)
            print(value)

        elif isinstance(node, IfNode):
            condition = self.eval_expr(node.condition)

            if condition:
                for stmt in node.body:
                    self.execute(stmt)

            elif node.else_body:
                for stmt in node.else_body:
                    self.execute(stmt)

        elif isinstance(node, WhileNode):
            while self.eval_expr(node.condition):
                for stmt in node.body:
                    self.execute(stmt)

        elif isinstance(node, ForNode):
            start_val = self.eval_expr(node.start)
            end_val = self.eval_expr(node.end)

            for i in range(start_val, end_val + 1):
                self.variables[node.var_name] = i
                for stmt in node.body:
                    self.execute(stmt)

    def eval_expr(self, node):

        if isinstance(node, NumberNode):
            return node.value

        elif isinstance(node, VarNode):
            if node.name not in self.variables:
                raise Exception(f"Undefined variable: {node.name}")
            return self.variables[node.name]

        elif isinstance(node, BinOpNode):
            left = self.eval_expr(node.left)
            right = self.eval_expr(node.right)

            if node.op == "PLUS":
                return left + right
            elif node.op == "MINUS":
                return left - right
            elif node.op == "MUL":
                return left * right
            elif node.op == "DIV":
                if right == 0:
                    raise Exception("Division by zero")
                return left / right
            elif node.op == "LT":
                return left < right
            elif node.op == "GT":
                return left > right
            elif node.op == "EQEQ":
                return left == right

        raise Exception(f"Unknown expression node: {type(node).__name__}")