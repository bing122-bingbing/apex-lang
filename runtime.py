from typing import Dict, Any, Optional, List
from dataclasses import dataclass

class ApexObject:
    """Base class for all Apex objects"""
    def __init__(self, class_name: str, properties: Dict[str, Any]):
        self.class_name = class_name
        self.properties = properties
    
    def get_property(self, name: str):
        if name in self.properties:
            return self.properties[name]
        raise AttributeError(f"Property '{name}' not found in class '{self.class_name}'")
    
    def set_property(self, name: str, value):
        self.properties[name] = value
    
    def __repr__(self):
        return f"<{self.class_name}: {self.properties}>"

class ApexFunction:
    """Represents a function in Apex"""
    def __init__(self, name: str, parameters: List[tuple], return_type: str, body, env):
        self.name = name
        self.parameters = parameters
        self.return_type = return_type
        self.body = body
        self.env = env

class ApexClass:
    """Represents a class definition"""
    def __init__(self, name: str, parent: Optional[str], methods: Dict, properties: Dict):
        self.name = name
        self.parent = parent
        self.methods = methods
        self.properties = properties

class Environment:
    """Execution environment with variable scoping"""
    def __init__(self, parent: Optional['Environment'] = None):
        self.parent = parent
        self.variables: Dict[str, Any] = {}
    
    def define(self, name: str, value: Any, var_type: str = 'var'):
        self.variables[name] = {
            'value': value,
            'type': var_type
        }
    
    def get(self, name: str) -> Any:
        if name in self.variables:
            return self.variables[name]['value']
        elif self.parent:
            return self.parent.get(name)
        else:
            raise NameError(f"Variable '{name}' is not defined")
    
    def get_type(self, name: str) -> str:
        if name in self.variables:
            return self.variables[name]['type']
        elif self.parent:
            return self.parent.get_type(name)
        else:
            raise NameError(f"Variable '{name}' is not defined")
    
    def set(self, name: str, value: Any):
        if name in self.variables:
            self.variables[name]['value'] = value
        elif self.parent:
            self.parent.set(name, value)
        else:
            raise NameError(f"Variable '{name}' is not defined")
    
    def exists(self, name: str) -> bool:
        if name in self.variables:
            return True
        elif self.parent:
            return self.parent.exists(name)
        return False

class TypeSystem:
    """Manages type checking and conversion"""
    
    PRIMITIVE_TYPES = {'int', 'float', 'string', 'bool', 'void'}
    
    @staticmethod
    def get_type(value: Any) -> str:
        if isinstance(value, int):
            return 'int'
        elif isinstance(value, float):
            return 'float'
        elif isinstance(value, str):
            return 'string'
        elif isinstance(value, bool):
            return 'bool'
        elif isinstance(value, list):
            return 'list'
        elif isinstance(value, dict):
            return 'dict'
        elif value is None:
            return 'null'
        elif isinstance(value, ApexObject):
            return value.class_name
        else:
            return type(value).__name__
    
    @staticmethod
    def is_compatible(actual_type: str, expected_type: str) -> bool:
        """Check if actual_type is compatible with expected_type"""
        if actual_type == expected_type:
            return True
        
        # Allow null for any type
        if actual_type == 'null':
            return True
        
        # Numeric type compatibility
        if expected_type == 'float' and actual_type == 'int':
            return True
        
        # Object compatibility (inheritance)
        if isinstance(actual_type, str) and isinstance(expected_type, str):
            # Could extend this for inheritance checking
            return False
        
        return False
    
    @staticmethod
    def type_error(actual: str, expected: str):
        raise TypeError(f"Type mismatch: expected {expected}, got {actual}")

class BreakException(Exception):
    """Exception for break statement"""
    pass

class ContinueException(Exception):
    """Exception for continue statement"""
    pass

class ReturnException(Exception):
    """Exception for return statement"""
    def __init__(self, value):
        self.value = value
