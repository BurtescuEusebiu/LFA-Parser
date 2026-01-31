from .Lexer import Lexer
from .Grammar import Grammar

class Parser():
    def __init__(self, lexer: Lexer, grammar: Grammar) -> None:
        self.lexer = lexer
        self.grammar = grammar

    
    def parse(self, input: str) -> str:
        lex_output = self.lexer.lex(input)
        lex_output = [lx for lx in lex_output if lx[0] != 'SPACE']
        cyk_output = self.grammar.cykParse(lex_output)
        return str(cyk_output)
        
