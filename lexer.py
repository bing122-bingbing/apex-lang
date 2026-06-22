import re
from enum import Enum, auto
from dataclasses import dataclass
from typing import List, Optional

class TokenType(Enum):
    # Literals
    INT = auto()
    FLOAT = auto()
    STRING = auto()
    TRUE = auto()
    FALSE = auto()
    NULL = auto()
    
    # Identifiers and Keywords
    IDENTIFIER = auto()
    CLASS = auto()
    DEF = auto()
    IF = auto()
    ELSE = auto()
    ELIF = auto()
    WHILE = auto()
    FOR = auto()
    IN = auto()
    BREAK = auto()
    CONTINUE = auto()
    RETURN = auto()
    NEW = auto()
    THIS = auto()
    EXTENDS = auto()
    VAR = auto()
    TYPE_INT = auto()
    TYPE_FLOAT = auto()
    TYPE_STRING = auto()
    TYPE_BOOL = auto()
    TYPE_LIST = auto()
    TYPE_DICT = auto()
    TYPE_VOID = auto()
    
    # Operators
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    MODULO = auto()
    POWER = auto()
    
    # Comparison
    EQ = auto()  # ==
    NEQ = auto()  # !=
    LT = auto()  # <
    GT = auto()  # >
    LTE = auto()  # <=
    GTE = auto()  # >=
    
    # Logical
    AND = auto()
    OR = auto()
    NOT = auto()
    
    # Assignment
    ASSIGN = auto()  # =
    PLUS_ASSIGN = auto()  # +=
    MINUS_ASSIGN = auto()  # -=
    
    # Delimiters
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    SEMICOLON = auto()
    COLON = auto()
    COMMA = auto()
    DOT = auto()
    ARROW = auto()  # ->
    
    # Special
    EOF = auto()
    NEWLINE = auto()

@dataclass
class Token:
    type: TokenType
    value: any
    line: int
    column: int

