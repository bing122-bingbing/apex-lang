from typing import Any, Dict, Optional
from ast_nodes import *
from runtime import (
    Environment, TypeSystem, ApexObject, ApexFunction, ApexClass,
    BreakException, ContinueException, ReturnException
)
import operator

class Interpreter:
    def __init__(self):
        self.global_env = Environment()
        self.current_env = self.global_env
        self.classes: Dict[str, ApexClass] = {}
        self.setup_builtins()
    
    def setup_builtins(self):
        """Setup built-in functions"""
        self.global_env.define('print', self.builtin_print, 'function')
        self.global_env.define('len', self.builtin_len, 'function')
        self.global_env.define('int', self.builtin_int, 'function')
        self.global_env.define('float', self.builtin_float, 'function')
        self.global_env.define('string', self.builtin_string, 'function')
        self.global_env.define('bool', self.builtin_bool, 'function')
        self.global_env.define('list', self.builtin_list, 'function')
        self.global_env.define('dict', self.builtin_dict, 'function')
    
    def interpret(self, program: Program) -> Any:
        result = None
        for statement in program.statements:
            result = self.execute(statement)
        return result
    
    def execute(self, node: ASTNode) -> Any:
        if node is None:
            return None
        
        if isinstance(node, Program):
            return self.interpret(node)
        elif isinstance(node, Block):
            return self.execute_block(node)
        elif isinstance(node, ExpressionStatement):
            return self.evaluate(node.expression)
        elif isinstance(node, VarDeclaration):
            return self.execute_var_declaration(node)
        elif isinstance(node, ClassDef):
            return self.execute_class_definition(node)
        elif isinstance(node, FunctionDef):
            return self.execute_function_definition(node)
        elif isinstance(node, IfStatement):
            return self.execute_if_statement(node)
        elif isinstance(node, WhileStatement):
            return self.execute_while_statement(node)
        elif isinstance(node, ForStatement):
            return self.execute_for_statement(node)
        elif isinstance(node, BreakStatement):
            raise BreakException()
        elif isinstance(node, ContinueStatement):
            raise ContinueException()
        elif isinstance(node, ReturnStatement):
            value = self.evaluate(node.value) if node.value else None
            raise ReturnException(value)
        else:
            return self.evaluate(node)
    
    def execute_block(self, block: Block) -> Any:
        new_env = Environment(self.current_env)
        prev_env = self.current_env
        self.current_env = new_env
        
        result = None
        try:
            for statement in block.statements:
                result = self.execute(statement)
        finally:
            self.current_env = prev_env
        
        return result
    
    def execute_var_declaration(self, node: VarDeclaration) -> None:
        value = None
        if node.value:
            value = self.evaluate(node.value)
            # Type checking
            actual_type = TypeSystem.get_type(value)
            if not TypeSystem.is_compatible(actual_type, node.var_type):
                TypeSystem.type_error(actual_type, node.var_type)
        
        self.current_env.define(node.name, value, node.var_type)
    
    def execute_class_definition(self, node: ClassDef) -> None:
        methods = {}
        properties = {}
        
        # Collect methods and properties
        for method in node.methods:
            methods[method.name] = method
        
        for prop in node.properties:
            properties[prop.name] = prop
        
        apex_class = ApexClass(node.name, node.parent, methods, properties)
        self.classes[node.name] = apex_class
        self.current_env.define(node.name, apex_class, 'class')
    
    def execute_function_definition(self, node: FunctionDef) -> None:
        func = ApexFunction(node.name, node.parameters, node.return_type, node.body, self.current_env)
        self.current_env.define(node.name, func, 'function')
    
    def execute_if_statement(self, node: IfStatement) -> Any:
        condition = self.evaluate(node.condition)
        
        if self.is_truthy(condition):
            return self.execute(node.then_block)
        
        if node.elif_blocks:
            for elif_condition, elif_body in node.elif_blocks:
                if self.is_truthy(self.evaluate(elif_condition)):
                    return self.execute(elif_body)
        
        if node.else_block:
            return self.execute(node.else_block)
        
        return None
    
    def execute_while_statement(self, node: WhileStatement) -> Any:
        result = None
        while self.is_truthy(self.evaluate(node.condition)):
            try:
                result = self.execute(node.body)
            except BreakException:
                break
            except ContinueException:
                continue
        return result
    
    def execute_for_statement(self, node: ForStatement) -> Any:
        iterable = self.evaluate(node.iterable)
        result = None
        
        if not isinstance(iterable, (list, dict, str)):
            raise TypeError(f"Cannot iterate over {TypeSystem.get_type(iterable)}")
        
        for item in iterable:
            self.current_env.define(node.variable, item)
            try:
                result = self.execute(node.body)
            except BreakException:
                break
            except ContinueException:
                continue
        
        return result
    
    def evaluate(self, node: ASTNode) -> Any:
        if isinstance(node, IntLiteral):
            return node.value
        elif isinstance(node, FloatLiteral):
            return node.value
        elif isinstance(node, StringLiteral):
            return node.value
        elif isinstance(node, BoolLiteral):
            return node.value
        elif isinstance(node, NullLiteral):
            return None
        elif isinstance(node, ListLiteral):
            return [self.evaluate(elem) for elem in node.elements]
        elif isinstance(node, DictLiteral):
            result = {}
            for key_node, value_node in node.pairs:
                key = self.evaluate(key_node)
                value = self.evaluate(value_node)
                result[key] = value
            return result
        elif isinstance(node, Identifier):
            return self.current_env.get(node.name)
        elif isinstance(node, ThisLiteral):
            return self.current_env.get('this')
        elif isinstance(node, BinaryOp):
            return self.evaluate_binary_op(node)
        elif isinstance(node, UnaryOp):
            return self.evaluate_unary_op(node)
        elif isinstance(node, Assignment):
            return self.evaluate_assignment(node)
        elif isinstance(node, FunctionCall):
            return self.call_function(node.name, node.arguments)
        elif isinstance(node, MethodCall):
            return self.call_method(node)
        elif isinstance(node, MemberAccess):
            return self.access_member(node)
        elif isinstance(node, IndexAccess):
            return self.access_index(node)
        elif isinstance(node, NewInstance):
            return self.create_instance(node)
        else:
            raise NotImplementedError(f"Evaluation not implemented for {type(node).__name__}")
    
    def evaluate_binary_op(self, node: BinaryOp) -> Any:
        left = self.evaluate(node.left)
        
        # Short-circuit evaluation for logical operators
        if node.operator == 'and':
            if not self.is_truthy(left):
                return False
            return self.is_truthy(self.evaluate(node.right))
        elif node.operator == 'or':
            if self.is_truthy(left):
                return True
            return self.is_truthy(self.evaluate(node.right))
        
        right = self.evaluate(node.right)
        
        ops = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv,
            '%': operator.mod,
            '**': operator.pow,
            '==': operator.eq,
            '!=': operator.ne,
            '<': operator.lt,
            '>': operator.gt,
            '<=': operator.le,
            '>=': operator.ge,
        }
        
        if node.operator in ops:
            try:
                return ops[node.operator](left, right)
            except Exception as e:
                raise RuntimeError(f"Error evaluating {node.operator}: {str(e)}")
        else:
            raise RuntimeError(f"Unknown operator: {node.operator}")
    
    def evaluate_unary_op(self, node: UnaryOp) -> Any:
        operand = self.evaluate(node.operand)
        
        if node.operator == '-':
            return -operand
        elif node.operator == 'not':
            return not self.is_truthy(operand)
        else:
            raise RuntimeError(f"Unknown unary operator: {node.operator}")
    
    def evaluate_assignment(self, node: Assignment) -> Any:
        value = self.evaluate(node.value)
        
        if node.operator == '=':
            self.current_env.set(node.target, value)
        elif node.operator == '+=':
            current = self.current_env.get(node.target)
            self.current_env.set(node.target, current + value)
        elif node.operator == '-=':
            current = self.current_env.get(node.target)
            self.current_env.set(node.target, current - value)
        
        return value
    
    def call_function(self, name: str, arguments: List[ASTNode]) -> Any:
        func = self.current_env.get(name)
        args = [self.evaluate(arg) for arg in arguments]
        
        if callable(func) and not isinstance(func, ApexFunction):
            # Built-in function
            return func(*args)
        
        if isinstance(func, ApexFunction):
            # Create new environment for function execution
            func_env = Environment(func.env)
            
            # Bind parameters
            if len(args) != len(func.parameters):
                raise TypeError(f"Function {name} expects {len(func.parameters)} arguments, got {len(args)}")
            
            for (param_name, param_type), arg_value in zip(func.parameters, args):
                # Type checking
                actual_type = TypeSystem.get_type(arg_value)
                if not TypeSystem.is_compatible(actual_type, param_type):
                    TypeSystem.type_error(actual_type, param_type)
                func_env.define(param_name, arg_value, param_type)
            
            # Execute function body
            prev_env = self.current_env
            self.current_env = func_env
            
            try:
                self.execute(func.body)
                return None  # Default return value
            except ReturnException as e:
                return e.value
            finally:
                self.current_env = prev_env
        
        raise TypeError(f"'{name}' is not callable")
    
    def call_method(self, node: MethodCall) -> Any:
        obj = self.evaluate(node.object)
        args = [self.evaluate(arg) for arg in node.arguments]
        
        if isinstance(obj, ApexObject):
            class_def = self.classes.get(obj.class_name)
            if class_def and node.method in class_def.methods:
                method = class_def.methods[node.method]
                
                # Create environment with 'this'
                func_env = Environment(self.current_env)
                func_env.define('this', obj)
                
                # Bind parameters
                for (param_name, param_type), arg_value in zip(method.parameters, args):
                    func_env.define(param_name, arg_value, param_type)
                
                # Execute method
                prev_env = self.current_env
                self.current_env = func_env
                
                try:
                    self.execute(method.body)
                    return None
                except ReturnException as e:
                    return e.value
                finally:
                    self.current_env = prev_env
        
        raise AttributeError(f"Method '{node.method}' not found")
    
    def access_member(self, node: MemberAccess) -> Any:
        obj = self.evaluate(node.object)
        
        if isinstance(obj, ApexObject):
            return obj.get_property(node.member)
        
        raise AttributeError(f"Cannot access member '{node.member}'")
    
    def access_index(self, node: IndexAccess) -> Any:
        obj = self.evaluate(node.object)
        index = self.evaluate(node.index)
        
        try:
            return obj[index]
        except (KeyError, IndexError) as e:
            raise IndexError(f"Index error: {str(e)}")
    
    def create_instance(self, node: NewInstance) -> Any:
        class_def = self.classes.get(node.class_name)
        if not class_def:
            raise NameError(f"Class '{node.class_name}' not found")
        
        # Create object with properties
        properties = {}
        for prop in class_def.properties:
            if prop.value:
                properties[prop.name] = self.evaluate(prop.value)
            else:
                properties[prop.name] = None
        
        obj = ApexObject(node.class_name, properties)
        
        # Call constructor if it exists
        if '__init__' in class_def.methods:
            init_method = class_def.methods['__init__']
            args = [self.evaluate(arg) for arg in node.arguments]
            
            func_env = Environment(self.current_env)
            func_env.define('this', obj)
            
            for (param_name, param_type), arg_value in zip(init_method.parameters, args):
                func_env.define(param_name, arg_value, param_type)
            
            prev_env = self.current_env
            self.current_env = func_env
            
            try:
                self.execute(init_method.body)
            except ReturnException:
                pass
            finally:
                self.current_env = prev_env
        
        return obj
    
    def is_truthy(self, value: Any) -> bool:
        if value is None or value is False:
            return False
        if value == 0 or value == '':
            return False
        return True
    
    # Built-in functions
    def builtin_print(self, *args):
        print(*args)
        return None
    
    def builtin_len(self, obj):
        return len(obj)
    
    def builtin_int(self, value):
        return int(value)
    
    def builtin_float(self, value):
        return float(value)
    
    def builtin_string(self, value):
        return str(value)
    
    def builtin_bool(self, value):
        return self.is_truthy(value)
    
    def builtin_list(self, *args):
        return list(args)
    
    def builtin_dict(self):
        return {}
