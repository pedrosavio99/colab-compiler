from .core import Parser

def parse(tokens):
    parser = Parser(tokens)
    return parser.parse()