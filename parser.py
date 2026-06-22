from typing import List, Optional
from lexer import Token, TokenType, Lexer
from ast_nodes import *

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.position = 0
    
    def current_token(self) -> Token:
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return self.tokens[-1]  # EOF
    
    def peek_token(self, offset=1) -> Token:
        pos = self.position + offset
        if pos < len(self.tokens):
            return self.tokens[pos]
        return self.tokens[-1]  # EOF
    
    def advance(self) -> Token:
        token = self.current_token()
        if self.position < len(self.tokens) - 1:
            self.position += 1
        return token
    
    def expect(self, token_type: TokenType) -> Token:
        token = self.current_token()
        if token.type != token_type:
            raise SyntaxError(f"Expected {token_type}, got {token.type} at line {token.line}")
        self.advance()
        return token
    
    def skip_newlines(self):
        while self.current_token().type == TokenType.NEWLINE:
            self.advance()
    
    def parse(self) -> Program:
        statements = []
        self.skip_newlines()
        
        while self.current_token().type != TokenType.EOF:
            self.skip_newlines()
            if self.current_token().type == TokenType.EOF:
                break
            
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
            self.skip_newlines()
        
        return Program(statements)
    
    def parse_statement(self) -> Optional[ASTNode]:
        self.skip_newlines()
        token = self.current_token()
        
        if token.type == TokenType.CLASS:
            return self.parse_class()
        elif token.type == TokenType.DEF:
            return self.parse_function()
        elif token.type == TokenType.VAR:
            return self.parse_var_declaration()
        elif token.type == TokenType.IF:
            return self.parse_if_statement()
        elif token.type == TokenType.WHILE:
            return self.parse_while_statement()
        elif token.type == TokenType.FOR:
            return self.parse_for_statement()
        elif token.type == TokenType.BREAK:
            self.advance()
            self.skip_semicolon()
            return BreakStatement()
        elif token.type == TokenType.CONTINUE:
            self.advance()
            self.skip_semicolon()
            return ContinueStatement()
        elif token.type == TokenType.RETURN:
            return self.parse_return_statement()
        elif token.type == TokenType.LBRACE:
            return self.parse_block()
        else:
            expr = self.parse_expression()
            self.skip_semicolon()
            return ExpressionStatement(expr) if expr else None
    
    def skip_semicolon(self):
        if self.current_token().type == TokenType.SEMICOLON:
            self.advance()
    
    def parse_class(self) -> ClassDef:
        self.expect(TokenType.CLASS)
        name_token = self.expect(TokenType.IDENTIFIER)
        class_name = name_token.value
        
        parent = None
        if self.current_token().type == TokenType.EXTENDS:
            self.advance()
            parent_token = self.expect(TokenType.IDENTIFIER)
            parent = parent_token.value
        
        self.expect(TokenType.LBRACE)
        self.skip_newlines()
        
        methods = []
        properties = []
        
        while self.current_token().type != TokenType.RBRACE:
            self.skip_newlines()
            if self.current_token().type == TokenType.RBRACE:
                break
            
            if self.current_token().type == TokenType.VAR:
                properties.append(self.parse_var_declaration())
            elif self.current_token().type == TokenType.DEF:
                methods.append(self.parse_function())
            else:
                raise SyntaxError(f"Unexpected token in class: {self.current_token().type}")
            
            self.skip_newlines()
        
        self.expect(TokenType.RBRACE)
        self.skip_semicolon()
        
        return ClassDef(class_name, parent, methods, properties)
    
    def parse_function(self) -> FunctionDef:
        self.expect(TokenType.DEF)
        name_token = self.expect(TokenType.IDENTIFIER)
        func_name = name_token.value
        
        self.expect(TokenType.LPAREN)
        parameters = self.parse_parameters()
        self.expect(TokenType.RPAREN)
        
        self.expect(TokenType.ARROW)
        return_type_token = self.parse_type()
        
        self.expect(TokenType.LBRACE)
        body = self.parse_block()
        self.expect(TokenType.RBRACE)
        
        return FunctionDef(func_name, parameters, return_type_token, body)
    
    def parse_parameters(self) -> List[tuple]:
        parameters = []
        
        while self.current_token().type != TokenType.RPAREN:
            name_token = self.expect(TokenType.IDENTIFIER)
            self.expect(TokenType.COLON)
            param_type = self.parse_type()
            parameters.append((name_token.value, param_type))
            
            if self.current_token().type == TokenType.COMMA:
                self.advance()
            elif self.current_token().type != TokenType.RPAREN:
                raise SyntaxError(f"Expected ',' or ')' in parameters")
        
        return parameters
    
    def parse_type(self) -> str:
        token = self.current_token()
        type_map = {
            TokenType.TYPE_INT: 'int',
            TokenType.TYPE_FLOAT: 'float',
            TokenType.TYPE_STRING: 'string',
            TokenType.TYPE_BOOL: 'bool',
            TokenType.TYPE_LIST: 'list',
            TokenType.TYPE_DICT: 'dict',
            TokenType.TYPE_VOID: 'void',
            TokenType.IDENTIFIER: token.value,
        }
        
        if token.type in type_map:
            result = type_map[token.type]
            self.advance()
            return result
        
        raise SyntaxError(f"Expected type, got {token.type} at line {token.line}")
    
    def parse_var_declaration(self) -> VarDeclaration:
        self.expect(TokenType.VAR)
        name_token = self.expect(TokenType.IDENTIFIER)
        self.expect(TokenType.COLON)
        var_type = self.parse_type()
        
        value = None
        if self.current_token().type == TokenType.ASSIGN:
            self.advance()
            value = self.parse_expression()
        
        self.skip_semicolon()
        return VarDeclaration(name_token.value, var_type, value)
    
    def parse_if_statement(self) -> IfStatement:
        self.expect(TokenType.IF)
        self.expect(TokenType.LPAREN)
        condition = self.parse_expression()
        self.expect(TokenType.RPAREN)
        
        self.expect(TokenType.LBRACE)
        then_block = self.parse_block()
        self.expect(TokenType.RBRACE)
        
        elif_blocks = []
        while self.current_token().type == TokenType.ELIF:
            self.advance()
            self.expect(TokenType.LPAREN)
            elif_condition = self.parse_expression()
            self.expect(TokenType.RPAREN)
            self.expect(TokenType.LBRACE)
            elif_body = self.parse_block()
            self.expect(TokenType.RBRACE)
            elif_blocks.append((elif_condition, elif_body))
        
        else_block = None
        if self.current_token().type == TokenType.ELSE:
            self.advance()
            self.expect(TokenType.LBRACE)
            else_block = self.parse_block()
            self.expect(TokenType.RBRACE)
        
        return IfStatement(condition, then_block, elif_blocks if elif_blocks else None, else_block)
    
    def parse_while_statement(self) -> WhileStatement:
        self.expect(TokenType.WHILE)
        self.expect(TokenType.LPAREN)
        condition = self.parse_expression()
        self.expect(TokenType.RPAREN)
        
        self.expect(TokenType.LBRACE)
        body = self.parse_block()
        self.expect(TokenType.RBRACE)
        
        return WhileStatement(condition, body)
    
    def parse_for_statement(self) -> ForStatement:
        self.expect(TokenType.FOR)
        var_token = self.expect(TokenType.IDENTIFIER)
        self.expect(TokenType.IN)
        iterable = self.parse_expression()
        
        self.expect(TokenType.LBRACE)
        body = self.parse_block()
        self.expect(TokenType.RBRACE)
        
        return ForStatement(var_token.value, iterable, body)
    
    def parse_return_statement(self) -> ReturnStatement:
        self.expect(TokenType.RETURN)
        
        value = None
        if self.current_token().type not in [TokenType.SEMICOLON, TokenType.NEWLINE, TokenType.RBRACE]:
            value = self.parse_expression()
        
        self.skip_semicolon()
        return ReturnStatement(value)
    
    def parse_block(self) -> Block:
        statements = []
        self.skip_newlines()
        
        while self.current_token().type != TokenType.RBRACE:
            self.skip_newlines()
            if self.current_token().type == TokenType.RBRACE:
                break
            
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
            self.skip_newlines()
        
        return Block(statements)
    
    def parse_expression(self) -> ASTNode:
        return self.parse_or_expression()
    
    def parse_or_expression(self) -> ASTNode:
        left = self.parse_and_expression()
        
        while self.current_token().type == TokenType.OR:
            op = self.advance().value
            right = self.parse_and_expression()
            left = BinaryOp(left, 'or', right)
        
        return left
    
    def parse_and_expression(self) -> ASTNode:
        left = self.parse_equality()
        
        while self.current_token().type == TokenType.AND:
            op = self.advance().value
            right = self.parse_equality()
            left = BinaryOp(left, 'and', right)
        
        return left
    
    def parse_equality(self) -> ASTNode:
        left = self.parse_comparison()
        
        while self.current_token().type in [TokenType.EQ, TokenType.NEQ]:
            op = self.advance().value
            right = self.parse_comparison()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_comparison(self) -> ASTNode:
        left = self.parse_additive()
        
        while self.current_token().type in [TokenType.LT, TokenType.GT, TokenType.LTE, TokenType.GTE]:
            op = self.advance().value
            right = self.parse_additive()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_additive(self) -> ASTNode:
        left = self.parse_multiplicative()
        
        while self.current_token().type in [TokenType.PLUS, TokenType.MINUS]:
            op = self.advance().value
            right = self.parse_multiplicative()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_multiplicative(self) -> ASTNode:
        left = self.parse_power()
        
        while self.current_token().type in [TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO]:
            op = self.advance().value
            right = self.parse_power()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_power(self) -> ASTNode:
        left = self.parse_unary()
        
        if self.current_token().type == TokenType.POWER:
            op = self.advance().value
            right = self.parse_power()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_unary(self) -> ASTNode:
        if self.current_token().type in [TokenType.MINUS, TokenType.NOT]:
            op = self.advance().value
            operand = self.parse_unary()
            return UnaryOp(op, operand)
        
        return self.parse_postfix()
    
    def parse_postfix(self) -> ASTNode:
        expr = self.parse_primary()
        
        while True:
            token = self.current_token()
            
            if token.type == TokenType.DOT:
                self.advance()
                member_token = self.expect(TokenType.IDENTIFIER)
                
                # Method call or member access
                if self.current_token().type == TokenType.LPAREN:
                    self.advance()
                    args = self.parse_arguments()
                    self.expect(TokenType.RPAREN)
                    expr = MethodCall(expr, member_token.value, args)
                else:
                    expr = MemberAccess(expr, member_token.value)
            
            elif token.type == TokenType.LBRACKET:
                self.advance()
                index = self.parse_expression()
                self.expect(TokenType.RBRACKET)
                expr = IndexAccess(expr, index)
            
            elif token.type == TokenType.LPAREN and isinstance(expr, Identifier):
                # Function call
                self.advance()
                args = self.parse_arguments()
                self.expect(TokenType.RPAREN)
                expr = FunctionCall(expr.name, args)
            
            elif token.type == TokenType.ASSIGN:
                if isinstance(expr, Identifier):
                    self.advance()
                    value = self.parse_expression()
                    expr = Assignment(expr.name, value)
                elif isinstance(expr, MemberAccess):
                    self.advance()
                    value = self.parse_expression()
                    # Handle member assignment
                    expr = Assignment(f"{expr.object}.{expr.member}", value)
                else:
                    raise SyntaxError("Invalid assignment target")
            
            elif token.type in [TokenType.PLUS_ASSIGN, TokenType.MINUS_ASSIGN]:
                if isinstance(expr, Identifier):
                    op = self.advance().value
                    value = self.parse_expression()
                    expr = Assignment(expr.name, value, op)
                else:
                    raise SyntaxError("Invalid assignment target")
            
            else:
                break
        
        return expr
    
    def parse_primary(self) -> ASTNode:
        token = self.current_token()
        
        if token.type == TokenType.INT:
            self.advance()
            return IntLiteral(token.value)
        
        elif token.type == TokenType.FLOAT:
            self.advance()
            return FloatLiteral(token.value)
        
        elif token.type == TokenType.STRING:
            self.advance()
            return StringLiteral(token.value)
        
        elif token.type == TokenType.TRUE:
            self.advance()
            return BoolLiteral(True)
        
        elif token.type == TokenType.FALSE:
            self.advance()
            return BoolLiteral(False)
        
        elif token.type == TokenType.NULL:
            self.advance()
            return NullLiteral()
        
        elif token.type == TokenType.THIS:
            self.advance()
            return ThisLiteral()
        
        elif token.type == TokenType.IDENTIFIER:
            name = token.value
            self.advance()
            return Identifier(name)
        
        elif token.type == TokenType.NEW:
            self.advance()
            class_name_token = self.expect(TokenType.IDENTIFIER)
            self.expect(TokenType.LPAREN)
            args = self.parse_arguments()
            self.expect(TokenType.RPAREN)
            return NewInstance(class_name_token.value, args)
        
        elif token.type == TokenType.LBRACKET:
            return self.parse_list_literal()
        
        elif token.type == TokenType.LBRACE and self.is_dict_literal():
            return self.parse_dict_literal()
        
        elif token.type == TokenType.LPAREN:
            self.advance()
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return expr
        
        else:
            raise SyntaxError(f"Unexpected token: {token.type} at line {token.line}")
    
    def parse_list_literal(self) -> ListLiteral:
        self.expect(TokenType.LBRACKET)
        elements = []
        
        while self.current_token().type != TokenType.RBRACKET:
            elements.append(self.parse_expression())
            if self.current_token().type == TokenType.COMMA:
                self.advance()
        
        self.expect(TokenType.RBRACKET)
        return ListLiteral(elements)
    
    def is_dict_literal(self) -> bool:
        # Simple heuristic: check if it looks like a dict
        saved_pos = self.position
        self.advance()  # Skip LBRACE
        
        if self.current_token().type == TokenType.RBRACE:
            self.position = saved_pos
            return False
        
        # Try to detect key: value pattern
        self.parse_expression()
        result = self.current_token().type == TokenType.COLON
        
        self.position = saved_pos
        return result
    
    def parse_dict_literal(self) -> DictLiteral:
        self.expect(TokenType.LBRACE)
        pairs = []
        
        while self.current_token().type != TokenType.RBRACE:
            key = self.parse_expression()
            self.expect(TokenType.COLON)
            value = self.parse_expression()
            pairs.append((key, value))
            
            if self.current_token().type == TokenType.COMMA:
                self.advance()
        
        self.expect(TokenType.RBRACE)
        return DictLiteral(pairs)
    
    def parse_arguments(self) -> List[ASTNode]:
        arguments = []
        
        while self.current_token().type != TokenType.RPAREN:
            arguments.append(self.parse_expression())
            if self.current_token().type == TokenType.COMMA:
                self.advance()
        
        return arguments
