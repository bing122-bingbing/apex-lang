from dataclasses import dataclass
from typing import List, Optional, Any

@dataclass
class ASTNode:
    pass

# Expressions
@dataclass
class IntLiteral(ASTNode):
    value: int

@dataclass
class FloatLiteral(ASTNode):
    value: float

@dataclass
class StringLiteral(ASTNode):
    value: str

@dataclass
class BoolLiteral(ASTNode):
    value: bool

@dataclass
class NullLiteral(ASTNode):
    pass

@dataclass
class Identifier(ASTNode):
    name: str

@dataclass
class ListLiteral(ASTNode):
    elements: List[ASTNode]

@dataclass
class DictLiteral(ASTNode):
    pairs: List[tuple]

@dataclass
class BinaryOp(ASTNode):
    left: ASTNode
    operator: str
    right: ASTNode

@dataclass
class UnaryOp(ASTNode):
    operator: str
    operand: ASTNode

@dataclass
class Assignment(ASTNode):
    target: str
    value: ASTNode
    operator: str = '='

@dataclass
class MemberAccess(ASTNode):
    object: ASTNode
    member: str

@dataclass
class MethodCall(ASTNode):
    object: ASTNode
    method: str
    arguments: List[ASTNode]

@dataclass
class FunctionCall(ASTNode):
    name: str
    arguments: List[ASTNode]

@dataclass
class IndexAccess(ASTNode):
    object: ASTNode
    index: ASTNode

@dataclass
class NewInstance(ASTNode):
    class_name: str
    arguments: List[ASTNode]

@dataclass
class ThisLiteral(ASTNode):
    pass

# Statements
@dataclass
class Block(ASTNode):
    statements: List[ASTNode]

@dataclass
class ExpressionStatement(ASTNode):
    expression: ASTNode

@dataclass
class VarDeclaration(ASTNode):
    name: str
    var_type: str
    value: Optional[ASTNode] = None

@dataclass
class IfStatement(ASTNode):
    condition: ASTNode
    then_block: ASTNode
    elif_blocks: List[tuple] = None
    else_block: Optional[ASTNode] = None

@dataclass
class WhileStatement(ASTNode):
    condition: ASTNode
    body: ASTNode

@dataclass
class ForStatement(ASTNode):
    variable: str
    iterable: ASTNode
    body: ASTNode

@dataclass
class BreakStatement(ASTNode):
    pass

@dataclass
class ContinueStatement(ASTNode):
    pass

@dataclass
class ReturnStatement(ASTNode):
    value: Optional[ASTNode] = None

@dataclass
class FunctionDef(ASTNode):
    name: str
    parameters: List[tuple]
    return_type: str
    body: ASTNode

@dataclass
class ClassDef(ASTNode):
    name: str
    parent: Optional[str]
    methods: List[FunctionDef]
    properties: List[VarDeclaration]

@dataclass
class Program(ASTNode):
    statements: List[ASTNode]
