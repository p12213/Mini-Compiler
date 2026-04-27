import re

TOKEN_TYPES = [
    ('NUMBER', r'\d+'),

    # ✅ COMPARISON OPERATORS (IMPORTANT — keep == before =)
    ('EQEQ', r'=='),
    ('LT', r'<'),
    ('GT', r'>'),

    # ✅ ARITHMETIC
    ('PLUS', r'\+'),
    ('MINUS', r'-'),
    ('MUL', r'\*'),
    ('DIV', r'/'),

    # ✅ ASSIGNMENT
    ('EQUAL', r'='),

    # ✅ BRACKETS
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('LBRACE', r'\{'),
    ('RBRACE', r'\}'),

    # ✅ IDENTIFIER
    ('ID', r'[a-zA-Z_]\w*'),

    # ✅ IGNORE
    ('COMMENT', r'\#.*'),
    ('NEWLINE', r'\n'),
    ('SKIP', r'[ \t]+'),
]

# ✅ Keywords dictionary
KEYWORDS = {
    "let": "LET",
    "print": "PRINT",
    "input": "INPUT",
    "if": "IF",
    "else": "ELSE",
    "while": "WHILE",
    "for": "FOR",
    "to": "TO",
    "func": "FUNC",
    "call": "CALL"
}


class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"{self.type}:{self.value}"


def lexer(code):
    tokens = []
    pos = 0

    while pos < len(code):
        match_found = False

        for token_type, pattern in TOKEN_TYPES:
            regex = re.compile(pattern)
            match = regex.match(code, pos)

            if match:
                text = match.group(0)
                match_found = True

                if token_type not in ("SKIP", "NEWLINE", "COMMENT"):

                    # ✅ Convert ID → keyword
                    if token_type == "ID" and text in KEYWORDS:
                        token_type = KEYWORDS[text]

                    tokens.append(Token(token_type, text))

                pos = match.end()
                break

        if not match_found:
            raise SyntaxError("Invalid character: " + code[pos])

    return tokens
