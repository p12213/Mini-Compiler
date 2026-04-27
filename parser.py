from ast_nodes import *

class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def eat(self, type_):
        token = self.current()
        if token and token.type == type_:
            self.pos += 1
            return token
        raise SyntaxError(f"Expected {type_}, got {token.type if token else 'EOF'}")

    # ================= MAIN =================
    def parse(self):
        statements = []

        while self.current():
            token = self.current()

            if token.type == "LET":
                statements.append(self.parse_assign())

            elif token.type == "PRINT":
                statements.append(self.parse_print())

            elif token.type == "IF":
                statements.append(self.parse_if())

            elif token.type == "WHILE":
                statements.append(self.parse_while())

            elif token.type == "FOR":
                statements.append(self.parse_for())

            else:
                raise SyntaxError(f"Unexpected token: {token.type}")

        return ProgramNode(statements)

    # ================= STATEMENTS =================
    def parse_assign(self):
        self.eat("LET")
        name = self.eat("ID").value
        self.eat("EQUAL")

        expr = self.parse_expression()
        return AssignNode(name, expr)

    def parse_print(self):
        self.eat("PRINT")
        expr = self.parse_expression()
        return PrintNode(expr)

    def parse_if(self):
        self.eat("IF")
        condition = self.parse_condition()
        body = self.parse_block()

        else_body = None
        if self.current() and self.current().type == "ELSE":
            self.eat("ELSE")
            else_body = self.parse_block()

        return IfNode(condition, body, else_body)

    def parse_while(self):
        self.eat("WHILE")
        condition = self.parse_condition()
        body = self.parse_block()

        return WhileNode(condition, body)

    def parse_for(self):
        self.eat("FOR")
        var_name = self.eat("ID").value
        self.eat("EQUAL")
        start = self.parse_expression()
        self.eat("TO")
        end = self.parse_expression()
        body = self.parse_block()

        return ForNode(var_name, start, end, body)

    # ================= BLOCK =================
    def parse_block(self):
        self.eat("LBRACE")

        statements = []

        while self.current() and self.current().type != "RBRACE":
            token = self.current()

            if token.type == "LET":
                statements.append(self.parse_assign())

            elif token.type == "PRINT":
                statements.append(self.parse_print())

            elif token.type == "IF":
                statements.append(self.parse_if())

            elif token.type == "WHILE":
                statements.append(self.parse_while())

            elif token.type == "FOR":
                statements.append(self.parse_for())

            else:
                raise SyntaxError(f"Unexpected token in block: {token.type}")

        self.eat("RBRACE")
        return statements

    # ================= EXPRESSIONS =================
    def parse_condition(self):
        left = self.parse_expression()

        if self.current() and self.current().type in ("LT", "GT", "EQEQ"):
            op = self.eat(self.current().type).type
            right = self.parse_expression()
            return BinOpNode(left, op, right)

        return left

    def parse_expression(self):
        node = self.parse_term()

        while self.current() and self.current().type in ("PLUS", "MINUS"):
            op = self.eat(self.current().type).type
            right = self.parse_term()
            node = BinOpNode(node, op, right)

        return node

    def parse_term(self):
        node = self.parse_factor()

        while self.current() and self.current().type in ("MUL", "DIV"):
            op = self.eat(self.current().type).type
            right = self.parse_factor()
            node = BinOpNode(node, op, right)

        return node

    def parse_factor(self):
        token = self.current()

        if token.type == "NUMBER":
            self.eat("NUMBER")
            return NumberNode(token.value)

        elif token.type == "ID":
            self.eat("ID")
            return VarNode(token.value)

        elif token.type == "LPAREN":
            self.eat("LPAREN")
            node = self.parse_expression()
            self.eat("RPAREN")
            return node

        else:
            raise SyntaxError(f"Unexpected token: {token.type}")