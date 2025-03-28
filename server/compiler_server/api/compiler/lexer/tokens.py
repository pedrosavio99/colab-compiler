import re

TOKEN_SPECS = [
    ('KEYWORD', r'\b(?:if|else|for|while|def|True|False|print|in)\b'),
    ('INVALID_NUMBER', r'\b\d+[a-zA-Z_]\w*\b|\b\d+\.(?!\d)\b|\b\d+e[-+]?\d*\b'),
    ('NUMBER', r'\b\d+(\.\d+)?\b'),
    ('ID', r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'),
    ('STRING', r'"[^"]*"|\'[^\']*\''),
    ('OPERATOR', r'[+\-*/%]'),
    ('BITWISE', r'[&|^~]|<<|>>'),
    ('LOGICAL', r'\b(?:and|or|not)\b'),
    ('COMPARISON', r'==|!=|<=|>=|<|>'),
    ('ASSIGN', r'='),
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('COMMA', r','),
    ('COLON', r':'),
    ('NEWLINE', r'\n'),
    ('WHITESPACE', r'[ \t]+'),
    ('UNKNOWN', r'[^ \t\n]'),
]

TOKEN_REGEX = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_SPECS)