class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
        self.keywords = {
            'class': TokenType.CLASS,
            'def': TokenType.DEF,
            'if': TokenType.IF,
            'else': TokenType.ELSE,
            'elif': TokenType.ELIF,
            'while': TokenType.WHILE,
            'for': TokenType.FOR,
            'in': TokenType.IN,
            'break': TokenType.BREAK,
            'continue': TokenType.CONTINUE,
            'return': TokenType.RETURN,
            'new': TokenType.NEW,
            'this': TokenType.THIS,
            'extends': TokenType.EXTENDS,
            'var': TokenType.VAR,
            'int': TokenType.TYPE_INT,
            'float': TokenType.TYPE_FLOAT,
            'string': TokenType.TYPE_STRING,
            'bool': TokenType.TYPE_BOOL,
            'list': TokenType.TYPE_LIST,
            'dict': TokenType.TYPE_DICT,
            'void': TokenType.TYPE_VOID,
            'true': TokenType.TRUE,
            'false': TokenType.FALSE,
            'null': TokenType.NULL,
            'and': TokenType.AND,
            'or': TokenType.OR,
            'not': TokenType.NOT,
        }
    
    def current_char(self) -> Optional[str]:
        if self.position >= len(self.source):
            return None
        return self.source[self.position]
    
    def peek_char(self, offset=1) -> Optional[str]:
        pos = self.position + offset
        if pos >= len(self.source):
            return None
        return self.source[pos]
    
    def advance(self):
        if self.position < len(self.source):
            if self.source[self.position] == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            self.position += 1
    
    def skip_whitespace(self):
        while self.current_char() and self.current_char() in ' \t':
            self.advance()
    
    def skip_comment(self):
        if self.current_char() == '#':
            while self.current_char() and self.current_char() != '\n':
                self.advance()
    
    def read_string(self, quote):
        value = ''
        self.advance()  # Skip opening quote
        while self.current_char() and self.current_char() != quote:
            if self.current_char() == '\\':
                self.advance()
                if self.current_char() == 'n':
                    value += '\n'
                elif self.current_char() == 't':
                    value += '\t'
                elif self.current_char() == 'r':
                    value += '\r'
                elif self.current_char() == '\\':
                    value += '\\'
                elif self.current_char() == quote:
                    value += quote
                else:
                    value += self.current_char()
                self.advance()
            else:
                value += self.current_char()
                self.advance()
        if self.current_char() == quote:
            self.advance()
        return value
    
    def read_number(self):
        num = ''
        while self.current_char() and (self.current_char().isdigit() or self.current_char() == '.'):
            num += self.current_char()
            self.advance()
        
        if '.' in num:
            return float(num)
        return int(num)
    
    def read_identifier(self):
        identifier = ''
        while self.current_char() and (self.current_char().isalnum() or self.current_char() == '_'):
            identifier += self.current_char()
            self.advance()
        return identifier
    
    def tokenize(self) -> List[Token]:
        while self.position < len(self.source):
            self.skip_whitespace()
            
            if self.current_char() is None:
                break
            
            # Comments
            if self.current_char() == '#':
                self.skip_comment()
                continue
            
            # Newlines
            if self.current_char() == '\n':
                self.tokens.append(Token(TokenType.NEWLINE, '\n', self.line, self.column))
                self.advance()
                continue
            
            # Strings
            if self.current_char() in '"\'':
                quote = self.current_char()
                value = self.read_string(quote)
                self.tokens.append(Token(TokenType.STRING, value, self.line, self.column))
                continue
            
            # Numbers
            if self.current_char().isdigit():
                value = self.read_number()
                token_type = TokenType.FLOAT if isinstance(value, float) else TokenType.INT
                self.tokens.append(Token(token_type, value, self.line, self.column))
                continue
            
            # Identifiers and Keywords
            if self.current_char().isalpha() or self.current_char() == '_':
                identifier = self.read_identifier()
                token_type = self.keywords.get(identifier, TokenType.IDENTIFIER)
                value = identifier if token_type == TokenType.IDENTIFIER else identifier
                self.tokens.append(Token(token_type, value, self.line, self.column))
                continue
            
            # Operators and Delimiters
            ch = self.current_char()
            
            if ch == '+':
                if self.peek_char() == '=':
                    self.tokens.append(Token(TokenType.PLUS_ASSIGN, '+=', self.line, self.column))
                    self.advance()
                    self.advance()
                else:
                    self.tokens.append(Token(TokenType.PLUS, '+', self.line, self.column))
                    self.advance()
            elif ch == '-':
                if self.peek_char() == '=':
                    self.tokens.append(Token(TokenType.MINUS_ASSIGN, '-=', self.line, self.column))
                    self.advance()
                    self.advance()
                elif self.peek_char() == '>':
                    self.tokens.append(Token(TokenType.ARROW, '->', self.line, self.column))
                    self.advance()
                    self.advance()
                else:
                    self.tokens.append(Token(TokenType.MINUS, '-', self.line, self.column))
                    self.advance()
            elif ch == '*':
                if self.peek_char() == '*':
                    self.tokens.append(Token(TokenType.POWER, '**', self.line, self.column))
                    self.advance()
                    self.advance()
                else:
                    self.tokens.append(Token(TokenType.MULTIPLY, '*', self.line, self.column))
                    self.advance()
            elif ch == '/':
                self.tokens.append(Token(TokenType.DIVIDE, '/', self.line, self.column))
                self.advance()
            elif ch == '%':
                self.tokens.append(Token(TokenType.MODULO, '%', self.line, self.column))
                self.advance()
            elif ch == '=':
                if self.peek_char() == '=':
                    self.tokens.append(Token(TokenType.EQ, '==', self.line, self.column))
                    self.advance()
                    self.advance()
                else:
                    self.tokens.append(Token(TokenType.ASSIGN, '=', self.line, self.column))
                    self.advance()
            elif ch == '!':
                if self.peek_char() == '=':
                    self.tokens.append(Token(TokenType.NEQ, '!=', self.line, self.column))
                    self.advance()
                    self.advance()
                else:
                    self.tokens.append(Token(TokenType.NOT, '!', self.line, self.column))
                    self.advance()
            elif ch == '<':
                if self.peek_char() == '=':
                    self.tokens.append(Token(TokenType.LTE, '<=', self.line, self.column))
                    self.advance()
                    self.advance()
                else:
                    self.tokens.append(Token(TokenType.LT, '<', self.line, self.column))
                    self.advance()
            elif ch == '>':
                if self.peek_char() == '=':
                    self.tokens.append(Token(TokenType.GTE, '>=', self.line, self.column))
                    self.advance()
                    self.advance()
                else:
                    self.tokens.append(Token(TokenType.GT, '>', self.line, self.column))
                    self.advance()
            elif ch == '(':
                self.tokens.append(Token(TokenType.LPAREN, '(', self.line, self.column))
                self.advance()
            elif ch == ')':
                self.tokens.append(Token(TokenType.RPAREN, ')', self.line, self.column))
                self.advance()
            elif ch == '{':
                self.tokens.append(Token(TokenType.LBRACE, '{', self.line, self.column))
                self.advance()
            elif ch == '}':
                self.tokens.append(Token(TokenType.RBRACE, '}', self.line, self.column))
                self.advance()
            elif ch == '[':
                self.tokens.append(Token(TokenType.LBRACKET, '[', self.line, self.column))
                self.advance()
            elif ch == ']':
                self.tokens.append(Token(TokenType.RBRACKET, ']', self.line, self.column))
                self.advance()
            elif ch == ';':
                self.tokens.append(Token(TokenType.SEMICOLON, ';', self.line, self.column))
                self.advance()
            elif ch == ':':
                self.tokens.append(Token(TokenType.COLON, ':', self.line, self.column))
                self.advance()
            elif ch == ',':
                self.tokens.append(Token(TokenType.COMMA, ',', self.line, self.column))
                self.advance()
            elif ch == '.':
                self.tokens.append(Token(TokenType.DOT, '.', self.line, self.column))
                self.advance()
            else:
                raise SyntaxError(f"Unknown character '{ch}' at line {self.line}, column {self.column}")
        
        self.tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return self.tokens
