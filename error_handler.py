import sys
import traceback
from typing import Optional, List, Tuple
from dataclasses import dataclass
from enum import Enum

class ErrorLevel(Enum):
    WARNING = 1
    ERROR = 2
    FATAL = 3

@dataclass
class ApexException(Exception):
    message: str
    line: int = -1
    column: int = -1
    level: ErrorLevel = ErrorLevel.ERROR
    suggestion: Optional[str] = None
    context_line: Optional[str] = None
    
    def __str__(self):
        return self.format_error()
    
    def format_error(self) -> str:
        result = f"\n{'='*60}\n"
        result += f"[{self.level.name}] {self.__class__.__name__}\n"
        result += f"{'='*60}\n"
        
        if self.line > 0:
            result += f"Line {self.line}, Column {self.column}\n"
        
        result += f"\n  ✗ {self.message}\n"
        
        if self.context_line:
            result += f"\n  Code: {self.context_line}\n"
            result += f"         {' ' * (self.column - 1)}^\n"
        
        if self.suggestion:
            result += f"\n  💡 Suggestion: {self.suggestion}\n"
        
        result += f"\n{'='*60}\n"
        return result

class SyntaxException(ApexException):
    """Syntax error in code"""
    pass

class TypeError(ApexException):
    """Type mismatch error"""
    pass

class NameError(ApexException):
    """Undefined variable or function"""
    pass

class RuntimeException(ApexException):
    """Runtime error during execution"""
    pass

class AttributeException(ApexException):
    """Attribute not found"""
    pass

class IndexException(ApexException):
    """Index out of bounds"""
    pass

class CallException(ApexException):
    """Function call error"""
    pass

class StackTrace:
    """Call stack trace for debugging"""
    def __init__(self):
        self.stack: List[Tuple[str, int, str]] = []  # (function, line, file)
    
    def push(self, func_name: str, line: int, file: str = "<apex>"):
        self.stack.append((func_name, line, file))
    
    def pop(self):
        if self.stack:
            self.stack.pop()
    
    def __str__(self) -> str:
        if not self.stack:
            return ""
        
        result = "\nCall Stack Trace:\n"
        result += "-" * 50 + "\n"
        for i, (func, line, file) in enumerate(self.stack):
            result += f"  [{i}] {func} at {file}:{line}\n"
        result += "-" * 50 + "\n"
        return result

class ErrorHandler:
    """Global error handler with recovery suggestions"""
    
    KEYWORD_SUGGESTIONS = {
        'clas': 'class',
        'def': 'def',
        'iff': 'if',
        'whle': 'while',
        'fro': 'for',
        'retrun': 'return',
        'brk': 'break',
        'cont': 'continue',
        'tru': 'true',
        'fals': 'false',
        'nul': 'null',
    }
    
    OPERATOR_SUGGESTIONS = {
        '=': '== (comparison) or = (assignment)',
        '==': '== (comparison)',
        '!=': '!= (not equal)',
        'and': 'and (logical AND)',
        'or': 'or (logical OR)',
    }
    
    def __init__(self):
        self.stack_trace = StackTrace()
        self.error_count = 0
    
    @staticmethod
    def suggest_keyword(typo: str) -> Optional[str]:
        """Suggest correct keyword for typo"""
        return ErrorHandler.KEYWORD_SUGGESTIONS.get(typo.lower())
    
    @staticmethod
    def suggest_similar(token: str, candidates: List[str]) -> Optional[str]:
        """Find similar token using Levenshtein distance"""
        def levenshtein_distance(s1: str, s2: str) -> int:
            if len(s1) < len(s2):
                return levenshtein_distance(s2, s1)
            if len(s2) == 0:
                return len(s1)
            
            previous_row = range(len(s2) + 1)
            for i, c1 in enumerate(s1):
                current_row = [i + 1]
                for j, c2 in enumerate(s2):
                    insertions = previous_row[j + 1] + 1
                    deletions = current_row[j] + 1
                    substitutions = previous_row[j] + (c1 != c2)
                    current_row.append(min(insertions, deletions, substitutions))
                previous_row = current_row
            
            return previous_row[-1]
        
        best_match = None
        best_distance = 3
        
        for candidate in candidates:
            distance = levenshtein_distance(token, candidate)
            if distance < best_distance:
                best_distance = distance
                best_match = candidate
        
        return best_match
    
    def handle_error(self, exc: ApexException) -> None:
        """Handle and display error with suggestions"""
        self.error_count += 1
        print(exc.format_error())
        if self.stack_trace.stack:
            print(str(self.stack_trace))
        
        if exc.level == ErrorLevel.FATAL:
            sys.exit(1)
    
    def handle_exception(self, exc: Exception) -> None:
        """Handle generic Python exceptions"""
        if isinstance(exc, ApexException):
            self.handle_error(exc)
        else:
            print(f"\n{'='*60}")
            print(f"[FATAL] Unhandled Exception")
            print(f"{'='*60}")
            print(f"\n  {type(exc).__name__}: {str(exc)}\n")
            print(f"{'='*60}")
            traceback.print_exc()
            sys.exit(1)
